#!/usr/bin/env python
"""
Command-line interface for the Reachy 2 robot agent.

This module provides a CLI for interacting with the Reachy 2 robot agent.
"""

import argparse
import os
import sys
from typing import Optional, List, Dict, Any
import json

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration and agent
from config import (
    OPENAI_API_KEY, MODEL, DEBUG, DISABLE_WEBSOCKET, 
    get_model_config, update_model_config, AVAILABLE_MODELS
)
from agent.agent_router import AgentRouter, AgentMode

# Define DEFAULT_MODULES to resolve import issues in api/app.py
DEFAULT_MODULES = []

def setup_agent(
    api_key: str = None,
    model_config: Dict[str, Any] = None,
    focus_modules: List[str] = None,
    regenerate_tools: bool = False,
    mode: AgentMode = AgentMode.FUNCTION_CALLING,
) -> AgentRouter:
    """
    Set up the Reachy 2 agent router.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
        model_config: Model configuration. If None, will use the configuration from config.py.
        focus_modules: Optional list of module names to focus on (default: parts, orbita, utils).
        regenerate_tools: Whether to regenerate tool definitions and implementations.
        mode: The agent mode to use (function_calling or code_generation).
        
    Returns:
        AgentRouter: The configured agent router.
    """
    # Use API key from environment variable if not provided
    if api_key is None:
        api_key = OPENAI_API_KEY
    
    # Use default modules if focus_modules is None
    if focus_modules is None:
        focus_modules = DEFAULT_MODULES
    
    # Use default model configuration if not provided
    if model_config is None:
        model_config = get_model_config()
    
    # Create agent router
    agent_router = AgentRouter(
        api_key=api_key,
        model_config=model_config,
        focus_modules=focus_modules,
        regenerate_tools=regenerate_tools,
        default_mode=mode
    )
    
    # Tools are loaded automatically in the agent's __init__ method
    print(f"Reachy 2 Agent ready with {len(agent_router.get_available_tools())} tools")
    print(f"Using model: {model_config.get('model', MODEL)}")
    print(f"Current mode: {agent_router.get_mode()}")
    
    return agent_router


def main():
    """Run the Reachy agent CLI."""
    parser = argparse.ArgumentParser(description="Reachy 2 Agent CLI")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--model", choices=AVAILABLE_MODELS, default=MODEL, help="LLM model to use")
    parser.add_argument("--temperature", type=float, default=0.2, help="Model temperature (0.0 to 1.0)")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Maximum tokens to generate")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions and implementations")
    parser.add_argument("--focus", nargs="+", default=DEFAULT_MODULES, help="Focus on specific modules")
    parser.add_argument("--disable-websocket", action="store_true", default=DISABLE_WEBSOCKET, help="Disable WebSocket server")
    parser.add_argument("--debug", action="store_true", default=DEBUG, help="Enable debug mode")
    parser.add_argument("--mode", choices=[AgentMode.FUNCTION_CALLING, AgentMode.CODE_GENERATION], 
                        default=AgentMode.FUNCTION_CALLING, help="Agent mode")
    
    args = parser.parse_args()
    
    # Set environment variables based on arguments
    if args.disable_websocket:
        os.environ["DISABLE_WEBSOCKET"] = "1"
    
    if args.debug:
        os.environ["DEBUG"] = "1"
    
    # Create model configuration
    model_config = {
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    
    print(f"Starting Reachy 2 Agent CLI with model: {args.model}")
    
    # Create agent
    agent = setup_agent(
        api_key=args.api_key,
        model_config=model_config,
        focus_modules=args.focus,
        regenerate_tools=args.regenerate,
        mode=args.mode
    )
    
    print("Type 'exit' or 'quit' to exit")
    print("Type 'reset' to reset the conversation")
    print("Type 'mode function_calling' or 'mode code_generation' to switch modes")
    print("Type 'config' to view current model configuration")
    print("Type 'config model gpt-4o' to change model")
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
            
            # Check for mode switch command
            if user_input.lower().startswith("mode "):
                mode_name = user_input.lower().split("mode ")[1].strip()
                try:
                    new_mode = AgentMode(mode_name)
                    agent.set_mode(new_mode)
                    print(f"Switched to {new_mode} mode")
                except ValueError:
                    print(f"Invalid mode: {mode_name}. Valid modes are: {list(AgentMode)}")
                continue
            
            # Check for config commands
            if user_input.lower() == "config":
                # Display current configuration
                config = agent.get_model_config()
                print("\nCurrent Model Configuration:")
                for key, value in config.items():
                    print(f"  {key}: {value}")
                print()
                continue
            
            if user_input.lower().startswith("config "):
                # Parse configuration command
                config_parts = user_input.lower().split("config ")[1].strip().split()
                if len(config_parts) >= 2:
                    key = config_parts[0]
                    value = " ".join(config_parts[1:])
                    
                    # Convert value to appropriate type
                    if key in ["temperature", "top_p", "frequency_penalty", "presence_penalty"]:
                        try:
                            value = float(value)
                        except ValueError:
                            print(f"Invalid value for {key}: {value}. Must be a number.")
                            continue
                    elif key == "max_tokens":
                        try:
                            value = int(value)
                        except ValueError:
                            print(f"Invalid value for {key}: {value}. Must be an integer.")
                            continue
                    
                    # Update configuration
                    new_config = {key: value}
                    try:
                        agent.update_model_config(new_config)
                        print(f"Updated {key} to {value}")
                    except Exception as e:
                        print(f"Error updating configuration: {e}")
                else:
                    print("Invalid config command. Format: config [key] [value]")
                continue
            
            # Process message
            response = agent.process_message(user_input)
            
            # Handle response based on mode
            if agent.get_mode() == AgentMode.FUNCTION_CALLING:
                # Print response message
                print(f"Agent: {response.get('message', '')}")
                
                # Print tool calls if any
                tool_calls = response.get("tool_calls", [])
                if tool_calls:
                    print("\nTool Calls:")
                    for i, tool_call in enumerate(tool_calls):
                        print(f"  {i+1}. {tool_call.get('name', 'Unknown tool')}")
                        print(f"     Arguments: {json.dumps(tool_call.get('arguments', {}), indent=2)}")
            else:  # code_generation mode
                # Print response message
                print(f"Agent: {response.get('message', '')}")
                
                # Print generated code if any
                code = response.get("code", "")
                if code:
                    print("\nGenerated Code:")
                    print("```python")
                    print(code)
                    print("```")
                    
                    # Print validation results
                    validation = response.get("validation", {})
                    if validation:
                        print("\nCode Validation:")
                        print(f"  Valid: {validation.get('valid', False)}")
                        
                        errors = validation.get("errors", [])
                        if errors:
                            print("  Errors:")
                            for error in errors:
                                print(f"    - {error}")
                        
                        warnings = validation.get("warnings", [])
                        if warnings:
                            print("  Warnings:")
                            for warning in warnings:
                                print(f"    - {warning}")
            
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye!")


if __name__ == "__main__":
    main() 