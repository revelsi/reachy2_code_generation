#!/usr/bin/env python
"""
Test script for the ReachyLangGraphAgent in isolation.

This script allows testing the agent's reasoning capabilities and tool integration
without requiring actual robot hardware.
"""

import json
import os
import sys
from typing import Dict, Any, List
import logging
from dotenv import load_dotenv

# Set path to find the agent module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_test")

# Load environment variables
load_dotenv()

# Import the mock WebSocket server
# We import this before the agent to ensure it's used for testing
import mock_websocket

# Patch sys.modules to use our mock websocket
sys.modules['api.websocket'] = mock_websocket

# Now import the agent
from agent.langgraph_agent import ReachyLangGraphAgent


class MockToolMapper:
    """
    Mock implementation of the tool mapper that provides mock tools for testing.
    This allows testing the agent without requiring actual robot hardware.
    """
    
    def __init__(self):
        self.tool_schemas = {}
        self.tool_implementations = {}
        self._register_mock_tools()
    
    def _register_mock_tools(self):
        """Register mock tools for testing."""
        # Mock tool: move_arm
        self.tool_schemas["move_arm"] = {
            "type": "function",
            "function": {
                "name": "move_arm",
                "description": "Move the robot's arm to a specific position.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "side": {
                            "type": "string",
                            "enum": ["left", "right"],
                            "description": "Which arm to move (left or right)."
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["up", "down", "left", "right", "forward", "backward"],
                            "description": "Direction to move the arm."
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to move in the specified direction (in degrees or cm)."
                        }
                    },
                    "required": ["side", "direction"]
                }
            }
        }
        
        # Mock implementation of move_arm
        def mock_move_arm(side: str, direction: str, amount: float = 10.0) -> Dict[str, Any]:
            logger.info(f"MOCK: Moving {side} arm {direction} by {amount}")
            return {
                "success": True,
                "result": {
                    "side": side,
                    "direction": direction,
                    "amount": amount,
                    "final_position": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                }
            }
        
        self.tool_implementations["move_arm"] = mock_move_arm
        
        # Mock tool: get_arm_position
        self.tool_schemas["get_arm_position"] = {
            "type": "function",
            "function": {
                "name": "get_arm_position",
                "description": "Get the current position of the robot's arm.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "side": {
                            "type": "string",
                            "enum": ["left", "right"],
                            "description": "Which arm to query (left or right)."
                        }
                    },
                    "required": ["side"]
                }
            }
        }
        
        # Mock implementation of get_arm_position
        def mock_get_arm_position(side: str) -> Dict[str, Any]:
            logger.info(f"MOCK: Getting position of {side} arm")
            return {
                "success": True,
                "result": {
                    "side": side,
                    "positions": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                    "gripper_opening": 0.5
                }
            }
        
        self.tool_implementations["get_arm_position"] = mock_get_arm_position
        
        # Mock tool: move_head
        self.tool_schemas["move_head"] = {
            "type": "function",
            "function": {
                "name": "move_head",
                "description": "Move the robot's head to look in a specific direction.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "yaw": {
                            "type": "number",
                            "description": "Rotation around the vertical axis (left/right) in degrees."
                        },
                        "pitch": {
                            "type": "number",
                            "description": "Rotation around the horizontal axis (up/down) in degrees."
                        }
                    },
                    "required": []
                }
            }
        }
        
        # Mock implementation of move_head
        def mock_move_head(yaw: float = 0.0, pitch: float = 0.0) -> Dict[str, Any]:
            logger.info(f"MOCK: Moving head to yaw={yaw}, pitch={pitch}")
            return {
                "success": True,
                "result": {
                    "yaw": yaw,
                    "pitch": pitch,
                    "final_position": [yaw, pitch, 0.0]
                }
            }
        
        self.tool_implementations["move_head"] = mock_move_head
    
    def discover_tool_classes(self):
        """Mock method for tool discovery."""
        pass
    
    def register_tools_from_classes(self):
        """Mock method for tool registration."""
        pass
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get the list of mock tool schemas."""
        return list(self.tool_schemas.values())
    
    def get_tool_implementations(self) -> Dict[str, Any]:
        """Get the dictionary of mock tool implementations."""
        return self.tool_implementations


# Patch the ReachyToolMapper in the agent module
import sys
import agent.langgraph_agent
sys.modules['tool_mapper'] = type('', (), {})
sys.modules['tool_mapper'].ReachyToolMapper = MockToolMapper


# Modified agent class that uses mock tools
class TestableReachyAgent(ReachyLangGraphAgent):
    """
    A testable version of the ReachyLangGraphAgent that uses mock tools.
    """
    
    def load_tools(self):
        """
        Override tool loading to use mock tools.
        """
        # Create a mock tool mapper instance
        mapper = MockToolMapper()
        
        # Get tool schemas and implementations
        self.tools = mapper.get_tool_schemas()
        self.tool_implementations = mapper.get_tool_implementations()
        
        print(f"Loaded {len(self.tools)} mock tools and {len(self.tool_implementations)} implementations")


def run_test_conversation():
    """
    Run a test conversation with the agent using mock tools.
    """
    # Get the mock WebSocket server
    ws_server = mock_websocket.get_websocket_server()
    
    # Create the agent
    agent = TestableReachyAgent(
        model="gpt-4-turbo", 
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # Test messages to send to the agent
    test_messages = [
        "Can you move the robot's right arm up?",
        "What is the current position of the left arm?",
        "Turn the head to look left",
        "Can you tell me what tools you have available?"
    ]
    
    # Process each test message
    for i, message in enumerate(test_messages):
        print(f"\n\n===== Test {i+1}: {message} =====\n")
        
        # Clear previous notifications
        ws_server.thinking_messages = []
        ws_server.error_messages = []
        ws_server.function_calls = []
        ws_server.messages = []
        
        try:
            response = agent.process_message(message)
            print(f"Agent response: {response['message']}")
            
            if response['tool_calls']:
                print("\nTool calls:")
                for tc in response['tool_calls']:
                    print(f"  - {tc['name']}({tc['arguments']})")
                    print(f"    Result: {tc['result']}")
            
            if response['error']:
                print(f"\nError: {response['error']}")
                
            # Print all captured notifications
            print("\nNotifications captured:")
            print(f"  - Thinking messages: {len(ws_server.thinking_messages)}")
            print(f"  - Function calls: {len(ws_server.function_calls)}")
            print(f"  - Errors: {len(ws_server.error_messages)}")
            print(f"  - Completions: {len(ws_server.messages)}")
            
        except Exception as e:
            print(f"Error during test: {str(e)}")


def test_specific_command(command: str):
    """
    Test the agent with a specific command.
    
    Args:
        command: The command to test
    """
    # Get the mock WebSocket server
    ws_server = mock_websocket.get_websocket_server()
    
    # Create the agent
    agent = TestableReachyAgent(
        model="gpt-4-turbo", 
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # Clear previous notifications
    ws_server.thinking_messages = []
    ws_server.error_messages = []
    ws_server.function_calls = []
    ws_server.messages = []
    
    print(f"\n\n===== Testing: {command} =====\n")
    
    try:
        response = agent.process_message(command)
        print(f"Agent response: {response['message']}")
        
        if response['tool_calls']:
            print("\nTool calls:")
            for tc in response['tool_calls']:
                print(f"  - {tc['name']}({tc['arguments']})")
                print(f"    Result: {tc['result']}")
        
        if response['error']:
            print(f"\nError: {response['error']}")
            
        # Print all captured notifications
        print("\nNotifications captured:")
        print(f"  - Thinking messages: {len(ws_server.thinking_messages)}")
        print(f"  - Function calls: {len(ws_server.function_calls)}")
        print(f"  - Errors: {len(ws_server.error_messages)}")
        print(f"  - Completions: {len(ws_server.messages)}")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the ReachyLangGraphAgent in isolation")
    parser.add_argument("--command", type=str, help="A specific command to test", required=False)
    
    args = parser.parse_args()
    
    if args.command:
        test_specific_command(args.command)
    else:
        run_test_conversation() 