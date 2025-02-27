#!/usr/bin/env python
"""Unit tests for the ReachyToolMapper class."""

import os
import sys
import unittest
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.utils.tool_mapper import ReachyToolMapper

class TestReachyToolMapper(unittest.TestCase):
    """Test cases for the ReachyToolMapper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mapper = ReachyToolMapper()
    
    def test_tool_registration(self):
        """Test that tools can be registered and retrieved correctly."""
        # Create a mock tool
        tool_name = "test_tool"
        tool_schema = {
            "name": tool_name,
            "description": "A test tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "string", "description": "First argument"},
                    "arg2": {"type": "integer", "description": "Second argument"}
                },
                "required": ["arg1"]
            }
        }
        
        def mock_implementation(arg1: str, arg2: int = 0) -> Dict[str, Any]:
            return {"success": True, "result": f"{arg1}_{arg2}"}
        
        # Register the tool
        self.mapper.register_tool(tool_name, tool_schema, mock_implementation)
        
        # Verify the tool was registered
        self.assertIn(tool_name, self.mapper.tool_schemas)
        self.assertIn(tool_name, self.mapper.tool_implementations)
        
        # Verify the schema was converted to LangChain format
        schema = self.mapper.tool_schemas[tool_name]
        self.assertEqual(schema["type"], "function")
        self.assertEqual(schema["function"]["name"], tool_name)
        
        # Test the implementation
        impl = self.mapper.tool_implementations[tool_name]
        result = impl(arg1="test", arg2=42)
        self.assertEqual(result["result"], "test_42")
    
    def test_schema_validation(self):
        """Test that tool schemas are properly validated."""
        # Test with an invalid schema
        invalid_schema = {
            "name": "invalid_tool",
            # Missing required fields
        }
        
        with self.assertRaises(ValueError):
            self.mapper.register_tool("invalid_tool", invalid_schema, lambda: None)
    
    def test_langchain_format_detection(self):
        """Test that LangChain format detection works correctly."""
        # Test with a schema already in LangChain format
        langchain_schema = {
            "type": "function",
            "function": {
                "name": "test_tool",
                "description": "A test tool",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
        
        self.assertTrue(self.mapper._is_langchain_format(langchain_schema))
        
        # Test with a non-LangChain format
        non_langchain_schema = {
            "name": "test_tool",
            "description": "A test tool",
            "parameters": {}
        }
        
        self.assertFalse(self.mapper._is_langchain_format(non_langchain_schema))

if __name__ == "__main__":
    unittest.main() 