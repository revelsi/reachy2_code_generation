#!/usr/bin/env python
"""
Debug script for investigating tool discovery issues in the Reachy Function Calling project.

This script helps diagnose why the ReachyToolMapper is not finding any tools.
"""

import os
import sys
import importlib
import inspect
import json
from pathlib import Path
from typing import Dict, Any, List, Type, Callable

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the tool mapper
from agent.tool_mapper import ReachyToolMapper

def inspect_directory(directory_path: str) -> None:
    """
    Inspect a directory for potential tool files.
    
    Args:
        directory_path: Path to the directory to inspect
    """
    print(f"\n=== Inspecting directory: {directory_path} ===")
    
    if not os.path.exists(directory_path):
        print(f"Directory does not exist: {directory_path}")
        return
    
    py_files = []
    for file in os.listdir(directory_path):
        if file.endswith(".py") and not file.startswith("__"):
            py_files.append(file)
    
    print(f"Found {len(py_files)} Python files: {', '.join(py_files)}")
    
    for file in py_files:
        inspect_file(os.path.join(directory_path, file))

def inspect_file(file_path: str) -> None:
    """
    Inspect a Python file for potential tool functions or classes.
    
    Args:
        file_path: Path to the Python file to inspect
    """
    print(f"\n--- Inspecting file: {os.path.basename(file_path)} ---")
    
    try:
        # Get the module name
        module_name = os.path.basename(file_path)[:-3]  # Remove .py extension
        
        # Add the directory to sys.path temporarily
        dir_path = os.path.dirname(file_path)
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)
        
        # Import the module
        module = importlib.import_module(module_name)
        
        # Find all functions and classes in the module
        functions = []
        classes = []
        
        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            
            if inspect.isfunction(obj):
                functions.append(name)
            elif inspect.isclass(obj):
                classes.append(name)
        
        print(f"Functions ({len(functions)}): {', '.join(functions)}")
        print(f"Classes ({len(classes)}): {', '.join(classes)}")
        
        # Remove the directory from sys.path
        if dir_path in sys.path:
            sys.path.remove(dir_path)
    
    except Exception as e:
        print(f"Error inspecting file: {e}")

def test_tool_mapper() -> None:
    """
    Test the ReachyToolMapper to see if it can discover and register tools.
    """
    print("\n=== Testing ReachyToolMapper ===")
    
    try:
        # Create a tool mapper instance
        mapper = ReachyToolMapper()
        
        # Print the initial state
        print(f"Initial tools: {len(mapper.tool_schemas)}")
        print(f"Initial implementations: {len(mapper.tool_implementations)}")
        
        # Discover and register tools
        print("\nAttempting to discover tool classes...")
        mapper.discover_tool_classes()
        
        print("\nAttempting to register tools from classes...")
        mapper.register_tools_from_classes()
        
        # Print the final state
        print(f"\nFinal tools: {len(mapper.tool_schemas)}")
        print(f"Final implementations: {len(mapper.tool_implementations)}")
        
        # Print the discovered tools
        if mapper.tool_schemas:
            print("\nDiscovered tools:")
            for name, schema in mapper.tool_schemas.items():
                print(f"  - {name}: {schema.get('function', {}).get('description', 'No description')}")
        else:
            print("\nNo tools were discovered.")
    
    except Exception as e:
        print(f"Error testing tool mapper: {e}")

def check_environment() -> None:
    """
    Check the environment for potential issues.
    """
    print("\n=== Checking Environment ===")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check PYTHONPATH
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
    
    # Check if the agent directory is in sys.path
    agent_dir = os.path.join(os.getcwd(), "agent")
    print(f"Agent directory in sys.path: {agent_dir in sys.path}")
    
    # Check if the tools directory exists
    tools_dir = os.path.join(os.getcwd(), "tools")
    print(f"Tools directory exists: {os.path.exists(tools_dir)}")
    
    # Check if the schemas directory exists
    schemas_dir = os.path.join(os.getcwd(), "agent", "schemas")
    print(f"Schemas directory exists: {os.path.exists(schemas_dir)}")

def main() -> None:
    """
    Main function to run the debug script.
    """
    print("=== Reachy Tool Discovery Debug Script ===")
    
    # Check the environment
    check_environment()
    
    # Inspect the tools directory
    tools_dir = os.path.join(os.getcwd(), "tools")
    inspect_directory(tools_dir)
    
    # Inspect the agent directory
    agent_dir = os.path.join(os.getcwd(), "agent")
    inspect_directory(agent_dir)
    
    # Test the tool mapper
    test_tool_mapper()
    
    print("\n=== Debug Script Complete ===")

if __name__ == "__main__":
    main() 