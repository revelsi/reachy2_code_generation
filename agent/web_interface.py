#!/usr/bin/env python
import os
import sys
import json
import argparse
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import gradio as gr

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from agent.langgraph_agent import ReachyLangGraphAgent
from agent.cli import setup_agent, DEFAULT_MODULES


class AgentInterface:
    """Web interface for the Reachy 2 Agent using Gradio."""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        focus_modules: List[str] = None,
        regenerate_tools: bool = False,
    ):
        """
        Initialize the agent interface.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            model: LLM model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
            focus_modules: Optional list of module names to focus on (default: parts, orbita, utils).
            regenerate_tools: Whether to regenerate tool definitions and implementations.
        """
        # Use model from environment variable if not provided
        if model is None:
            model = os.environ.get("MODEL", "gpt-4-turbo")
            
        self.agent = setup_agent(
            api_key=api_key,
            model=model,
            focus_modules=focus_modules,
            regenerate_tools=regenerate_tools,
        )
        
        # Initialize chat history
        self.chat_history = []
        
        # Track tool calls for visualization
        self.tool_calls = []
    
    def process_message(self, message: str, history: List[List[str]]) -> Tuple[List[List[str]], List[Dict[str, Any]]]:
        """
        Process a user message and update the chat history.
        
        Args:
            message: User message.
            history: Current chat history.
            
        Returns:
            Tuple[List[List[str]], List[Dict[str, Any]]]: Updated chat history and tool calls.
        """
        # Process the message
        response = self.agent.process_message(message)
        
        # Update chat history
        history.append([message, response])
        self.chat_history = history
        
        # Get tool calls from the agent
        tool_calls = []
        for msg in self.agent.state.messages:
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    # Find the corresponding result if available
                    result = None
                    for tool_result in self.agent.state.tool_results:
                        if tool_result.tool_call_id == tool_call.get("id"):
                            result = tool_result.result
                            break
                    
                    # Add to tool calls
                    tool_calls.append({
                        "name": tool_call.get("function", {}).get("name", "unknown"),
                        "arguments": tool_call.get("function", {}).get("arguments", {}),
                        "result": result
                    })
        
        self.tool_calls = tool_calls
        
        return history, tool_calls
    
    def reset_chat(self) -> Tuple[List[List[str]], List[Dict[str, Any]]]:
        """
        Reset the chat history and agent state.
        
        Returns:
            Tuple[List[List[str]], List[Dict[str, Any]]]: Empty chat history and tool calls.
        """
        self.agent.reset()
        self.chat_history = []
        self.tool_calls = []
        return [], []
    
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
            Type your commands in the chat box below.
            """)
            
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
                    # Tool calls visualization
                    gr.Markdown("### Tool Calls")
                    tool_calls_json = gr.JSON(
                        value=self.tool_calls,
                        label="Tool Calls",
                        height=500,
                    )
            
            # Set up event handlers
            submit_btn.click(
                fn=self.process_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, tool_calls_json],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            msg.submit(
                fn=self.process_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, tool_calls_json],
            ).then(
                fn=lambda: "",
                outputs=[msg],
            )
            
            reset_btn.click(
                fn=self.reset_chat,
                outputs=[chatbot, tool_calls_json],
            )
        
        # Launch the interface
        interface.launch(share=share)


def main():
    """Main entry point for the web interface."""
    parser = argparse.ArgumentParser(description="Reachy 2 Agent Web Interface")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--model", default=os.environ.get("MODEL", "gpt-4-turbo"), help="LLM model to use")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions and implementations")
    parser.add_argument("--focus", nargs="+", default=DEFAULT_MODULES, help="Focus on specific modules")
    parser.add_argument("--share", action="store_true", help="Create a public link")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    
    args = parser.parse_args()
    
    print(f"Starting Reachy 2 Agent Web Interface with model: {args.model}")
    
    # Create interface
    interface = AgentInterface(
        api_key=args.api_key,
        model=args.model,
        focus_modules=args.focus,
        regenerate_tools=args.regenerate,
    )
    
    interface.launch_interface(share=args.share)


if __name__ == "__main__":
    main() 