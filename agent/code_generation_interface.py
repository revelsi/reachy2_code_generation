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
from typing import Dict, List, Any, Tuple, get_origin, get_args, Union, ClassVar
from dotenv import load_dotenv
import numpy as np
import traceback

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
        model: str = "gpt-4o",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        websocket_port: int = None,
        max_iterations: int = 2,
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

    def generate_code(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generate code using the OpenAI API.

        Args:
            system_prompt: The system prompt to use.
            user_prompt: The user prompt to use.

        Returns:
            Dict[str, Any]: The response from the API, including generated code.
        """
        try:
            self.logger.debug(f"Generating code with model: {self.model}")
            
            # Create messages for the API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
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
        """Extract code and explanation from the response.

        Args:
            response: The response from the API.

        Returns:
            tuple[str, str]: The extracted code and explanation.
        """
        # Default values
        code = ""
        explanation = response
        
        # Check if the response contains a code block
        if "```python" in response:
            # Split by Python code blocks
            parts = response.split("```python")
            
            if len(parts) > 1:
                # Get the first part as the explanation (before the code block)
                explanation = parts[0].strip()
                
                # Get the code from the first code block
                code_parts = parts[1].split("```", 1)
                if len(code_parts) > 0:
                    code = code_parts[0].strip()
                
                # If there's content after the code block, add it to the explanation
                if len(code_parts) > 1 and code_parts[1].strip():
                    explanation += "\n\n" + code_parts[1].strip()
        
        return code, explanation

    def process_message(self, message: str, history: List[List[str]]) -> Tuple[List[List[str]], str, Dict[str, Any], str]:
        """
        Process a user message and update the chat history.
        
        Args:
            message: User message.
            history: Current chat history.
            
        Returns:
            Tuple: Updated chat history, generated code, code validation, and status message.
        """
        try:
            # Simple handling for Request objects from Gradio
            if hasattr(message, "__class__") and message.__class__.__name__ == "Request":
                # Just extract the text field which contains the actual message
                self.logger.warning("Received a Request object, extracting text")
                try:
                    # For starlette Request or similar, try to extract form data
                    if hasattr(message, "form"):
                        form_data = message.form()
                        if isinstance(form_data, dict) and "text" in form_data:
                            message = form_data["text"]
                    # Fallback to string representation
                    if not isinstance(message, str):
                        message = "Generate code for Reachy 2 robot"
                except Exception as e:
                    self.logger.error(f"Error extracting message: {e}")
                    message = "Generate code for Reachy 2 robot"

            # Ensure history is a list
            if not isinstance(history, list):
                history = []

            # Add a status message to the chat
            history.append([message, "Generating code..."])
            self.chat_history = history
            
            # Import necessary components
            from agent.code_generation_pipeline import CodeGenerationPipeline
            from agent.code_evaluator import CodeEvaluator
            from agent.code_generation_agent import ReachyCodeGenerationAgent
            
            # Create generator agent and evaluator
            try:
                # Prepare generator parameters based on model type
                generator_kwargs = {
                    "api_key": self.client.api_key,
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
                
                generator = ReachyCodeGenerationAgent(**generator_kwargs)
                
                # Prepare evaluator parameters based on model type
                evaluator_model = EVALUATOR_MODEL  # Use centralized evaluator model
                evaluator_kwargs = {
                    "api_key": self.client.api_key,
                    "model": evaluator_model,
                    "max_tokens": self.max_tokens,
                    "temperature": max(0.1, self.temperature - 0.1)  # Lower temp for evaluator
                }
                
                evaluator = CodeEvaluator(**evaluator_kwargs)
                
                # Create the pipeline with integrated approach
                pipeline = CodeGenerationPipeline(
                    generator=generator,
                    evaluator=evaluator,
                    evaluation_threshold=self.evaluation_threshold,
                    max_iterations=self.max_iterations
                )
                
                self.logger.info("Components initialized successfully")
            except Exception as init_error:
                self.logger.error(f"Error initializing components: {init_error}")
                self.logger.error(traceback.format_exc())
                raise RuntimeError(f"Failed to initialize components: {init_error}")
            
            # Generate, evaluate, and optimize code
            try:
                self.logger.info(f"Starting code generation for request: {message[:100]}...")
                pipeline_result = pipeline.generate_code(
                    user_request=message,
                    optimize=True  # Always try to optimize the code
                )
                self.logger.info("Code generation completed successfully")
                
                # Add debug logging to track the pipeline result
                self.logger.debug(f"Pipeline result keys: {pipeline_result.keys() if isinstance(pipeline_result, dict) else 'Not a dict'}")
                
                # Extract the best code (optimized if available, otherwise generated)
                best_code = ""
                if isinstance(pipeline_result, dict):
                    # Try to get code in order of preference: final_code, optimized_code, generated_code
                    best_code = (pipeline_result.get("final_code") or 
                                pipeline_result.get("optimized_code") or 
                                pipeline_result.get("generated_code", ""))
                    
                    # Log the code extraction for debugging
                    self.logger.info(f"Code extraction sources - final_code: {'final_code' in pipeline_result}")
                    self.logger.info(f"Code extraction sources - optimized_code: {'optimized_code' in pipeline_result}")
                    self.logger.info(f"Code extraction sources - generated_code: {'generated_code' in pipeline_result}")
                    self.logger.info(f"Code extracted - Final code length: {len(best_code) if best_code else 0}")
                    
                    # Extract evaluation result for validation
                    evaluation_result = pipeline_result.get("evaluation_result", {})
                    
                    # Convert evaluation result to the expected validation format
                    code_validation = {
                        "valid": evaluation_result.get("valid", False),
                        "errors": evaluation_result.get("errors", []),
                        "warnings": evaluation_result.get("warnings", []),
                        "score": evaluation_result.get("score", 0.0)
                    }
                    
                    # Update chat history with a concise response
                    if pipeline_result.get("success", False):
                        response_message = "✅ Code generated and optimized successfully."
                    else:
                        response_message = "⚠️ Code generated with some issues."
                    
                    # Create a status message
                    if pipeline_result.get("success", False):
                        status = f"✅ Code generation successful"
                    elif not best_code:
                        status = "❌ No code generated. Try a different request."
                    else:
                        status = f"⚠️ Code has issues"
                else:
                    self.logger.error(f"Pipeline returned non-dictionary result: {type(pipeline_result)}")
                    response_message = "⚠️ Error in code generation pipeline."
                    code_validation = {"valid": False, "errors": ["Internal error in code generation"], "warnings": [], "score": 0.0}
                    status = "❌ Code generation pipeline error"
            except Exception as pipeline_error:
                self.logger.error(f"Error in pipeline execution: {pipeline_error}")
                self.logger.error(traceback.format_exc())
                best_code = ""
                response_message = f"⚠️ Error in code generation: {str(pipeline_error)}"
                code_validation = {"valid": False, "errors": [str(pipeline_error)], "warnings": [], "score": 0.0}
                status = "❌ Pipeline execution error"
            
            # Update chat history with the response
            history[-1] = [message, response_message]
            self.chat_history = history
            
            return history, best_code, code_validation, status
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            self.logger.error(traceback.format_exc())
            error_message = f"Error: {str(e)}"
            
            if not history:
                history = []
            if len(history) > 0 and len(history[-1]) == 2 and history[-1][1] == "Generating code...":
                history[-1] = [message, error_message]
            else:
                history.append([message, error_message])
                
            return history, "", {"valid": False, "errors": [error_message], "warnings": []}, f"❌ Error: {str(e)}"
    
    def reset_chat(self) -> Tuple[List[List[str]], str, Dict[str, Any], str]:
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
                    # Left column for input
                    with gr.Column(scale=1):
                        gr.Markdown("## What would you like Reachy to do?")
                        
                        # Input area
                        msg = gr.Textbox(
                            placeholder="Example: Move the robot's right arm to wave hello...",
                            lines=4,
                            max_lines=10,
                            label="Natural Language Request"
                        )
                        
                        # Submit button in a row for better placement
                        with gr.Row():
                            submit_btn = gr.Button("Generate Code", variant="primary", scale=2)
                            clear_btn = gr.Button("Reset", variant="secondary", scale=1)
                        
                        # Status indicator
                        status_md = gr.Markdown(
                            """<div class="status-ready">Ready to generate code</div>""",
                        )
                    
                    # Right column for code and feedback
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
                        
                        # Feedback section
                        gr.Markdown("## Execution Feedback")
                        feedback = gr.Textbox(
                            value="",
                            lines=6,
                            max_lines=12,
                            label="Execution Results",
                            interactive=False,
                        )
                
                # Internal state to track chat history
                chatbot = gr.State([])
                
                # Helper functions for status updates
                def update_status(message="Processing your request...", status="processing"):
                    """Update the status indicator with a message and status type"""
                    status_classes = {
                        "ready": "status-ready",
                        "processing": "status-processing", 
                        "success": "status-success",
                        "error": "status-error"
                    }
                    css_class = status_classes.get(status, "status-ready")
                    
                    # Add an emoji based on status
                    emoji = {
                        "ready": "🔹",
                        "processing": "⏳",
                        "success": "✅",
                        "error": "❌"
                    }.get(status, "🔹")
                    
                    return f"""<div class="{css_class}">{emoji} {message}</div>"""
                
                # Function to reset the interface
                def reset_fn():
                    """Reset all fields and state"""
                    return [], update_status("Ready to generate code", "ready"), "", ""
                
                # Function to generate code (without updating feedback)
                def generate_code_fn(message, history):
                    """Process a user request and generate code only"""
                    try:
                        # Set processing status
                        status_html = update_status("Generating code for your request...", "processing")
                        
                        # Generate code
                        new_history, code, validation, _ = self.process_message(message, history)
                        
                        # Update status based on code generation success
                        if code:
                            status_html = update_status("Code generated successfully", "success")
                        else:
                            status_html = update_status("No code was generated", "error")
                            code = ""  # Ensure empty string is returned
                        
                        # Return status and code, but don't update feedback
                        return new_history, status_html, code
                        
                    except Exception as e:
                        self.logger.error(f"Error in generate_code_fn: {str(e)}")
                        self.logger.error(traceback.format_exc())
                        status_html = update_status(f"Error: {str(e)}", "error")
                        return history, status_html, ""
                
                # Function to execute code
                def execute_code_fn(code):
                    """Execute the generated code on the robot"""
                    try:
                        # Set processing status
                        status_html = update_status("Executing code on robot...", "processing")
                        
                        # Execute code
                        result = self.execute_code(code)
                        
                        # Update status based on execution success
                        if result.get("success", False):
                            status_html = update_status("Code executed successfully", "success")
                            
                            if result.get("output", "").strip():
                                feedback_text = f"✅ Execution successful\n\nOutput:\n{result['output']}"
                            else:
                                feedback_text = "✅ Execution completed successfully with no output."
                        else:
                            status_html = update_status("Execution failed", "error")
                            
                            if result.get("feedback", ""):
                                feedback_text = f"❌ Execution failed\n\n{result['feedback']}"
                            elif result.get("stderr", ""):
                                feedback_text = f"❌ Execution failed\n\nError details:\n{result['stderr']}"
                            else:
                                feedback_text = f"❌ Execution failed: {result.get('message', 'Unknown error')}"
                        
                        # Return the results
                        return status_html, feedback_text
                    except Exception as e:
                        self.logger.error(f"Error in execute_code: {str(e)}")
                        self.logger.error(traceback.format_exc())
                        status_html = update_status(f"Error: {str(e)}", "error")
                        return status_html, f"❌ Error executing code: {str(e)}"
                
                # Set up event handlers
                submit_btn.click(
                    fn=generate_code_fn,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, status_md, code_editor],
                    api_name="generate"
                )
                
                msg.submit(
                    fn=generate_code_fn,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, status_md, code_editor]
                )
                
                execute_btn.click(
                    fn=execute_code_fn,
                    inputs=[code_editor],
                    outputs=[status_md, feedback],
                    api_name="execute"
                )
                
                clear_btn.click(
                    fn=reset_fn,
                    outputs=[chatbot, status_md, code_editor, feedback],
                    api_name="reset"
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
    
    args = parser.parse_args()
    
    print(f"Starting Reachy 2 Code Generation Interface with model: gpt-4o")
    
    # Create interface with default temperature and max_tokens
    interface = CodeGenerationInterface(
        api_key=args.api_key,
        model="gpt-4o",
        temperature=0.2,      # Default temperature
        max_tokens=4000,      # Default max_tokens
        websocket_port=args.websocket_port,
    )
    
    interface.launch_interface(share=args.share, port=args.port)


if __name__ == "__main__":
    main() 