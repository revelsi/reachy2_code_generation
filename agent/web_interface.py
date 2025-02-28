#!/usr/bin/env python
import os
import sys
import json
import argparse
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

import gradio as gr

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from agent.agent_router import AgentRouter, AgentMode
from agent.cli import setup_agent, DEFAULT_MODULES
from config import (
    OPENAI_API_KEY, MODEL, DEBUG, DISABLE_WEBSOCKET, 
    get_model_config, update_model_config, AVAILABLE_MODELS
)

# Configure OpenAI client with custom settings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", OPENAI_API_KEY),
    timeout=30.0,  # Increase timeout
    max_retries=2  # Add retries
)

# Log API key presence (not the actual key)
logger.debug(f"OpenAI API key is {'set' if os.getenv('OPENAI_API_KEY') else 'not set'}")

class AgentInterface:
    """Web interface for the Reachy 2 Agent using Gradio."""
    
    def __init__(
        self,
        api_key: str = None,
        model_config: Dict[str, Any] = None,
        focus_modules: List[str] = None,
        regenerate_tools: bool = False,
    ):
        """
        Initialize the agent interface.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            model_config: Model configuration. If None, will use the configuration from config.py.
            focus_modules: Optional list of module names to focus on (default: parts, orbita, utils).
            regenerate_tools: Whether to regenerate tool definitions and implementations.
        """
        # Use model configuration from config.py if not provided
        if model_config is None:
            model_config = get_model_config()
            
        # Initialize the agent router
        self.agent_router = AgentRouter(
            api_key=api_key,
            model_config=model_config,
            focus_modules=focus_modules,
            regenerate_tools=regenerate_tools,
            default_mode=AgentMode.FUNCTION_CALLING
        )
        
        # Initialize chat history
        self.chat_history = []
        
        # Track tool calls for visualization
        self.tool_calls = []
        
        # Track generated code
        self.generated_code = ""
        self.code_validation = {}
        
        # Store model configuration
        self.model_config = model_config
    
    def process_message(self, message: str, history: List[List[str]], mode: str) -> Tuple[List[List[str]], List[Dict[str, Any]], str, Dict[str, Any]]:
        """
        Process a user message and update the chat history.
        
        Args:
            message: User message.
            history: Current chat history.
            mode: Agent mode (function_calling or code_generation).
            
        Returns:
            Tuple: Updated chat history, tool calls, generated code, and code validation.
        """
        # Set the agent mode
        self.agent_router.set_mode(AgentMode(mode))
        
        # Process the message
        response_data = self.agent_router.process_message(message)
        
        # Extract the message from the response
        response_message = response_data.get("message", "")
        if response_data.get("error"):
            response_message = f"Error: {response_data.get('error')}"
        
        # Update chat history
        history.append([message, response_message])
        self.chat_history = history
        
        # Handle mode-specific data
        if mode == AgentMode.FUNCTION_CALLING:
            # Get tool calls from the response
            self.tool_calls = response_data.get("tool_calls", [])
            self.generated_code = ""
            self.code_validation = {}
        else:  # code_generation mode
            # Get generated code and validation
            self.tool_calls = []
            self.generated_code = response_data.get("code", "")
            self.code_validation = response_data.get("validation", {})
        
        return history, self.tool_calls, self.generated_code, self.code_validation
    
    def reset_chat(self) -> Tuple[List[List[str]], List[Dict[str, Any]], str, Dict[str, Any]]:
        """
        Reset the chat history and agent state.
        
        Returns:
            Tuple: Empty chat history, tool calls, generated code, and code validation.
        """
        self.agent_router.reset_conversation()
        self.chat_history = []
        self.tool_calls = []
        self.generated_code = ""
        self.code_validation = {}
        return [], [], "", {}
    
    def update_model_config(self, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """
        Update the model configuration.
        
        Args:
            model: The model name.
            temperature: The temperature value.
            max_tokens: The maximum number of tokens.
            
        Returns:
            Dict[str, Any]: The updated model configuration.
        """
        # Create new configuration
        new_config = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Update the agent router
        self.agent_router.update_model_config(new_config)
        
        # Update local configuration
        self.model_config = self.agent_router.get_model_config()
        
        return self.model_config
    
    def launch_interface(self, share: bool = False):
        """
        Launch the Gradio interface.
        
        Args:
            share: Whether to create a public link.
        """
        # Create the chat interface
        with gr.Blocks(title="Reachy 2 Agent") as interface:
            gr.Markdown("# Reachy 2 Agent")
            gr.Markdown("""
            This interface allows you to control the Reachy 2 robot using natural language.
            Choose between Function Calling mode (direct control) or Code Generation mode (generates Python code).
            """)
            
            # Mode selection
            with gr.Row():
                mode = gr.Radio(
                    choices=[AgentMode.FUNCTION_CALLING, AgentMode.CODE_GENERATION],
                    value=AgentMode.FUNCTION_CALLING,
                    label="Agent Mode",
                    info="Select the agent mode"
                )
                
                # Model configuration
                with gr.Group():
                    gr.Markdown("### Model Configuration")
                    with gr.Row():
                        model_dropdown = gr.Dropdown(
                            choices=AVAILABLE_MODELS,
                            value=self.model_config.get("model", MODEL),
                            label="Model",
                            info="Select the LLM model"
                        )
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
                    
                    update_model_btn = gr.Button("Update Model Configuration", variant="secondary")
            
            with gr.Row():
                with gr.Column(scale=3):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        value=self.chat_history,
                        height=500,
                        show_copy_button=True,
                    )
                    
                    # Message input
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        container=False,
                        scale=7,
                    )
                    
                    # Buttons
                    with gr.Row():
                        submit_btn = gr.Button("Send", variant="primary", scale=1)
                        reset_btn = gr.Button("Reset Chat", variant="secondary", scale=1)
                
                with gr.Column(scale=2):
                    # Function Calling Mode UI
                    with gr.Group(visible=True) as function_calling_ui:
                        gr.Markdown("### Tool Calls")
                        tool_calls_json = gr.JSON(
                            value=self.tool_calls,
                            label="Tool Calls",
                        )
                    
                    # Code Generation Mode UI
                    with gr.Group(visible=False) as code_generation_ui:
                        gr.Markdown("### Generated Code")
                        code_editor = gr.Code(
                            value=self.generated_code,
                            language="python",
                            label="Generated Code",
                            interactive=True,
                        )
                        validation_json = gr.JSON(
                            value=self.code_validation,
                            label="Code Validation",
                        )
                        execute_btn = gr.Button("Execute Code", variant="primary")
            
            # Model configuration output
            model_config_json = gr.JSON(
                value=self.model_config,
                label="Current Model Configuration",
                visible=False
            )
            
            # Set up event handlers
            def update_ui_visibility(mode_value):
                if mode_value == AgentMode.FUNCTION_CALLING:
                    return gr.update(visible=True), gr.update(visible=False)
                else:
                    return gr.update(visible=False), gr.update(visible=True)
            
            mode.change(
                fn=update_ui_visibility,
                inputs=[mode],
                outputs=[function_calling_ui, code_generation_ui],
            )
            
            update_model_btn.click(
                fn=self.update_model_config,
                inputs=[model_dropdown, temperature_slider, max_tokens_slider],
                outputs=[model_config_json],
            ).then(
                fn=lambda: gr.update(visible=True),
                outputs=[model_config_json],
            )
            
            submit_btn.click(
                fn=self.process_message,
                inputs=[msg, chatbot, mode],
                outputs=[chatbot, tool_calls_json, code_editor, validation_json],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            msg.submit(
                fn=self.process_message,
                inputs=[msg, chatbot, mode],
                outputs=[chatbot, tool_calls_json, code_editor, validation_json],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            reset_btn.click(
                fn=self.reset_chat,
                outputs=[chatbot, tool_calls_json, code_editor, validation_json],
            )
            
            # TODO: Implement code execution functionality
            execute_btn.click(
                fn=lambda x: f"Code execution not yet implemented. Code: {x[:100]}...",
                inputs=[code_editor],
                outputs=[gr.Textbox(label="Execution Result")],
            )
        
        # Launch the interface
        interface.launch(share=share)


def main():
    """Main entry point for the web interface."""
    parser = argparse.ArgumentParser(description="Reachy 2 Agent Web Interface")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--model", choices=AVAILABLE_MODELS, default=MODEL, help="LLM model to use")
    parser.add_argument("--temperature", type=float, default=0.2, help="Model temperature (0.0 to 1.0)")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Maximum tokens to generate")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions and implementations")
    parser.add_argument("--focus", nargs="+", default=DEFAULT_MODULES, help="Focus on specific modules")
    parser.add_argument("--share", action="store_true", help="Create a public link")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--mode", choices=[AgentMode.FUNCTION_CALLING, AgentMode.CODE_GENERATION], 
                        default=AgentMode.FUNCTION_CALLING, help="Initial agent mode")
    
    args = parser.parse_args()
    
    # Create model configuration
    model_config = {
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    
    print(f"Starting Reachy 2 Agent Web Interface with model: {args.model}")
    
    # Create interface
    interface = AgentInterface(
        api_key=args.api_key,
        model_config=model_config,
        focus_modules=args.focus,
        regenerate_tools=args.regenerate,
    )
    
    interface.launch_interface(share=args.share)


if __name__ == "__main__":
    main() 