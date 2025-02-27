#!/usr/bin/env python

import os
import sys
import unittest
import logging
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.langgraph_agent import ReachyLangGraphAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestReachyLangGraphAgent(unittest.TestCase):
    """Test cases for the ReachyLangGraphAgent."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        load_dotenv()
        cls.agent = ReachyLangGraphAgent(
            model="gpt-4-turbo",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.tools)
        self.assertIsNotNone(self.agent.tool_implementations)
        self.assertTrue(len(self.agent.tools) > 0)
        logger.info(f"Found {len(self.agent.tools)} tools")
    
    def test_tool_loading(self):
        """Test that tools are loaded correctly."""
        # Check tool schemas
        for tool in self.agent.tools:
            self.assertIn("type", tool)
            self.assertEqual(tool["type"], "function")
            self.assertIn("function", tool)
            self.assertIn("name", tool["function"])
            self.assertIn("description", tool["function"])
            self.assertIn("parameters", tool["function"])
        
        # Check tool implementations
        for tool_name in self.agent.tool_implementations:
            self.assertTrue(callable(self.agent.tool_implementations[tool_name]))
    
    def test_basic_query(self):
        """Test processing a basic query."""
        response = self.agent.process_message("What tools are available?")
        self.assertIsNotNone(response)
        self.assertIn("message", response)
        self.assertIsNone(response["error"])
        logger.info(f"Response: {response['message']}")
    
    def test_tool_execution(self):
        """Test executing a tool."""
        response = self.agent.process_message("Get the current position of the right arm")
        self.assertIsNotNone(response)
        self.assertIn("message", response)
        self.assertIn("tool_calls", response)
        self.assertTrue(len(response["tool_calls"]) > 0)
        logger.info(f"Tool calls: {response['tool_calls']}")
        logger.info(f"Response: {response['message']}")
    
    def test_error_handling(self):
        """Test error handling with an invalid tool name."""
        response = self.agent.process_message("Use the non_existent_tool to do something")
        self.assertIsNotNone(response)
        self.assertIn("message", response)
        logger.info(f"Error handling response: {response['message']}")

if __name__ == "__main__":
    unittest.main(verbosity=2) 