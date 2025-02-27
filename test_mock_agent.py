#!/usr/bin/env python
"""
Test script for the ReachyLangGraphAgent in mock mode.
This script creates an instance of the agent and sends a test message to it.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the agent
from agent.langgraph_agent import ReachyLangGraphAgent

def main():
    """Run a test of the ReachyLangGraphAgent in mock mode."""
    print("Creating ReachyLangGraphAgent...")
    agent = ReachyLangGraphAgent(model="gpt-4-turbo")
    
    print(f"Agent created with {len(agent.tools)} tools and {len(agent.tool_implementations)} implementations")
    
    # Test message
    test_message = "Can you move the robot's right arm up by 20 degrees?"
    print(f"\nSending test message: '{test_message}'")
    
    # Process the message
    response = agent.process_message(test_message)
    
    # Print the response
    print("\nResponse:")
    print(f"Message: {response.get('message')}")
    
    # Print tool calls
    print("\nTool Calls:")
    for i, tool_call in enumerate(response.get("tool_calls", [])):
        print(f"\nTool Call {i+1}:")
        print(f"  Name: {tool_call.get('name')}")
        print(f"  Arguments: {json.dumps(tool_call.get('arguments'), indent=2)}")
        print(f"  Result: {json.dumps(tool_call.get('result'), indent=2)}")
    
    # Check if there was an error
    if response.get("error"):
        print(f"\nError: {response.get('error')}")

if __name__ == "__main__":
    main() 