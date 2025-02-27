#!/usr/bin/env python
"""
Test script for the ReachyToolMapper.

This script tests the functionality of the ReachyToolMapper class to ensure
it correctly discovers, registers, and formats tools for use with LangChain/LangGraph.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Configure path to include the agent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.dirname(current_dir)
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

# Import the tool mapper
from agent.utils.tool_mapper import ReachyToolMapper


def test_tool_mapper():
    """Test the ReachyToolMapper functionality."""
    print("Testing ReachyToolMapper...")
    
    # Create a tool mapper instance
    mapper = ReachyToolMapper()
    
    # Discover tool classes
    print("\nDiscovering tool classes...")
    tool_classes = mapper.discover_tool_classes()
    print(f"Discovered {len(tool_classes)} tool classes")
    
    # Register tools from classes
    print("\nRegistering tools from classes...")
    num_tools = mapper.register_tools_from_classes(tool_classes)
    print(f"Registered {num_tools} tools")
    
    # Get tool schemas and implementations
    tool_schemas = mapper.get_tool_schemas()
    tool_implementations = mapper.get_tool_implementations()
    
    print(f"\nGot {len(tool_schemas)} tool schemas and {len(tool_implementations)} tool implementations")
    
    # Verify tool schemas are in the correct format
    print("\nVerifying tool schema format...")
    valid_count = 0
    for name, schema in zip(range(len(tool_schemas)), tool_schemas):
        # Check if the schema is in the correct format
        if (isinstance(schema, dict) and 
            schema.get("type") == "function" and 
            "function" in schema and 
            "name" in schema["function"] and 
            "description" in schema["function"] and 
            "parameters" in schema["function"]):
            valid_count += 1
        else:
            print(f"Invalid schema format for tool {name}:")
            print(json.dumps(schema, indent=2))
    
    print(f"{valid_count}/{len(tool_schemas)} tool schemas are in the correct format")
    
    # Save tool definitions
    print("\nSaving tool definitions...")
    output_dir = os.path.join(current_dir, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "test_tools.json")
    
    success = mapper.save_tool_definitions(output_path)
    print(f"Saved tool definitions: {success}")
    
    # Try to load API documentation and map to tools
    print("\nLoading API documentation...")
    if mapper.load_api_documentation():
        print("Successfully loaded API documentation")
        
        # Map API to tools
        print("\nMapping API to tools...")
        tools = mapper.map_api_to_tools()
        print(f"Mapped {len(tools)} tools from API documentation")
        
        # Verify tool format
        print("\nVerifying mapped tool format...")
        valid_count = 0
        for name, tool in list(tools.items())[:5]:  # Check first 5 tools
            # Check if the tool is in the correct format
            if (isinstance(tool, dict) and 
                tool.get("type") == "function" and 
                "function" in tool and 
                "name" in tool["function"] and 
                "description" in tool["function"] and 
                "parameters" in tool["function"]):
                valid_count += 1
                print(f"Valid tool: {name}")
            else:
                print(f"Invalid tool format for {name}:")
                print(json.dumps(tool, indent=2))
        
        # Generate tool implementations
        print("\nGenerating tool implementations...")
        impl_dir = os.path.join(output_dir, "tools")
        success = mapper.generate_tool_implementations(impl_dir)
        print(f"Generated tool implementations: {success}")
    else:
        print("Failed to load API documentation")
    
    print("\nTool mapper test completed")


if __name__ == "__main__":
    test_tool_mapper() 