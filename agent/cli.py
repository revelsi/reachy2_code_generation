#!/usr/bin/env python
"""
Command-line interface for the Reachy 2 robot agent.

This module provides a CLI for interacting with the Reachy 2 robot agent.
"""

import argparse
import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Define DEFAULT_MODULES to resolve import issues in api/app.py
DEFAULT_MODULES = []

# Load environment variables from .env file
load_dotenv()

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from agent.langgraph_agent import ReachyLangGraphAgent


def setup_agent(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> ReachyLangGraphAgent:
    """
    Set up the Reachy agent with tools.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
        model: LLM model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
        temperature: Temperature for LLM sampling.
        max_tokens: Maximum tokens for LLM response.
        
    Returns:
        ReachyLangGraphAgent: Configured LangGraph agent.
    """
    # Use model from environment variable if not provided
    if model is None:
        model = os.environ.get("MODEL", "gpt-4-turbo")
    
    # Create agent
    agent = ReachyLangGraphAgent(
        api_key=api_key, 
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Tools are loaded automatically in the agent's __init__ method
    print(f"Reachy 2 Agent ready with {len(agent.tools)} tools")
    print(f"Using model: {model}")
    
    return agent


def main():
    """Run the Reachy agent CLI."""
    parser = argparse.ArgumentParser(description="Reachy 2 Agent CLI")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--model", default=os.environ.get("MODEL", "gpt-4-turbo"), help="LLM model to use")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions and implementations")
    parser.add_argument("--focus", nargs="+", default=DEFAULT_MODULES, help="Focus on specific modules")
    
    args = parser.parse_args()
    
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