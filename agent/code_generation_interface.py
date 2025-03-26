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
from typing import Dict, List, Any, Tuple
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
from config import OPENAI_API_KEY, MODEL, AVAILABLE_MODELS, get_model_config

# Import Gradio
import gradio as gr

# Import the OpenAI client
from openai import OpenAI


class CodeGenerationInterface:
    """Interface for code generation using OpenAI API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        websocket_port: int = None
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
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.websocket_port = websocket_port
        
        # Initialize chat history
        self.chat_history = []
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        logger.debug(f"Initialized code generation interface with model: {model}")

    def generate_code(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generate code using the OpenAI API.

        Args:
            system_prompt: The system prompt to use.
            user_prompt: The user prompt to use.

        Returns:
            Dict[str, Any]: The response from the API, including generated code.
        """
        try:
            logger.debug(f"Generating code with model: {self.model}")
            
            # Create messages for the API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty
            )
            
            # Extract code and explanation from the response
            content = response.choices[0].message.content
            code, explanation = self._extract_code_and_explanation(content)
            
            # Prepare the response
            result = {
                "message": explanation,
                "code": code,
                "raw_response": content
            }
            
            logger.debug("Code generation successful")
            return result
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            logger.error(traceback.format_exc())
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
            # Add a status message to the chat
            history.append([message, "Generating code..."])
            self.chat_history = history
            
            # Import the agent here to avoid circular imports
            from agent.code_generation_agent import ReachyCodeGenerationAgent
            
            # Create a temporary agent to get the system prompt
            # We only need the system prompt, not the full agent functionality
            temp_agent = ReachyCodeGenerationAgent(
                api_key=self.client.api_key,
                model=self.model
            )
            
            # Get the system prompt from the agent
            system_prompt = temp_agent._build_system_prompt()
            
            # Process the message
            response_data = self.generate_code(system_prompt=system_prompt, user_prompt=message)
            
            # Extract the message from the response
            response_message = response_data.get("message", "")
            if response_data.get("error"):
                response_message = f"Error: {response_data.get('error')}"
            else:
                # Make the response more concise - focus on the code
                response_message = "Code generated based on your request."
            
            # Update chat history with the actual response
            history[-1] = [message, response_message]
            self.chat_history = history
            
            # Get generated code and validation
            generated_code = response_data.get("code", "")
            code_validation = response_data.get("validation", {})
            
            # Create a status message
            status = "✅ Code generated"
            if not generated_code:
                status = "❌ No code generated. Try a different request."
            elif not code_validation.get("valid", False):
                status = "⚠️ Code has validation issues"
            
            return history, generated_code, code_validation, status
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_message = f"Error: {str(e)}"
            history.append([message, error_message])
            return history, "", {"valid": False, "errors": [error_message], "warnings": []}, "❌ Error occurred"
    
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
            "model": "gpt-4o-mini",  # Always use gpt-4o-mini
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Reinitialize the agent with the new configuration
        # self.agent = ReachyCodeGenerationAgent(
        #     model="gpt-4o-mini",  # Always use gpt-4o-mini
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
        try:
            # Store the code being executed
            self.last_executed_code = code
            
            # Log the code being executed
            logger.info(f"Executing code:\n{code}")
            
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
            except Exception as e:
                logger.error(f"Error checking Reachy availability: {e}")
                reachy_available = False
            
            if not reachy_available:
                return {
                    "success": False,
                    "error": "Reachy robot is not available",
                    "output": "Cannot execute code because the Reachy robot or simulator is not running or not accessible.",
                    "status": "❌ Robot connection failed",
                    "feedback": "Please ensure that:\n1. The Reachy robot or simulator is running\n2. The gRPC server is accessible on port 50051\n3. There are no network connectivity issues"
                }
            
            # Import the agent here to avoid circular imports
            from agent.code_generation_agent import ReachyCodeGenerationAgent
            
            try:
                # Create a temporary agent to execute the code
                temp_agent = ReachyCodeGenerationAgent(
                    api_key=self.client.api_key,
                    model=self.model
                )
                
                # Execute the code using the agent's execute_code method
                # Set confirm=False since we're executing directly, and force=True to bypass validation
                result = temp_agent.execute_code(code, confirm=False, force=True)
                
                # Ensure the result has all required fields
                if not isinstance(result, dict):
                    raise ValueError("Agent returned invalid result format")
                
                # Add a status message if not already present
                if "status" not in result:
                    if result.get("success", False):
                        result["status"] = "✅ Code executed successfully"
                    else:
                        error = result.get("error", "Unknown error")
                        result["status"] = f"❌ Code execution failed: {error}"
                
                return result
                
            except Exception as agent_error:
                logger.error(f"Error in agent execution: {agent_error}")
                logger.error(traceback.format_exc())
                return {
                    "success": False,
                    "error": str(agent_error),
                    "output": "",
                    "status": "❌ Agent execution error",
                    "feedback": f"The code execution agent encountered an error:\n{str(agent_error)}\n\nThis might be due to:\n1. Invalid code syntax\n2. Missing dependencies\n3. System resource issues"
                }
                
        except Exception as e:
            logger.error(f"Error in execute_code: {e}")
            logger.error(traceback.format_exc())
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "status": "❌ System error",
                "feedback": f"A system error occurred:\n{str(e)}\n\nThis is likely a bug in the interface. Please report this issue."
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
        """
        Launch the Gradio interface.
        
        Args:
            share: Whether to create a public link.
            port: The port to run the server on.
        """
        # Create the interface
        with gr.Blocks(title="Reachy 2 Code Generation") as interface:
            gr.Markdown("# Reachy 2 Code Generation")
            gr.Markdown("""
            This interface allows you to generate Python code for the Reachy 2 robot using natural language.
            Simply describe what you want the robot to do, and the agent will generate the appropriate code.
            """)
            
            # Reachy status
            with gr.Row():
                reachy_status_md = gr.Markdown(self.check_reachy_status())
                refresh_btn = gr.Button("Refresh Reachy Status", variant="secondary", scale=0)
            
            # Process status indicator
            process_status = gr.Markdown("### Status: Ready")
            
            with gr.Row():
                with gr.Column(scale=3):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        value=self.chat_history,
                        show_copy_button=True,
                    )
                    
                    # Message input
                    msg = gr.Textbox(
                        placeholder="Describe what you want the robot to do...",
                        container=False,
                        scale=7,
                    )
                    
                    # Status message
                    status_msg = gr.Markdown("Ready for your request.")
                    
                    # Buttons
                    with gr.Row():
                        submit_btn = gr.Button("Generate Code", variant="primary", scale=1)
                        reset_btn = gr.Button("Reset Chat", variant="secondary", scale=1)
                
                with gr.Column(scale=2):
                    # Code Generation UI
                    gr.Markdown("### Generated Code")
                    code_editor = gr.Code(
                        value="",
                        language="python",
                        label="Generated Code",
                        interactive=True,
                    )
                    
                    # Validation explanation
                    validation_explanation = gr.Markdown("""
                    ### Code Validation
                    
                    Validation: **Syntax** | **Imports** | **API Usage** | **Safety**
                    """)
                    
                    validation_json = gr.JSON(
                        value={},
                        label="Validation Results",
                    )
                    
                    # Execution status
                    execution_status = gr.Markdown("No code executed yet.")
                    
                    # Execution buttons
                    with gr.Row():
                        execute_btn = gr.Button("Execute Code", variant="primary")
                    
                    execution_result = gr.JSON(
                        value={},
                        label="Execution Result",
                        visible=False,  # Hide the raw JSON by default
                    )
                    
                    # Add a text area for feedback
                    execution_feedback = gr.Textbox(
                        value="",
                        label="Execution Feedback",
                        interactive=False,
                        lines=5,
                    )
            
            # Set up event handlers
            
            # Generate code
            def update_process_status(step):
                return f"### Status: {step}"
            
            # Generate code
            submit_btn.click(
                fn=lambda: update_process_status("Generating..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Working on it...",
                outputs=[status_msg],
            ).then(
                fn=self.process_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, code_editor, validation_json, status_msg],
            ).then(
                fn=lambda: update_process_status("Complete"),
                outputs=[process_status],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            # Same for message submission
            msg.submit(
                fn=lambda: update_process_status("Generating..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Working on it...",
                outputs=[status_msg],
            ).then(
                fn=self.process_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, code_editor, validation_json, status_msg],
            ).then(
                fn=lambda: update_process_status("Complete"),
                outputs=[process_status],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            # Reset chat
            reset_btn.click(
                fn=lambda: update_process_status("Resetting..."),
                outputs=[process_status],
            ).then(
                fn=self.reset_chat,
                outputs=[chatbot, code_editor, validation_json, status_msg],
            ).then(
                fn=lambda: "",
                outputs=[execution_status],
            ).then(
                fn=lambda: "",
                outputs=[execution_feedback],
            ).then(
                fn=lambda: {},
                outputs=[execution_result],
            ).then(
                fn=lambda: update_process_status("Ready"),
                outputs=[process_status],
            )
            
            # Define a function to extract status from execution result
            def extract_status(result):
                # Use the status if provided, otherwise determine from success
                if "status" in result:
                    return result["status"]
                elif result.get("success", False):
                    return "✅ Code executed successfully"
                else:
                    error_msg = result.get("error", "Unknown error")
                    return f"❌ Code execution failed: {error_msg}"
            
            # Define a function to extract feedback from execution result
            def extract_feedback(result):
                feedback = ""
                
                # If execution failed, provide error details
                if not result.get("success", True):
                    error = result.get("error", "")
                    stderr = result.get("stderr", "")
                    output = result.get("output", "")
                    feedback_msg = result.get("feedback", "")
                    message = result.get("message", "")
                    
                    # Build feedback in order of importance
                    if feedback_msg:  # Specific feedback from error analysis
                        feedback += f"{feedback_msg}\n\n"
                    
                    if message and message not in feedback:  # General error message
                        feedback += f"{message}\n\n"
                    
                    if error and error not in feedback:  # Technical error
                        feedback += f"Error: {error}\n\n"
                    
                    if stderr:  # Stack trace or system errors
                        feedback += f"Details:\n{stderr}\n\n"
                    
                    if output and output not in feedback:  # Program output
                        feedback += f"Output:\n{output}\n\n"
                    
                    if not feedback:
                        feedback = "Execution failed. No additional error information available."
                
                # If execution succeeded, provide output or success message
                else:
                    output = result.get("output", "").strip()
                    if output:
                        feedback = f"Execution successful!\n\nOutput:\n{output}"
                    else:
                        feedback = "Execution successful! (No output)"
                
                return feedback.strip()  # Remove any trailing whitespace
            
            # Execute code
            execute_btn.click(
                fn=lambda: update_process_status("Executing..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Preparing to execute code...",
                outputs=[execution_status],
            ).then(
                fn=lambda: "",  # Clear previous feedback
                outputs=[execution_feedback],
            ).then(
                fn=self.execute_code,
                inputs=[code_editor],
                outputs=[execution_result],
            ).then(
                fn=extract_status,
                inputs=[execution_result],
                outputs=[execution_status],
            ).then(
                fn=extract_feedback,
                inputs=[execution_result],
                outputs=[execution_feedback],
            ).then(
                fn=lambda: update_process_status("Ready"),
                outputs=[process_status],
            )
            
            # Refresh robot status
            refresh_btn.click(
                fn=lambda: update_process_status("Checking connection..."),
                outputs=[process_status],
            ).then(
                fn=self.check_reachy_status,
                outputs=[reachy_status_md],
            ).then(
                fn=lambda: update_process_status("Ready"),
                outputs=[process_status],
            )
        
        # Launch the interface
        interface.launch(share=share, server_port=port)


def main():
    """Main entry point for the code generation interface."""
    parser = argparse.ArgumentParser(description="Reachy 2 Code Generation Interface")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--share", action="store_true", help="Create a public link")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--websocket-port", type=int, help="Port for the WebSocket server (default is 8765)")
    
    args = parser.parse_args()
    
    print(f"Starting Reachy 2 Code Generation Interface with model: gpt-4o-mini")
    
    # Create interface with default temperature and max_tokens
    interface = CodeGenerationInterface(
        api_key=args.api_key,
        model="gpt-4o-mini",  # Always use gpt-4o-mini
        temperature=0.2,      # Default temperature
        max_tokens=4000,      # Default max_tokens
        websocket_port=args.websocket_port,
    )
    
    interface.launch_interface(share=args.share, port=args.port)


if __name__ == "__main__":
    main() 