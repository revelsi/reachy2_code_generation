#!/usr/bin/env python
"""
Test script for the LangGraph implementation of the Reachy 2 robot agent.

This script tests the LangGraph implementation by verifying the agent's functionality
with the new class-based tool structure.
"""

import os
import sys
import json
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from agent.langgraph_agent import ReachyLangGraphAgent
from agent.tools.base_tool import BaseTool


class MockTool(BaseTool):
    """A mock tool class for testing."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all mock tools."""
        cls.register_tool(
            name="mock_tool",
            func=cls.mock_tool,
            schema=cls.create_tool_schema(
                name="mock_tool",
                description="A mock tool for testing.",
                parameters={
                    "arg1": {
                        "type": "string",
                        "description": "First argument."
                    },
                    "arg2": {
                        "type": "integer",
                        "description": "Second argument."
                    }
                },
                required=["arg1"]
            )
        )
    
    @staticmethod
    def mock_tool(arg1: str, arg2: int = 0) -> Dict[str, Any]:
        """
        A mock tool for testing.
        
        Args:
            arg1: First argument.
            arg2: Second argument.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        return {
            "success": True,
            "result": f"Processed {arg1} with {arg2}"
        }


def test_agent_initialization():
    """Test that the agent can be initialized."""
    agent = ReachyLangGraphAgent()
    assert agent is not None
    print("✅ Agent initialized successfully")


def test_tool_loading():
    """Test that the agent can load tools using the tool mapper."""
    agent = ReachyLangGraphAgent()
    
    # Check that tools were loaded
    assert len(agent.tools) > 0
    assert len(agent.tool_implementations) > 0
    
    print(f"✅ Tools loaded successfully: {len(agent.tools)} tools available")


def test_message_processing():
    """Test that the agent can process messages."""
    agent = ReachyLangGraphAgent()
    
    # Process a message (without actually calling OpenAI)
    try:
        # This will fail without an API key, but we just want to test the structure
        agent.process_message("Hello, what can you do?")
    except Exception as e:
        # Just check that the error is related to the API, not our code
        assert "api_key" in str(e).lower() or "openai" in str(e).lower(), f"Unexpected error: {e}"
    
    print("✅ Message processing structure is correct")


def test_tool_registration():
    """Test that custom tools can be registered."""
    # Register the mock tool
    MockTool.register_all_tools()
    
    # Check that the tool was registered
    assert "mock_tool" in MockTool.get_all_tools()
    assert "mock_tool" in MockTool.get_all_schemas()
    
    # Test the tool directly
    result = MockTool.mock_tool("test", 42)
    assert result["success"] is True
    assert result["result"] == "Processed test with 42"
    
    print("✅ Tool registration works")


def test_state_management():
    """Test the agent state management."""
    # Create an agent state
    from agent.langgraph_agent import AgentState, Message
    
    state = AgentState(
        messages=[
            Message(role="system", content="System message"),
            Message(role="user", content="User message")
        ]
    )
    
    # Check that the state was created correctly
    assert len(state.messages) == 2
    assert state.messages[0].role == "system"
    assert state.messages[1].role == "user"
    
    print("✅ State management works")


def main():
    """Run all tests."""
    print("Testing LangGraph Agent...")
    
    test_agent_initialization()
    test_tool_loading()
    test_message_processing()
    test_tool_registration()
    test_state_management()
    
    print("\nAll tests passed! ✅")


if __name__ == "__main__":
    main() 