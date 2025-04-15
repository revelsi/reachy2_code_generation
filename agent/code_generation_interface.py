#!/usr/bin/env python
"""
Simple Gradio interface for the Reachy 2 Code Generation Agent.

This module provides a focused interface for generating Python code for the Reachy 2 robot
based on natural language requests, using only the official Reachy 2 SDK API.
"""

import os
import sys
import json
import argparse
import logging
import time
from typing import Dict, List, Any, Tuple, get_origin, get_args, Union, ClassVar, Optional
from dotenv import load_dotenv
import numpy as np
import traceback
import re

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code_generation_interface")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import OPENAI_API_KEY, MODEL, EVALUATOR_MODEL, AVAILABLE_MODELS, get_model_config

# Import Gradio
import gradio as gr

# Import the OpenAI client
from openai import OpenAI


class CodeGenerationInterface:
    """Interface for code generation using OpenAI API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        websocket_port: int = None,
        max_iterations: int = 1,
        evaluation_threshold: float = 75.0
    ):
        """Initialize the code generation interface.

        Args:
            api_key: The OpenAI API key.
            model: The OpenAI model to use.
            temperature: The temperature for the model (0.0 to 1.0).
            max_tokens: The maximum number of tokens to generate.
            top_p: The top_p value for the model (0.0 to 1.0).
            frequency_penalty: The frequency penalty for the model (-2.0 to 2.0).
            presence_penalty: The presence penalty for the model (-2.0 to 2.0).
            websocket_port: Port for the WebSocket server (default is 8765).
            max_iterations: Maximum number of optimization iterations.
            evaluation_threshold: Score threshold for considering code good enough.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.websocket_port = websocket_port
        self.max_iterations = max_iterations
        self.evaluation_threshold = evaluation_threshold
        
        # Initialize logger
        self.logger = logging.getLogger("code_generation_interface")
        
        # Initialize chat history
        self.chat_history = []
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        self.logger.debug(f"Initialized code generation interface with model: {model}")

    def generate_code(self, system_prompt: str, user_prompt: str, history: Optional[List[List[str]]] = None) -> Dict[str, Any]:
        """Generate code using the OpenAI API.

        Args:
            system_prompt: The system prompt to use.
            user_prompt: The user prompt to use.
            history: Optional list of previous user/assistant messages [[user_msg, assistant_msg], ...].

        Returns:
            Dict[str, Any]: The response from the API, including generated code.
        """
        try:
            self.logger.debug(f"Generating code with model: {self.model}")
            
            # Create messages for the API
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add history if provided
            if history:
                for user_msg, assistant_msg in history:
                    # Ensure we don't add None or empty messages
                    if user_msg:
                        messages.append({"role": "user", "content": user_msg})
                    if assistant_msg:
                        # Check if assistant message contains code to handle potential structure
                        if "```python" in assistant_msg:
                             # Simple extraction: Find first python block or assume content is assistant response
                             code_match = re.search(r"```python\n(.*?)```", assistant_msg, re.DOTALL)
                             if code_match:
                                 # Represent assistant turn as generating code
                                 # We might simplify this to just the message content for context
                                 messages.append({"role": "assistant", "content": assistant_msg}) # Keep full response for now
                             else:
                                 messages.append({"role": "assistant", "content": assistant_msg})
                        else:
                             messages.append({"role": "assistant", "content": assistant_msg})

            # Add the current user prompt
            messages.append({"role": "user", "content": user_prompt})
            
            self.logger.debug(f"API Messages length: {len(messages)}")
            # Log last few messages for context checking
            if len(messages) > 1:
                 self.logger.debug(f"Last message: {messages[-1]}")
            if len(messages) > 2:
                 self.logger.debug(f"Second last message: {messages[-2]}")

            # Call the OpenAI API with retry logic
            max_retries = 2
            retry_count = 0
            
            while retry_count <= max_retries:
                try:
                    # Call the OpenAI API
                    # GPT models use standard parameters
                    params = {
                        "model": self.model,
                        "messages": messages,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                        "top_p": self.top_p,
                        "frequency_penalty": self.frequency_penalty,
                        "presence_penalty": self.presence_penalty
                    }
                    
                    # Make the API call
                    response = self.client.chat.completions.create(**params)
                    
                    # Extract code and explanation from the response
                    content = response.choices[0].message.content
                    code, explanation = self._extract_code_and_explanation(content)
                    
                    # Prepare the response
                    result = {
                        "message": explanation,
                        "code": code,
                        "raw_response": content
                    }
                    
                    self.logger.debug("Code generation successful")
                    return result
                    
                except Exception as retry_error:
                    self.logger.warning(f"API call attempt {retry_count + 1} failed: {retry_error}")
                    retry_count += 1
                    if retry_count > max_retries:
                        raise  # Re-raise after max retries
                    time.sleep(1)  # Wait before retrying
            
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "message": f"Error generating code: {str(e)}",
                "code": "",
                "raw_response": ""
            }
    
    def _extract_code_and_explanation(self, response: str) -> tuple[str, str]:
        """Extract code and explanation (conversational intro) from the response.

        Assumes the AI follows the prompt instruction to provide a brief conversational
        explanation BEFORE the code block, and nothing after.

        Args:
            response: The raw response string from the API.

        Returns:
            tuple[str, str]: (code, explanation)
        """
        code = ""
        explanation = ""
        
        # Find the start of the first Python code block
        code_block_start = response.find("```python")
        
        if code_block_start != -1:
            # Extract explanation as the text before the code block
            explanation = response[:code_block_start].strip()
            
            # Find the end of the code block
            code_block_end = response.find("```", code_block_start + len("```python"))
            
            if code_block_end != -1:
                # Extract the code itself
                code = response[code_block_start + len("```python"):code_block_end].strip()
            else:
                # Code block started but didn't end? Extract what we can.
                code = response[code_block_start + len("```python"):].strip()
                self.logger.warning("Code block started with ```python but closing ``` was not found.")
        else:
            # No Python code block found. Assume the entire response is explanation/message.
            explanation = response.strip()
            code = "" # No code to display
            self.logger.info("No ```python code block found in the response.")
            
        # If explanation is empty but code exists, provide a default explanation
        if not explanation and code:
            explanation = "Okay, here is the generated code:"
            self.logger.debug("No explanation found before code block, using default.")
        elif not explanation and not code:
            # If both are empty, the response was likely empty or just whitespace
            explanation = "(No response content received)"
            self.logger.warning("Empty response received from the API.")
            
        return code, explanation

    def process_message(self, message: str, history: List[List[str]]) -> Tuple[List[Dict[str, str]], str, Dict[str, Any], str]:
        """
        Process a user message, update the chat history, and generate/optimize code.
        
        Args:
            message: The new user message.
            history: Chat history in Gradio's list format [[user_msg, assistant_msg], ...].
                    For back-compatibility with our chat UI.
            
        Returns:
            Tuple: 
                - Updated history (as Dict format for compatibility with backend)
                - The latest generated/optimized code.
                - Code validation dictionary.
                - Status message string.
        """
        try:
            # Basic message validation
            if not isinstance(message, str) or not message.strip():
                error_msg = "Empty or invalid message."
                # Return as dictionary format for backend
                history_dict = [{"role": "assistant", "content": error_msg}]
                return history_dict, "", {"valid": False, "errors": [error_msg], "warnings": [], "score": 0.0}, "❌ Invalid input"

            # Convert list-format history to dict format for backend
            backend_history = []
            if history and isinstance(history, list):
                for item in history:
                    if isinstance(item, list) and len(item) == 2:
                        user_msg, assistant_msg = item
                        if user_msg is not None:
                            backend_history.append({"role": "user", "content": user_msg})
                        if assistant_msg is not None:
                            backend_history.append({"role": "assistant", "content": assistant_msg})

            # --- Code Generation Logic ---
            try:
                from agent.code_generation_pipeline import CodeGenerationPipeline
                from agent.code_evaluator import CodeEvaluator
                from agent.code_generation_agent import ReachyCodeGenerationAgent
                
                generator = ReachyCodeGenerationAgent(
                    api_key=self.client.api_key,
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                evaluator = CodeEvaluator(
                    api_key=self.client.api_key,
                    model=EVALUATOR_MODEL,
                    max_tokens=self.max_tokens,
                    temperature=max(0.1, self.temperature - 0.1)
                )
                pipeline = CodeGenerationPipeline(
                    generator=generator,
                    evaluator=evaluator,
                    evaluation_threshold=self.evaluation_threshold,
                    max_iterations=self.max_iterations
                )
            except Exception as init_error:
                self.logger.error(f"Error initializing components: {init_error}", exc_info=True)
                history_dict = backend_history + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": f"Error initializing components: {init_error}"}
                ]
                return history_dict, "", {"valid": False, "errors": [str(init_error)], "warnings": []}, "❌ Initialization Error"

            # Generate code
            try:
                self.logger.info(f"Starting pipeline for: \"{message[:100]}...\" with history length {len(backend_history)}")
                pipeline_result = pipeline.generate_code(
                    user_request=message,
                    history=backend_history,
                    optimize=True
                )
                
                # Process pipeline result
                best_code = (pipeline_result.get("final_code") or 
                            pipeline_result.get("optimized_code") or 
                            pipeline_result.get("generated_code", ""))
                
                # Extract AI's conversational reply from raw response
                raw_response = pipeline_result.get("raw_response", "")
                _, explanation = self._extract_code_and_explanation(raw_response)
                
                # Build validation information 
                evaluation_result = pipeline_result.get("evaluation_result", {})
                code_validation = {
                    "valid": evaluation_result.get("valid", False),
                    "errors": evaluation_result.get("errors", []),
                    "warnings": evaluation_result.get("warnings", []),
                    "score": evaluation_result.get("score", 0.0)
                }
                
                # Construct assistant response message
                score = code_validation['score']
                
                # Use the explanation as the assistant's message, but ensure it's not empty
                assistant_message = explanation if explanation else "Here's the code I generated for your request."
                # Optionally add a score/warnings note
                if not pipeline_result.get("success", False):
                    assistant_message += f" (Score: {score:.1f}/100)"
                
                # Construct final status message - this goes to status_update in UI
                if pipeline_result.get("success", False):
                    status = f"✅ Success (Score: {score:.1f})"
                elif best_code:
                    status = f"⚠️ Issues Found (Score: {score:.1f})"
                else:
                    status = "❌ Generation Failed"
                
                # Add to history in dictionary format for backend compatibility
                final_history = backend_history + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_message}
                ]
                
                self.logger.info(f"Processed message. Returning history length: {len(final_history)}, code: {len(best_code)} chars")
                return final_history, best_code, code_validation, status
                
            except Exception as e:
                self.logger.error(f"Error in code generation: {e}", exc_info=True)
                error_message = f"Error generating code: {str(e)}"
                history_dict = backend_history + [
                    {"role": "user", "content": message}, 
                    {"role": "assistant", "content": f"❌ {error_message}"}
                ]
                return history_dict, "", {"valid": False, "errors": [error_message], "warnings": []}, f"❌ Error: {str(e)}"
                
        except Exception as e:
            self.logger.error(f"Critical error in process_message: {e}", exc_info=True)
            error_message = f"Critical Error: {str(e)}"
            return [
                {"role": "user", "content": message},
                {"role": "assistant", "content": f"❌ {error_message}"}
            ], "", {"valid": False, "errors": [error_message], "warnings": []}, f"❌ Critical Error: {str(e)}"
    
    def reset_chat(self) -> Tuple[List[Dict[str, str]], str, Dict[str, Any], str]:
        """
        Reset the chat history and clear all outputs.
        
        Returns:
            Tuple: Empty chat history, empty code, empty validation, and status message.
        """
        self.chat_history = []
        return [], "", {"valid": False, "errors": [], "warnings": []}, "Chat reset. Ready for new requests."
    
    def update_model_config(self, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """
        Update the model configuration.
        
        Args:
            temperature: The temperature to use.
            max_tokens: The maximum number of tokens to generate.
            
        Returns:
            Dict: The updated model configuration.
        """
        # Update the model configuration
        self.model_config = {
            "model": EVALUATOR_MODEL,  # Use centralized evaluator model
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Reinitialize the agent with the new configuration
        # self.agent = ReachyCodeGenerationAgent(
        #     model=EVALUATOR_MODEL,  # Use centralized evaluator model
        #     temperature=temperature,
        #     max_tokens=max_tokens
        # )
        
        # Check if Reachy is available
        self.reachy_available = self.check_reachy_available()
        
        return self.model_config
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute the generated code.
        
        Args:
            code: The code to execute.
            
        Returns:
            Dict: The execution result.
        """
        if not code or not code.strip():
            return {
                "success": False,
                "error": "No code provided for execution",
                "output": "",
                "status": "❌ No code to execute",
                "feedback": "Please generate code first before attempting to execute."
            }
            
        try:
            # Log the code being executed
            self.logger.info(f"Preparing to execute code...")
            
            # Use the agent's execute_code method for more thorough execution handling
            try:
                from agent.code_generation_agent import ReachyCodeGenerationAgent
                agent = ReachyCodeGenerationAgent(api_key=self.client.api_key, model=self.model)
                
                # Execute the code (force=True to bypass validation confirmation in the UI)
                result = agent.execute_code(code, confirm=False, force=True)
                
                # Execution was handled by the agent
                return result
            
            except ImportError:
                self.logger.warning("Could not import ReachyCodeGenerationAgent, falling back to basic execution")
                
                # Check if Reachy is available
                import socket
                reachy_available = False
                try:
                    # Try to connect to the Reachy gRPC server
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    result = s.connect_ex(('localhost', 50051))  # Default gRPC port for Reachy
                    s.close()
                    reachy_available = (result == 0)
                    self.logger.info(f"Reachy availability check: {'Available' if reachy_available else 'Not available'}")
                except Exception as e:
                    self.logger.error(f"Error checking Reachy availability: {e}")
                    self.logger.error(traceback.format_exc())
                    reachy_available = False
                
                if not reachy_available:
                    self.logger.warning("Reachy robot is not available")
                    return {
                        "success": False,
                        "error": "Reachy robot is not available",
                        "output": "Cannot execute code because the Reachy robot or simulator is not running or not accessible.",
                        "status": "❌ Robot connection failed",
                        "feedback": "Please ensure that:\n1. The Reachy robot or simulator is running\n2. The gRPC server is accessible on port 50051\n3. There are no network connectivity issues"
                    }
                
                # Create a temporary script file
                import tempfile
                import subprocess
                import os
                
                self.logger.info("Creating temporary script file...")
                with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp_file:
                    temp_file_path = temp_file.name
                    temp_file.write(code)
                    self.logger.info(f"Created temporary script at {temp_file_path}")
                
                try:
                    # Execute the code
                    self.logger.info("Executing code...")
                    process = subprocess.Popen(
                        ['python', temp_file_path], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    self.logger.info("Waiting for process completion...")
                    stdout, stderr = process.communicate(timeout=30)  # 30 second timeout
                    
                    # Prepare result - this is a simple execution without the agent's detailed feedback
                    result = {
                        "success": process.returncode == 0,
                        "error": f"Process exited with code {process.returncode}" if process.returncode != 0 else "",
                        "output": stdout,
                        "stderr": stderr,
                        "status": "✅ Code executed successfully" if process.returncode == 0 else f"❌ Execution failed (exit code {process.returncode})"
                    }
                    
                    # Add simple feedback based on execution results (this is execution feedback, not validation)
                    if process.returncode == 0:
                        if stdout.strip():
                            result["feedback"] = f"Execution successful. Output:\n{stdout}"
                        else:
                            result["feedback"] = "Execution completed successfully with no output."
                    else:
                        if stderr.strip():
                            result["feedback"] = f"Execution failed. Error details:\n{stderr}"
                        else:
                            result["feedback"] = f"Execution failed with exit code {process.returncode}."
                    
                    self.logger.info(f"Code execution completed with exit code {process.returncode}")
                    return result
                    
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.logger.error("Execution timed out after 30 seconds")
                    return {
                        "success": False,
                        "error": "Execution timed out after 30 seconds",
                        "output": "",
                        "status": "❌ Execution timed out",
                        "feedback": "The code execution timed out after 30 seconds. This could be due to:\n1. An infinite loop in the code\n2. Long-running operations\n3. The robot taking too long to respond\n\nPlease check your code and try again with a simpler implementation."
                    }
                except Exception as e:
                    self.logger.error(f"Error during execution: {e}")
                    self.logger.error(traceback.format_exc())
                    return {
                        "success": False,
                        "error": str(e),
                        "output": "",
                        "status": "❌ Execution error",
                        "feedback": f"An error occurred during execution:\n{str(e)}"
                    }
                finally:
                    # Clean up the temporary file
                    try:
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)
                            self.logger.info(f"Removed temporary script at {temp_file_path}")
                    except Exception as cleanup_error:
                        self.logger.error(f"Error cleaning up temporary file: {cleanup_error}")
                
        except Exception as e:
            self.logger.error(f"Error in execute_code: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "status": "❌ System error",
                "feedback": f"A system error occurred:\n{str(e)}\n\nThis might be due to missing dependencies or system configuration issues."
            }
    
    def check_reachy_available(self) -> bool:
        """
        Check if the Reachy robot is available.
        
        Returns:
            bool: True if the Reachy robot is available, False otherwise.
        """
        import socket
        try:
            # Try to connect to the Reachy gRPC server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex(('localhost', 50051))  # Default gRPC port for Reachy
            s.close()
            return result == 0
        except:
            return False
    
    def check_reachy_status(self) -> str:
        """
        Check if the Reachy robot is available and return a status message.
        
        Returns:
            str: HTML status message.
        """
        self.reachy_available = self.check_reachy_available()
        reachy_status = "Connected" if self.reachy_available else "Not Connected"
        reachy_status_color = "green" if self.reachy_available else "red"
        return f"<p>Reachy Robot Status: <span style='color: {reachy_status_color};'>{reachy_status}</span></p>"
    
    def launch_interface(self, share: bool = False, port: int = 7860):
        """Launch the Gradio interface.
        
        Args:
            share: Whether to create a public link.
            port: The port to run the server on.
        """
        import gradio as gr
        
        try:
            # Get Gradio version for compatibility
            gradio_version = gr.__version__
            self.logger.info(f"Using Gradio version: {gradio_version}")
            
            # Create the interface with a clean modern design
            with gr.Blocks(
                title="Reachy 2 Code Generator",
                theme=gr.themes.Soft(primary_hue="indigo"),
                css="""
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;500&display=swap');
                
                * { font-family: 'Inter', system-ui, sans-serif; }
                
                /* Apply Source Code Pro to code editor */
                .cm-editor .cm-content, 
                .cm-editor .cm-line,
                .cm-editor {
                    font-family: 'Source Code Pro', monospace !important;
                    font-size: 14px !important;
                }
                
                /* Improve chat message styling */
                .message {
                    font-family: 'Inter', system-ui, sans-serif !important;
                    font-size: 15px !important;
                    line-height: 1.5 !important;
                    margin-bottom: 8px !important;
                }
                
                /* Improve chat container */
                .chatbot-container {
                    border-radius: 8px !important;
                    background-color: #f9fafb !important;
                }
                
                .status-ready { 
                    padding: 10px 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    background-color: rgba(79, 70, 229, 0.1);
                    border-left: 4px solid #4f46e5;
                }
                .status-processing { 
                    padding: 10px 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    background-color: rgba(234, 179, 8, 0.1);
                    border-left: 4px solid #eab308;
                }
                .status-success { 
                    padding: 10px 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    background-color: rgba(34, 197, 94, 0.1);
                    border-left: 4px solid #22c55e;
                }
                .status-error { 
                    padding: 10px 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    background-color: rgba(239, 68, 68, 0.1);
                    border-left: 4px solid #ef4444;
                }
                """
            ) as demo:
                # Header section with simple, clean design
                gr.Markdown(
                    """
                    # Reachy 2 Code Generation
                    Generate Python code for controlling the Reachy 2 robot using natural language.
                    """
                )
                
                # Main content area with two columns
                with gr.Row(equal_height=False):
                    # Left column for chat and input
                    with gr.Column(scale=1):
                        gr.Markdown("## Conversation")
                        
                        # Chatbot display - Improved setup with no avatars
                        chatbot = gr.Chatbot(
                            value=[], 
                            height=400,
                            bubble_full_width=False,
                            avatar_images=(None, None),  # Remove avatar images
                            show_copy_button=True,
                            render=True,
                        )
                        
                        # Textbox for user input
                        msg = gr.Textbox(
                            placeholder="Type your request or code refinement here...",
                            lines=3,
                            label="Message",
                            show_label=False
                        )
                        
                        # Submit/Clear buttons
                        with gr.Row():
                            submit_btn = gr.Button("Send", variant="primary", scale=2)
                            clear_btn = gr.Button("Clear Chat", variant="secondary", scale=1)
                        
                        # Status indicator
                        status_md = gr.Markdown(
                            """<div class="status-ready">Ready for your request</div>""",
                        )
                        
                    # Right column for code and execution
                    with gr.Column(scale=1):
                        gr.Markdown("## Generated Code")
                        
                        # Code editor with syntax highlighting
                        code_editor = gr.Code(
                            value="",
                            language="python",
                            interactive=True,
                            lines=12,
                        )
                        
                        # Execute button
                        execute_btn = gr.Button("Execute Code", variant="primary")
                        
                        # Feedback section - REMOVING THE TITLE
                        # gr.Markdown("## Execution Feedback")
                        feedback = gr.Textbox(
                            value="",
                            lines=6,
                            max_lines=12,
                            label="Execution Results",
                            interactive=False,
                        )
                
                # --- SIMPLIFIED CHAT FUNCTIONS ---
                # Basic two-step function for showing user message immediately, then AI response
                def chat_and_code(message, history):
                    """Two-step function for handling chat and code generation."""
                    # First, add user message to history and display
                    history.append([message, None])
                    yield history, status_update("Processing your request...", "processing"), "", ""
                    
                    # Call backend to generate code and response
                    try:
                        # Call the backend process_message function - it still returns List[List]
                        # but we're now using the older format directly in the UI
                        full_history, code, validation, status = self.process_message(message, history[:-1])
                        
                        # Extract the last assistant message
                        if full_history and len(full_history) > 0:
                            # Update the placeholder in the UI history
                            if full_history[-1]["role"] == "assistant":
                                history[-1][1] = full_history[-1]["content"]
                            else:
                                # Fallback if something went wrong with response structure
                                history[-1][1] = "I've generated code for your request."
                        else:
                            history[-1][1] = "Code generated but couldn't create a response message."
                            
                        # Determine appropriate status message
                        status_message = status
                        status_type = "error" if "❌" in status else "success" if "✅" in status else "processing"
                        
                        # Send final state: history with AI response, status update, code
                        yield history, status_update(status_message, status_type), code, ""
                        
                    except Exception as e:
                        self.logger.error(f"Error in chat_and_code: {e}", exc_info=True)
                        # Add error message to history
                        history[-1][1] = f"❌ Error: {str(e)}"
                        yield history, status_update(f"Error: {str(e)}", "error"), "", ""
                
                # Helper for status messages
                def status_update(message, status="processing"):
                    """Create a status message with appropriate styling."""
                    status_class = {
                        "ready": "status-ready",
                        "processing": "status-processing",
                        "success": "status-success", 
                        "error": "status-error"
                    }.get(status, "status-ready")
                    
                    emoji = {
                        "ready": "🔹",
                        "processing": "⏳",
                        "success": "✅",
                        "error": "❌" 
                    }.get(status, "🔹")
                    
                    return f"""<div class="{status_class}">{emoji} {message}</div>"""
                
                # Execute code function - simplified
                def execute_code(code):
                    """Execute the code and yield updates."""
                    if not code or not code.strip():
                        yield status_update("No code to execute", "error"), "Please generate code first."
                        return
                    
                    # Set processing status
                    yield status_update("Executing code...", "processing"), "Executing... please wait."
                    
                    # Execute the code
                    try:
                        result = self.execute_code(code)
                        
                        # Process the result
                        success = result.get("success", False)
                        status_type = "success" if success else "error"
                        status_msg = "Execution successful" if success else "Execution failed"
                        
                        # Get the feedback text
                        feedback_text = result.get("feedback", "") or result.get("output", "")
                        if not feedback_text.strip():
                            feedback_text = "No output from execution."
                            
                        # Return the final result
                        yield status_update(status_msg, status_type), feedback_text
                    
                    except Exception as e:
                        self.logger.error(f"Error executing code: {e}", exc_info=True)
                        yield status_update(f"Error: {str(e)}", "error"), f"Error executing code: {str(e)}"
                
                # Clear chat function
                def clear_chat():
                    """Reset the chat and code."""
                    return [], status_update("Chat cleared. Ready for new request.", "ready"), "", ""
                
                # --- CONNECT EVENT HANDLERS ---
                # Submit button triggers chat and code function
                submit_btn.click(
                    fn=chat_and_code,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, status_md, code_editor, feedback]
                ).then(
                    fn=lambda: "", 
                    inputs=None, 
                    outputs=msg  # Clear input box after sending
                )
                
                # Enter key in message box also triggers chat
                msg.submit(
                    fn=chat_and_code,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, status_md, code_editor, feedback]
                ).then(
                    fn=lambda: "", 
                    inputs=None, 
                    outputs=msg  # Clear input box after sending
                )
                
                # Execute button triggers code execution
                execute_btn.click(
                    fn=execute_code,
                    inputs=[code_editor],
                    outputs=[status_md, feedback]
                )
                
                # Clear button resets everything
                clear_btn.click(
                    fn=clear_chat,
                    inputs=[],
                    outputs=[chatbot, status_md, code_editor, feedback]
                )
            
            # Launch the interface
            self.logger.info(f"Launching Gradio interface on port {port} with share={share}")
            demo.launch(
                server_name="0.0.0.0",
                server_port=port,
                share=share,
                show_error=True
            )
            
        except Exception as e:
            self.logger.error(f"Error launching interface: {e}")
            self.logger.error(traceback.format_exc())
            raise


def main():
    """Main entry point for the code generation interface."""
    parser = argparse.ArgumentParser(description="Reachy 2 Code Generation Interface")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--share", action="store_true", help="Create a public link")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--websocket-port", type=int, help="Port for the WebSocket server (default is 8765)")
    parser.add_argument("--generator-model", help="Specify the generator model")
    parser.add_argument("--temperature", type=float, help="Specify the temperature")
    parser.add_argument("--max-tokens", type=int, help="Specify the max_tokens")
    
    args = parser.parse_args()
    
    print(f"Starting Reachy 2 Code Generation Interface with model: {args.generator_model or 'gpt-4.1-mini'}")
    
    # Create interface with default temperature and max_tokens
    interface = CodeGenerationInterface(
        api_key=args.api_key,
        model=args.generator_model or "gpt-4.1-mini",
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        websocket_port=args.websocket_port,
    )
    
    interface.launch_interface(share=args.share, port=args.port)


if __name__ == "__main__":
    main() 