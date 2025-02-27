#!/usr/bin/env python
"""
Demo script for the Reachy function calling agent with transparent execution.

This script demonstrates how the agent works with transparent function calls,
showing reasoning, parameter validation, and user approval before execution.
"""

import os
import sys
import argparse
import logging
import json
import time
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("demo")

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add the current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import tools and executor directly
try:
    from transparent_executor import get_executor
    from tools.connection_manager import connect_to_reachy, disconnect_reachy, get_connection_info
except ImportError:
    # Try with agent prefix
    from agent.transparent_executor import get_executor
    from agent.tools.connection_manager import connect_to_reachy, disconnect_reachy, get_connection_info

# Try to import OpenAI (optional)
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI SDK not available. Using local examples only.")
    OPENAI_AVAILABLE = False


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}  ".center(80, "="))
    print("=" * 80)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "-" * 80)
    print(f"  {title}  ".center(80, "-"))
    print("-" * 80)


def setup_tools(use_mock: bool = False, auto_approve: bool = False) -> Dict[str, Any]:
    """
    Set up the tools for the demo.
    
    Args:
        use_mock: Whether to use mock implementations
        auto_approve: Whether to automatically approve function calls
        
    Returns:
        Dict[str, Any]: Dictionary of available tools
    """
    print_section("Setting up tools")
    
    # Configure the executor
    executor = get_executor(
        auto_approve=auto_approve,
        use_mock=use_mock,
        dry_run=False,
        verbose=True
    )
    
    # Connect to Reachy (real or mock)
    print("Connecting to Reachy...")
    reachy = connect_to_reachy(use_mock=use_mock)
    
    # Get connection info
    connection_info = get_connection_info()
    print(f"Connection: {connection_info['connection_type']}")
    
    # Load tool classes
    try:
        from agent.utils.tool_mapper import ReachyToolMapper
    except ImportError:
        try:
            from agent.tool_mapper import ReachyToolMapper
        except ImportError:
            logger.error("Could not import ReachyToolMapper. Demo will be limited.")
            return {
                "executor": executor,
                "reachy": reachy,
                "tools": {},
                "schemas": {},
                "mapper": None
            }
    
    # Create tool mapper and discover tools
    print("Discovering tools...")
    mapper = ReachyToolMapper()
    tool_classes = mapper.discover_tool_classes()
    print(f"Found {len(tool_classes)} tool classes")
    
    # Register tools
    mapper.register_tools_from_classes()
    
    # Get tool implementations
    tools = mapper.get_tool_implementations()
    schemas = mapper.get_tool_schemas()
    
    print(f"Registered {len(tools)} tools:")
    for i, name in enumerate(sorted(tools.keys()), 1):
        print(f"  {i}. {name}")
    
    return {
        "executor": executor,
        "reachy": reachy,
        "tools": tools,
        "schemas": schemas,
        "mapper": mapper
    }


def run_openai_agent(
    tools_setup: Dict[str, Any],
    prompt: str,
    model: str = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run an OpenAI agent with the provided tools.
    
    Args:
        tools_setup: Tools setup from setup_tools()
        prompt: User prompt for the agent
        model: OpenAI model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
        api_key: OpenAI API key (uses env var if None)
        
    Returns:
        Dict[str, Any]: Result of the agent run
    """
    if not OPENAI_AVAILABLE:
        print("OpenAI SDK not available. Cannot run agent.")
        return {"error": "OpenAI SDK not available"}
    
    # Use model from environment variable if not provided
    if model is None:
        model = os.environ.get("MODEL", "gpt-4-turbo")
    
    # Set up OpenAI client
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = OpenAI()
    
    # Get tools and schemas
    tools = tools_setup["tools"]
    schemas = tools_setup["schemas"]
    
    # Create tool definition for OpenAI
    tools_definition = []
    for name, schema in schemas.items():
        tools_definition.append({
            "type": "function",
            "function": schema["function"] if "function" in schema else schema
        })
    
    # System message
    system_message = """
    You are an assistant that controls a Reachy 2 robot. You can use the available functions
    to control the robot's arms, head, and other components.
    
    Always provide clear reasoning for your actions before calling a function. Think step
    by step about the best approach to fulfill the user's request.
    
    For movements, consider:
    1. Safety first - avoid sudden or extreme movements
    2. Start with slower, smaller movements before large ones
    3. Check the current position before planning movements
    
    When the user asks you to perform an action:
    1. Determine which functions are needed
    2. Explain your reasoning
    3. Call the appropriate functions with suitable parameters
    """
    
    # Run the conversation
    print_section(f"Running OpenAI agent with model: {model}")
    print(f"User prompt: {prompt}")
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    # Make API call
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools_definition,
        tool_choice="auto"
    )
    
    # Get the response
    response_message = response.choices[0].message
    
    # Process tool calls if any
    if hasattr(response_message, "tool_calls") and response_message.tool_calls:
        # There are tool calls to execute
        print("\nAgent wants to call functions:")
        
        # Execute each tool call
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"\nFunction: {function_name}")
            print(f"Arguments: {json.dumps(function_args, indent=2)}")
            
            # Check if function exists
            if function_name in tools:
                # Execute the function
                print(f"Executing {function_name}...")
                function = tools[function_name]
                result = function(**function_args)
                
                # Add result to conversation
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                    ]
                })
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            else:
                print(f"Function {function_name} not found")
        
        # Get final response after tool calls
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        final_response = response.choices[0].message.content
        print("\nFinal response:")
        print(final_response)
        
        return {
            "success": True,
            "response": final_response,
            "messages": messages
        }
    else:
        # No tool calls, just a regular response
        content = response_message.content
        print("\nAgent response:")
        print(content)
        
        return {
            "success": True,
            "response": content,
            "messages": messages
        }


def run_example_commands(tools_setup: Dict[str, Any]) -> None:
    """
    Run example commands using the tools directly.
    
    Args:
        tools_setup: Tools setup from setup_tools()
    """
    print_section("Running example commands")
    
    # Get tools
    tools = tools_setup["tools"]
    
    # Example 1: Get robot info
    print("\nExample 1: Get robot info")
    if "get_robot_info" in tools:
        result = tools["get_robot_info"](
            reasoning="Need to check the robot's capabilities"
        )
        print(f"Result: {json.dumps(result, indent=2)}")
    else:
        print("Tool 'get_robot_info' not available")
    
    # Example 2: Move right arm to a position
    print("\nExample 2: Move right arm to a position")
    if "move_arm" in tools:
        result = tools["move_arm"](
            arm="right",
            positions=[0, 0.3, 0, -0.5, 0, 0, 0],
            duration=2.0,
            interpolation_mode="minimum_jerk",
            wait=True,
            reasoning="Moving the arm to a safe position for demonstration"
        )
        print(f"Result: {json.dumps(result, indent=2)}")
    else:
        print("Tool 'move_arm' not available")
    
    # Example 3: Make the robot look at a point
    print("\nExample 3: Make the robot look at a point")
    if "look_at" in tools:
        result = tools["look_at"](
            x=0.5,
            y=0,
            z=0.3,
            frame="robot",
            duration=1.5,
            interpolation_mode="minimum_jerk",
            wait=True,
            reasoning="Making the robot look forward at a neutral point"
        )
        print(f"Result: {json.dumps(result, indent=2)}")
    else:
        print("Tool 'look_at' not available")


def main():
    """Main entry point for the demo."""
    parser = argparse.ArgumentParser(description="Reachy function calling demo")
    parser.add_argument("--use-mock", action="store_true", help="Use mock implementations")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve function calls")
    parser.add_argument("--openai-key", help="OpenAI API key")
    parser.add_argument("--model", default=os.environ.get("MODEL", "gpt-4-turbo"), help="OpenAI model to use")
    parser.add_argument("--prompt", help="User prompt for the agent")
    parser.add_argument("--examples", action="store_true", help="Run example commands")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    print_header("Reachy Function Calling Demo")
    print(f"Using model: {args.model}")
    
    # Set up tools
    tools_setup = setup_tools(use_mock=args.use_mock, auto_approve=args.auto_approve)
    
    # Run example commands if requested
    if args.examples:
        run_example_commands(tools_setup)
    
    # Run OpenAI agent if requested
    if args.prompt:
        run_openai_agent(
            tools_setup=tools_setup,
            prompt=args.prompt,
            model=args.model,
            api_key=args.openai_key
        )
    
    # Run in interactive mode if requested
    if args.interactive:
        print_section("Interactive Mode")
        print("Enter prompts for the agent (type 'exit' to quit)")
        
        while True:
            try:
                prompt = input("\nPrompt> ")
                if prompt.lower() in ["exit", "quit", "q"]:
                    break
                
                if prompt:
                    run_openai_agent(
                        tools_setup=tools_setup,
                        prompt=prompt,
                        model=args.model,
                        api_key=args.openai_key
                    )
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    # Disconnect from Reachy
    print("\nDisconnecting from Reachy...")
    disconnect_reachy()
    
    print("\nDemo completed.")


if __name__ == "__main__":
    main() 