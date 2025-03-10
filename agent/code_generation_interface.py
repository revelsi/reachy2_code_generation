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

# Import the code generation agent
from agent.code_generation_agent import ReachyCodeGenerationAgent


class CodeGenerationInterface:
    """Simple Gradio interface for the Reachy 2 Code Generation Agent."""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o-mini",  # Hardcoded to gpt-4o-mini
        temperature: float = 0.2,
        max_tokens: int = 4000,
        websocket_port: int = None,
    ):
        """
        Initialize the code generation interface.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            temperature: The temperature to use for code generation.
            max_tokens: The maximum number of tokens to generate.
            websocket_port: The port to use for the WebSocket server. If None, will use the default port.
        """
        # Configure WebSocket port if provided
        if websocket_port is not None:
            # Import here to avoid circular imports
            from api.websocket import get_websocket_server
            websocket_server = get_websocket_server(port=websocket_port)
        
        # Initialize the code generation agent
        self.agent = ReachyCodeGenerationAgent(
            api_key=api_key,
            model=model,  # Always use gpt-4o-mini
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Initialize chat history
        self.chat_history = []
        
        # Store model configuration
        self.model_config = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Initialize Reachy availability
        self.reachy_available = False
    
    def process_message(self, message: str, history: List[List[str]]) -> Tuple[List[List[str]], str, Dict[str, Any], str, str]:
        """
        Process a user message and update the chat history.
        
        Args:
            message: User message.
            history: Current chat history.
            
        Returns:
            Tuple: Updated chat history, generated code, code validation, status message, and correction history.
        """
        try:
            # Add a status message to the chat
            history.append([message, "Thinking... Generating code based on your request. This may take a moment."])
            self.chat_history = history
            
            # Process the message with recursive correction
            response_data = self.agent.process_message(message, max_correction_attempts=3)
            
            # Extract the message from the response
            response_message = response_data.get("message", "")
            if response_data.get("error"):
                response_message = f"Error: {response_data.get('error')}"
            
            # Update chat history with the actual response
            history[-1] = [message, response_message]
            self.chat_history = history
            
            # Get generated code and validation
            generated_code = response_data.get("code", "")
            code_validation = response_data.get("validation", {})
            
            # Check if code was corrected
            correction_count = response_data.get("correction_count", 0)
            correction_info = ""
            if correction_count > 0:
                correction_info = f" (Automatically corrected {correction_count} time{'s' if correction_count > 1 else ''})"
            
            # Create a status message
            status = f"✅ Code generated successfully{correction_info}."
            if not generated_code:
                status = "❌ No code was generated. Please try again with a different request."
            elif not code_validation.get("valid", False):
                status = f"⚠️ Code generated with validation issues{correction_info}. Check the validation results."
            
            # Create correction history
            correction_history = ""
            corrections = response_data.get("corrections", [])
            if corrections:
                correction_history = "### Code Correction History\n\n"
                for i, correction in enumerate(corrections):
                    correction_history += f"**Correction {i+1}:**\n"
                    issues = correction.get('issues', [])
                    fixed = correction.get('fixed', False)
                    correction_history += f"- Issues: {', '.join(issues)}\n"
                    correction_history += f"- Fixed: {fixed}\n"
                    if fixed:
                        correction_history += "- ✅ The model successfully fixed these issues\n\n"
                    else:
                        correction_history += "- ❌ The model was unable to fix these issues\n\n"
                
                # Add explanation of validation process
                correction_history += "### Validation Process\n\n"
                correction_history += "The code goes through these validation steps:\n"
                correction_history += "1. **Syntax Check**: Ensures the code has valid Python syntax\n"
                correction_history += "2. **Import Validation**: Verifies all imports are available\n"
                correction_history += "3. **API Usage Check**: Confirms correct usage of the Reachy API\n"
                correction_history += "4. **Safety Check**: Looks for potentially harmful operations\n\n"
                correction_history += "When issues are found, the model attempts to fix them automatically."
            
            return history, generated_code, code_validation, status, correction_history
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_message = f"An error occurred: {str(e)}"
            history.append([message, error_message])
            return history, "", {"valid": False, "errors": [error_message], "warnings": []}, "❌ Error occurred during processing", ""
    
    def reset_chat(self) -> Tuple[List[List[str]], str, Dict[str, Any], str, str]:
        """
        Reset the chat history.
        
        Returns:
            Tuple: Empty chat history, empty code, empty validation, status message, and empty correction history.
        """
        self.chat_history = []
        self.agent.reset_conversation()
        return [], "", {"valid": False, "errors": [], "warnings": []}, "Chat reset. Ready for new requests.", ""
    
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
        self.agent = ReachyCodeGenerationAgent(
            model="gpt-4o-mini",  # Always use gpt-4o-mini
            temperature=temperature,
            max_tokens=max_tokens
        )
        
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
            except:
                reachy_available = False
            
            if not reachy_available:
                return {
                    "success": False,
                    "message": "Reachy robot is not available. Please make sure the robot or simulator is running.",
                    "output": "Cannot execute code because the Reachy robot or simulator is not running or not accessible.",
                    "stderr": "Connection to Reachy robot failed. The robot or simulator must be running on localhost:50051.",
                    "status": "❌ Robot connection failed"
                }
            
            # Execute the code
            result = self.agent.execute_code(code, confirm=False)
            
            # Add a status message
            if result.get("success", False):
                result["status"] = "✅ Code executed successfully"
            else:
                result["status"] = "❌ Code execution failed"
            
            return result
        except Exception as e:
            logger.error(f"Error executing code: {e}")
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "result": None,
                "status": "❌ Error during execution"
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
            
            **Features:**
            - Automatic code validation
            - Recursive code correction (fixes issues automatically)
            - Code execution with detailed feedback
            
            **Model: GPT-4o-mini** - Optimized for code generation with the Reachy 2 robot
            """)
            
            # Reachy status
            with gr.Row():
                reachy_status_md = gr.Markdown(self.check_reachy_status())
                refresh_btn = gr.Button("Refresh Reachy Status", variant="secondary", scale=0)
            
            # Process status indicator
            process_status = gr.Markdown("### Status: Ready")
            
            # Model configuration
            with gr.Group():
                gr.Markdown("### Generation Parameters")
                with gr.Row():
                    temperature_slider = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=self.model_config.get("temperature", 0.2),
                        step=0.1,
                        label="Temperature",
                        info="Higher values make output more random, lower values more deterministic"
                    )
                    max_tokens_slider = gr.Slider(
                        minimum=1000,
                        maximum=8000,
                        value=self.model_config.get("max_tokens", 4000),
                        step=500,
                        label="Max Tokens",
                        info="Maximum number of tokens to generate"
                    )
                
                update_model_btn = gr.Button("Update Parameters", variant="secondary")
            
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
                    
                    When code is generated, it goes through these validation steps:
                    1. **Syntax Check**: Ensures the code has valid Python syntax
                    2. **Import Validation**: Verifies all imports are available
                    3. **API Usage Check**: Confirms correct usage of the Reachy API
                    4. **Safety Check**: Looks for potentially harmful operations
                    
                    Issues found during validation will be shown below:
                    """)
                    
                    validation_json = gr.JSON(
                        value={},
                        label="Validation Results",
                    )
                    
                    # Correction history
                    correction_history_md = gr.Markdown("")
                    
                    # Execution status
                    execution_status = gr.Markdown("No code executed yet.")
                    
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
            
            # Model configuration output
            model_config_json = gr.JSON(
                value=self.model_config,
                label="Current Model Configuration",
                visible=False
            )
            
            # Set up event handlers
            
            # Update model configuration
            update_model_btn.click(
                fn=lambda: "### Status: Updating generation parameters...",
                outputs=[process_status],
            ).then(
                fn=self.update_model_config,
                inputs=[temperature_slider, max_tokens_slider],
                outputs=[model_config_json],
            ).then(
                fn=lambda: "### Status: Generation parameters updated",
                outputs=[process_status],
            ).then(
                fn=lambda: "Generation parameters updated successfully.",
                outputs=[status_msg],
            )
            
            # Generate code
            def update_process_status(step):
                return f"### Status: {step}"
            
            # Define the code generation pipeline with detailed status updates
            submit_btn.click(
                fn=lambda: update_process_status("Starting code generation..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Generating code based on your request. This may take a moment...",
                outputs=[status_msg],
            ).then(
                fn=lambda: update_process_status("Analyzing request..."),
                outputs=[process_status],
            ).then(
                fn=lambda: time.sleep(1) or update_process_status("Generating code..."),
                outputs=[process_status],
            ).then(
                fn=lambda: update_process_status("Validating code (syntax, imports, API usage, safety)..."),
                outputs=[process_status],
            ).then(
                fn=lambda: time.sleep(1) or update_process_status("Applying automatic corrections if needed..."),
                outputs=[process_status],
            ).then(
                fn=self.process_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, code_editor, validation_json, status_msg, correction_history_md],
            ).then(
                fn=lambda: update_process_status("Code generation complete"),
                outputs=[process_status],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            # Same for message submission
            msg.submit(
                fn=lambda: update_process_status("Starting code generation..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Generating code based on your request. This may take a moment...",
                outputs=[status_msg],
            ).then(
                fn=lambda: update_process_status("Analyzing request..."),
                outputs=[process_status],
            ).then(
                fn=lambda: time.sleep(1) or update_process_status("Generating code..."),
                outputs=[process_status],
            ).then(
                fn=lambda: update_process_status("Validating code (syntax, imports, API usage, safety)..."),
                outputs=[process_status],
            ).then(
                fn=lambda: time.sleep(1) or update_process_status("Applying automatic corrections if needed..."),
                outputs=[process_status],
            ).then(
                fn=self.process_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, code_editor, validation_json, status_msg, correction_history_md],
            ).then(
                fn=lambda: update_process_status("Code generation complete"),
                outputs=[process_status],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            # Reset chat
            reset_btn.click(
                fn=lambda: update_process_status("Resetting chat..."),
                outputs=[process_status],
            ).then(
                fn=self.reset_chat,
                outputs=[chatbot, code_editor, validation_json, status_msg, correction_history_md],
            ).then(
                fn=lambda: update_process_status("Ready"),
                outputs=[process_status],
            )
            
            # Define a function to extract feedback from execution result
            def extract_feedback(result):
                feedback = result.get("feedback", "")
                if not feedback and not result.get("success", True):
                    # If no feedback but execution failed, provide a basic message
                    feedback = "Execution failed. Check the execution result for details."
                return feedback
            
            # Define a function to extract status from execution result
            def extract_status(result):
                return result.get("status", "Code execution completed.")
            
            # Execute code
            execute_btn.click(
                fn=lambda: update_process_status("Executing code..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Executing code. This may take a moment...",
                outputs=[execution_status],
            ).then(
                fn=self.execute_code,
                inputs=[code_editor],
                outputs=[execution_result],
            ).then(
                fn=extract_feedback,
                inputs=[execution_result],
                outputs=[execution_feedback],
            ).then(
                fn=extract_status,
                inputs=[execution_result],
                outputs=[execution_status],
            ).then(
                fn=lambda: update_process_status("Code execution complete"),
                outputs=[process_status],
            )
            
            # Refresh robot status
            refresh_btn.click(
                fn=lambda: update_process_status("Checking robot connection..."),
                outputs=[process_status],
            ).then(
                fn=lambda: "Checking robot connection...",
                outputs=[status_msg],
            ).then(
                fn=self.check_reachy_status,
                outputs=[reachy_status_md],
            ).then(
                fn=lambda: "Robot status updated.",
                outputs=[status_msg],
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
    parser.add_argument("--temperature", type=float, default=0.2, help="Model temperature (0.0 to 1.0)")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Maximum tokens to generate")
    parser.add_argument("--share", action="store_true", help="Create a public link")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--websocket-port", type=int, help="Port for the WebSocket server (default is 8765)")
    
    args = parser.parse_args()
    
    print(f"Starting Reachy 2 Code Generation Interface with model: gpt-4o-mini")
    
    # Create interface
    interface = CodeGenerationInterface(
        api_key=args.api_key,
        model="gpt-4o-mini",  # Always use gpt-4o-mini
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        websocket_port=args.websocket_port,
    )
    
    interface.launch_interface(share=args.share, port=args.port)


if __name__ == "__main__":
    main() 