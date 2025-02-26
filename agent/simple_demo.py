#!/usr/bin/env python
"""
Simple demo script for the Reachy function calling with transparent execution.

This script demonstrates the transparent function calling framework with minimal dependencies.
It shows how functions can be executed with reasoning, parameter validation, and user approval.
It also includes OpenAI function calling for natural language control.
"""

import os
import sys
import json
import time
import logging
import argparse
from typing import Dict, Any, List, Optional, Callable, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("simple_demo")

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add the current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI SDK not available. Natural language control will not be available.")
    OPENAI_AVAILABLE = False

# Simple transparent executor
class SimpleTransparentExecutor:
    """
    Simple transparent executor that shows reasoning and function calls.
    
    This class wraps functions to provide a transparent execution flow that:
    1. Shows the reasoning behind each function call
    2. Displays the function call with parameters
    3. Requests user permission before execution
    4. Shows execution results
    """
    
    def __init__(self, auto_approve: bool = False):
        """
        Initialize the transparent executor.
        
        Args:
            auto_approve: Whether to automatically approve function calls
        """
        self.auto_approve = auto_approve
        self.execution_history = []
        self.functions = {}
        
    def register_function(self, func: Callable) -> Callable:
        """
        Register a function with the executor.
        
        Args:
            func: Function to register
            
        Returns:
            Callable: Wrapped function
        """
        function_name = func.__name__
        self.functions[function_name] = func
        
        def wrapped_function(*args, **kwargs):
            # Extract reasoning
            reasoning = kwargs.pop("reasoning", "No reasoning provided")
            
            # Format parameters for display
            params = {**dict(zip(func.__code__.co_varnames, args)), **kwargs}
            
            # Display execution plan
            self._display_execution_plan(function_name, reasoning, params)
            
            # Request approval
            if not self.auto_approve:
                approved = self._request_approval()
                if not approved:
                    print("\n❌ Execution rejected by user")
                    return {"success": False, "error": "Execution rejected by user"}
            
            # Execute function
            print(f"\n🔄 Executing: {function_name}...")
            try:
                result = func(*args, **kwargs)
                self._display_execution_result(function_name, result)
                return {"success": True, "result": result}
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                return {"success": False, "error": str(e)}
        
        return wrapped_function
    
    def _display_execution_plan(self, function_name: str, reasoning: str, params: Dict[str, Any]) -> None:
        """Display the execution plan."""
        print("\n" + "=" * 80)
        print(f"🧠 REASONING: {reasoning}")
        print("-" * 80)
        print(f"📋 FUNCTION: {function_name}")
        print(f"📝 PARAMETERS:")
        print(json.dumps(params, indent=2, default=str))
        print("-" * 80)
        print("=" * 80)
    
    def _request_approval(self) -> bool:
        """Request user approval for execution."""
        while True:
            response = input("\n⚠️ Execute this function? (y/n): ").strip().lower()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def _display_execution_result(self, function_name: str, result: Any) -> None:
        """Display the execution result."""
        print("\n" + "-" * 80)
        print(f"✅ SUCCESS: {function_name}")
        print(f"📊 RESULT:")
        print(json.dumps(result, indent=2, default=str))
        print("-" * 80)


# Mock Reachy robot for demo
class MockReachy:
    """Simple mock Reachy robot for demo purposes."""
    
    def __init__(self):
        """Initialize the mock Reachy robot."""
        self.arms = {
            "left": {"position": [0.0] * 7, "gripper_opening": 0.5},
            "right": {"position": [0.0] * 7, "gripper_opening": 0.5}
        }
        self.head = {"position": [0.0, 0.0, 0.0]}  # roll, pitch, yaw
        self.base = {"position": [0.0, 0.0, 0.0]}  # x, y, theta
        
    def get_info(self) -> Dict[str, Any]:
        """Get information about the robot."""
        return {
            "name": "Mock Reachy 2",
            "version": "2.0.0",
            "parts": ["left_arm", "right_arm", "head", "mobile_base"],
            "cameras": ["teleop", "depth"],
            "has_audio": True,
            "has_mobile_base": True
        }
    
    def move_arm(self, arm: str, positions: List[float]) -> Dict[str, Any]:
        """Move an arm to the specified positions."""
        if arm not in self.arms:
            return {"success": False, "error": f"Invalid arm: {arm}"}
        
        self.arms[arm]["position"] = positions
        return {
            "success": True,
            "arm": arm,
            "positions": positions
        }
    
    def look_at(self, x: float, y: float, z: float) -> Dict[str, Any]:
        """Make the head look at a point in space."""
        # Simplified calculation
        roll = 0.0
        pitch = 0.2 if z > 0 else -0.2
        yaw = 0.3 if y > 0 else -0.3
        
        self.head["position"] = [roll, pitch, yaw]
        return {
            "success": True,
            "target": [x, y, z],
            "head_position": self.head["position"]
        }
    
    def move_base(self, x: float, y: float, theta: float) -> Dict[str, Any]:
        """Move the base to the specified position."""
        self.base["position"] = [x, y, theta]
        return {
            "success": True,
            "position": [x, y, theta]
        }


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


def run_examples(executor: SimpleTransparentExecutor, reachy: MockReachy) -> None:
    """Run example commands with the transparent executor."""
    print_section("Running example commands")
    
    # Example 1: Get robot info
    get_robot_info = executor.register_function(reachy.get_info)
    get_robot_info(reasoning="Need to check the robot's capabilities")
    
    # Example 2: Move an arm
    move_arm = executor.register_function(reachy.move_arm)
    move_arm(
        arm="right",
        positions=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        reasoning="Moving the right arm to a specific position"
    )
    
    # Example 3: Look at a point
    look_at = executor.register_function(reachy.look_at)
    look_at(
        x=0.5,
        y=0.3,
        z=0.2,
        reasoning="Making the robot look at an object in front"
    )
    
    # Example 4: Move the base
    move_base = executor.register_function(reachy.move_base)
    move_base(
        x=1.0,
        y=0.5,
        theta=45.0,
        reasoning="Moving the robot to a new position"
    )


def create_function_schemas(reachy: MockReachy) -> List[Dict[str, Any]]:
    """
    Create function schemas for OpenAI function calling.
    
    Args:
        reachy: The Reachy robot instance
        
    Returns:
        List[Dict[str, Any]]: List of function schemas
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_info",
                "description": "Get information about the robot's capabilities",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_arm",
                "description": "Move an arm to the specified positions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "arm": {
                            "type": "string",
                            "description": "Which arm to move (left or right)",
                            "enum": ["left", "right"]
                        },
                        "positions": {
                            "type": "array",
                            "description": "Joint positions for the 7 joints of the arm",
                            "items": {
                                "type": "number"
                            }
                        }
                    },
                    "required": ["arm", "positions"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "look_at",
                "description": "Make the robot look at a point in space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "X coordinate in meters (forward/backward)"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate in meters (left/right)"
                        },
                        "z": {
                            "type": "number",
                            "description": "Z coordinate in meters (up/down)"
                        }
                    },
                    "required": ["x", "y", "z"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_base",
                "description": "Move the mobile base to a new position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "X coordinate in meters (forward/backward)"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate in meters (left/right)"
                        },
                        "theta": {
                            "type": "number",
                            "description": "Rotation angle in degrees"
                        }
                    },
                    "required": ["x", "y", "theta"]
                }
            }
        }
    ]


def run_openai_agent(
    executor: SimpleTransparentExecutor, 
    reachy: MockReachy, 
    prompt: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Run an OpenAI agent with the provided tools.
    
    Args:
        executor: The transparent executor
        reachy: The Reachy robot instance
        prompt: User prompt for the agent
        model: OpenAI model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
        api_key: OpenAI API key (uses env var if None)
    """
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI SDK not available. Cannot run natural language control.")
        return
    
    print_section("OpenAI Natural Language Control")
    print(f"User prompt: {prompt}")
    
    # Use model from environment variable if not provided
    if model is None:
        model = os.environ.get("MODEL", "gpt-4-turbo")
    
    print(f"Using model: {model}")
    
    # Set up OpenAI client
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = OpenAI()
    
    # Register functions with the executor
    registered_functions = {
        "get_info": executor.register_function(reachy.get_info),
        "move_arm": executor.register_function(reachy.move_arm),
        "look_at": executor.register_function(reachy.look_at),
        "move_base": executor.register_function(reachy.move_base)
    }
    
    # Create function schemas
    tools = create_function_schemas(reachy)
    
    # System message
    system_message = """
    You are an assistant that controls a Reachy 2 robot. You can use the available functions
    to control the robot's arms, head, and mobile base.
    
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
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # Get the response
        message = response.choices[0].message
        
        # Print the assistant's message
        if message.content:
            print(f"\n🤖 Assistant: {message.content}")
        
        # Handle tool calls
        if message.tool_calls:
            # Add the assistant's message with tool calls to the conversation
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in message.tool_calls
                ]
            })
            
            # Process each tool call
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Add reasoning from the assistant's message or a default
                reasoning = message.content if message.content else f"Executing {function_name} based on user request"
                
                # Execute the function
                if function_name in registered_functions:
                    # Add reasoning to the arguments
                    function_args["reasoning"] = reasoning
                    
                    # Call the function
                    result = registered_functions[function_name](**function_args)
                    
                    # Add the result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
                else:
                    print(f"❌ Unknown function: {function_name}")
            
            # Get final response
            final_response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            
            final_message = final_response.choices[0].message
            print(f"\n🤖 Final response: {final_message.content}")
    
    except Exception as e:
        print(f"❌ Error calling OpenAI API: {str(e)}")
        import traceback
        traceback.print_exc()


def interactive_mode(
    executor: SimpleTransparentExecutor, 
    reachy: MockReachy,
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Run in interactive mode, allowing the user to enter natural language commands.
    
    Args:
        executor: The transparent executor
        reachy: The Reachy robot instance
        model: OpenAI model to use
        api_key: OpenAI API key
    """
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI SDK not available. Cannot run interactive mode.")
        return
    
    print_section("Interactive Mode")
    print("Enter natural language commands for the robot (type 'exit' to quit)")
    
    while True:
        try:
            prompt = input("\nCommand> ")
            if prompt.lower() in ["exit", "quit", "q"]:
                break
            
            if prompt:
                run_openai_agent(
                    executor=executor,
                    reachy=reachy,
                    prompt=prompt,
                    model=model,
                    api_key=api_key
                )
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def main() -> None:
    """Main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Simple demo for transparent function calling")
    parser.add_argument("--auto-approve", action="store_true", help="Automatically approve all function calls")
    parser.add_argument("--model", default=os.environ.get("MODEL", "gpt-4-turbo"), help="OpenAI model to use")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    parser.add_argument("--prompt", help="Natural language prompt for the robot")
    parser.add_argument("--examples", action="store_true", help="Run example commands")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Print welcome message
    print_header("Reachy Transparent Function Calling Demo")
    print(f"Using model: {args.model}")
    
    # Create executor and mock robot
    executor = SimpleTransparentExecutor(auto_approve=args.auto_approve)
    reachy = MockReachy()
    
    # Run examples if requested
    if args.examples:
        run_examples(executor, reachy)
    
    # Run with prompt if provided
    if args.prompt:
        run_openai_agent(
            executor=executor,
            reachy=reachy,
            prompt=args.prompt,
            model=args.model,
            api_key=args.api_key
        )
    
    # Run in interactive mode if requested
    if args.interactive:
        interactive_mode(
            executor=executor,
            reachy=reachy,
            model=args.model,
            api_key=args.api_key
        )
    
    # If no mode specified, run examples
    if not (args.examples or args.prompt or args.interactive):
        run_examples(executor, reachy)
    
    print("\nDemo completed!")


if __name__ == "__main__":
    main() 