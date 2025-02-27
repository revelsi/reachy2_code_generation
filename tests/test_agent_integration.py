#!/usr/bin/env python
"""
Integration tests for the ReachyLangGraphAgent.

These tests verify that the agent properly loads real tool definitions from the Reachy SDK
and can operate in both mock and real implementation modes.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the mock WebSocket server
import mock_websocket

# Patch sys.modules to use our mock websocket
sys.modules['api.websocket'] = mock_websocket

# Import the agent
from agent.langgraph_agent import ReachyLangGraphAgent


class TestAgentIntegration(unittest.TestCase):
    """
    Integration tests for the ReachyLangGraphAgent.
    """
    
    def setUp(self):
        """Set up the test environment."""
        # Clear any existing WebSocket messages
        mock_websocket._mock_websocket_server = mock_websocket.MockWebSocketServer()
    
    @patch('config.USE_MOCK', True)
    @patch('agent.utils.tool_mapper.ReachyToolMapper')
    def test_agent_mock_mode(self, mock_mapper_class):
        """Test that the agent can load real tool definitions but use mock implementations."""
        # Mock the tool mapper to provide real-like tool definitions
        mock_mapper = MagicMock()
        mock_mapper.discover_tool_classes.return_value = []
        mock_mapper.register_tools_from_classes.return_value = 0
        
        # Create sample tools that mimic real Reachy SDK tools
        mock_mapper.get_tool_schemas.return_value = [
            {
                "type": "function",
                "function": {
                    "name": "move_arm",
                    "description": "Move the robot's arm to a specific position.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "side": {"type": "string", "enum": ["left", "right"]},
                            "direction": {"type": "string", "enum": ["up", "down", "left", "right", "forward", "backward"]},
                            "amount": {"type": "number", "description": "Amount to move in the specified direction (in degrees or cm)."}
                        },
                        "required": ["side", "direction"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_arm_position",
                    "description": "Get the current position of the robot's arm.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "side": {"type": "string", "enum": ["left", "right"]}
                        },
                        "required": ["side"]
                    }
                }
            }
        ]
        
        # Create real-like implementations (these won't be used in mock mode)
        def real_move_arm(side, direction, amount=10.0):
            return {
                "success": True,
                "result": {
                    "side": side,
                    "direction": direction,
                    "amount": amount,
                    "final_position": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                }
            }
            
        def real_get_arm_position(side):
            return {
                "success": True,
                "result": {
                    "side": side,
                    "positions": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                }
            }
            
        mock_mapper.get_tool_implementations.return_value = {
            "move_arm": real_move_arm,
            "get_arm_position": real_get_arm_position
        }
        
        mock_mapper_class.return_value = mock_mapper
        
        # Create an agent instance
        agent = ReachyLangGraphAgent(model="gpt-3.5-turbo")
        
        # Verify that tools were loaded
        self.assertTrue(len(agent.tools) > 0, "No tools were loaded")
        self.assertTrue(len(agent.tool_implementations) > 0, "No tool implementations were loaded")
        self.assertEqual(len(agent.tools), 2, "Expected 2 tools to be loaded")
        
        # Verify that the agent can process a message
        with patch.object(agent, '_call_llm', return_value=self._mock_llm_response()):
            response = agent.process_message("Move the right arm up")
            
            # Check that the response contains a message
            self.assertIn("message", response)
            self.assertIsNotNone(response["message"])
            
            # Check that the tool calls were processed
            self.assertIn("tool_calls", response)
            self.assertEqual(len(response["tool_calls"]), 1)
            self.assertEqual(response["tool_calls"][0]["name"], "move_arm")
            self.assertEqual(response["tool_calls"][0]["arguments"]["side"], "right")
            self.assertEqual(response["tool_calls"][0]["arguments"]["direction"], "up")
            
            # Verify that the result contains the mock flag
            self.assertTrue(response["tool_calls"][0]["result"].get("mock", False), 
                           "Expected mock implementation to be used")
    
    @patch('config.USE_MOCK', False)
    @patch('agent.utils.tool_mapper.ReachyToolMapper')
    def test_agent_real_mode(self, mock_mapper_class):
        """Test that the agent can load real tool definitions and use real implementations."""
        # Mock the tool mapper to provide real-like tool definitions
        mock_mapper = MagicMock()
        mock_mapper.discover_tool_classes.return_value = []
        mock_mapper.register_tools_from_classes.return_value = 0
        
        # Create sample tools that mimic real Reachy SDK tools
        mock_mapper.get_tool_schemas.return_value = [
            {
                "type": "function",
                "function": {
                    "name": "move_arm",
                    "description": "Move the robot's arm to a specific position.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "side": {"type": "string", "enum": ["left", "right"]},
                            "direction": {"type": "string", "enum": ["up", "down", "left", "right", "forward", "backward"]},
                            "amount": {"type": "number", "description": "Amount to move in the specified direction (in degrees or cm)."}
                        },
                        "required": ["side", "direction"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_arm_position",
                    "description": "Get the current position of the robot's arm.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "side": {"type": "string", "enum": ["left", "right"]}
                        },
                        "required": ["side"]
                    }
                }
            }
        ]
        
        # Create real-like implementations
        def real_move_arm(side, direction, amount=10.0):
            return {
                "success": True,
                "result": {
                    "side": side,
                    "direction": direction,
                    "amount": amount,
                    "final_position": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                }
            }
            
        def real_get_arm_position(side):
            return {
                "success": True,
                "result": {
                    "side": side,
                    "positions": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                }
            }
            
        mock_mapper.get_tool_implementations.return_value = {
            "move_arm": real_move_arm,
            "get_arm_position": real_get_arm_position
        }
        
        mock_mapper_class.return_value = mock_mapper
        
        # Create an agent instance
        agent = ReachyLangGraphAgent(model="gpt-3.5-turbo")
        
        # Verify that tools were loaded
        self.assertTrue(len(agent.tools) > 0, "No tools were loaded")
        self.assertTrue(len(agent.tool_implementations) > 0, "No tool implementations were loaded")
        self.assertEqual(len(agent.tools), 2, "Expected 2 tools to be loaded")
        
        # Verify that the agent can process a message
        with patch.object(agent, '_call_llm', return_value=self._mock_llm_response()):
            response = agent.process_message("Move the right arm up")
            
            # Check that the response contains a message
            self.assertIn("message", response)
            self.assertIsNotNone(response["message"])
            
            # Check that the tool calls were processed
            self.assertIn("tool_calls", response)
            self.assertEqual(len(response["tool_calls"]), 1)
            self.assertEqual(response["tool_calls"][0]["name"], "move_arm")
            self.assertEqual(response["tool_calls"][0]["arguments"]["side"], "right")
            self.assertEqual(response["tool_calls"][0]["arguments"]["direction"], "up")
            
            # Verify that the result does NOT contain the mock flag
            self.assertNotIn("mock", response["tool_calls"][0]["result"], 
                           "Expected real implementation to be used")
    
    def _mock_llm_response(self):
        """Create a mock LLM response with a tool call."""
        from langchain_core.messages import AIMessage
        
        return {
            "messages": [
                AIMessage(
                    content=None,
                    tool_calls=[
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {
                                "name": "move_arm",
                                "arguments": '{"side": "right", "direction": "up"}'
                            }
                        }
                    ]
                )
            ],
            "current_tool_calls": [
                {
                    "id": "call_123",
                    "name": "move_arm",
                    "arguments": {"side": "right", "direction": "up"}
                }
            ],
            "tool_results": [],
            "error": None,
            "final_response": None
        }


if __name__ == "__main__":
    unittest.main() 