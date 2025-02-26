#!/usr/bin/env python
"""
Command-line interface for the Reachy 2 robot agent.

This module provides a CLI for interacting with the Reachy 2 robot agent.
"""

import argparse
import os
import sys
from typing import Optional, List

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration and agent
from config import OPENAI_API_KEY, MODEL, DEBUG, DISABLE_WEBSOCKET
from langgraph_agent import ReachyLangGraphAgent

# Define DEFAULT_MODULES to resolve import issues in api/app.py
DEFAULT_MODULES = []

def setup_agent(
    api_key: str = None,
    model: str = None,
    focus_modules: List[str] = None,
    regenerate_tools: bool = False,
) -> ReachyLangGraphAgent:
    """
    Set up the Reachy 2 agent.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
        model: LLM model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
        focus_modules: Optional list of module names to focus on (default: parts, orbita, utils).
        regenerate_tools: Whether to regenerate tool definitions and implementations.
        
    Returns:
        ReachyLangGraphAgent: The configured agent.
    """
    # Use model from environment variable if not provided
    if model is None:
        model = os.environ.get("MODEL", "gpt-4-turbo")
    
    # Use API key from environment variable if not provided
    if api_key is None:
        api_key = OPENAI_API_KEY
    
    # Use default modules if focus_modules is None
    if focus_modules is None:
        focus_modules = DEFAULT_MODULES
    
    # Create agent
    agent = ReachyLangGraphAgent(
        model=model
    )
    
    # Tools are loaded automatically in the agent's __init__ method
    print(f"Reachy 2 Agent ready with {len(agent.tools)} tools")
    print(f"Using model: {model}")
    
    return agent


def main():
    """Run the Reachy agent CLI."""
    parser = argparse.ArgumentParser(description="Reachy 2 Agent CLI")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--model", default=MODEL, help="LLM model to use")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions and implementations")
    parser.add_argument("--focus", nargs="+", default=DEFAULT_MODULES, help="Focus on specific modules")
    parser.add_argument("--disable-websocket", action="store_true", default=DISABLE_WEBSOCKET, help="Disable WebSocket server")
    parser.add_argument("--debug", action="store_true", default=DEBUG, help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Set environment variables based on arguments
    if args.disable_websocket:
        os.environ["DISABLE_WEBSOCKET"] = "1"
    
    if args.debug:
        os.environ["DEBUG"] = "1"
    
    print(f"Starting Reachy 2 Agent CLI with model: {args.model}")
    
    # Create agent
    agent = setup_agent(
        api_key=args.api_key,
        model=args.model,
        focus_modules=args.focus,
        regenerate_tools=args.regenerate,
    )
    
    print("Type 'exit' or 'quit' to exit")
    print("Type 'reset' to reset the conversation")
    print()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                break
                
            # Check for reset command
            if user_input.lower() == "reset":
                agent.reset_conversation()
                print("Conversation reset")
                continue
            
            # Process message
            response = agent.process_message(user_input)
            
            # Print response
            print(f"Agent: {response}")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye!")


if __name__ == "__main__":
    main() 