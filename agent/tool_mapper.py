#!/usr/bin/env python
"""
Tool mapper for Reachy 2 agent.

This module provides functionality for mapping Reachy 2 tools to LLM-compatible tools,
generating tool schemas, and registering tools with the agent.
"""

import os
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Type, Callable, Optional, Union

# Configure path to include the agent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.dirname(current_dir)
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

# Output directories
SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "schemas")
os.makedirs(SCHEMAS_DIR, exist_ok=True)


class ReachyToolMapper:
    """
    Maps Reachy 2 tools to agent tools.
    
    This class loads tool classes and registers their tools with the agent.
    """
    
    def __init__(self):
        self.tools = {}
        self.tool_implementations = {}
        self.tool_classes = []
        
    def discover_tool_classes(self, tools_dir: str = None) -> List[Type]:
        """
        Discover tool classes in the tools directory.
        
        Args:
            tools_dir: Directory containing tool classes. If None, uses the default tools directory.
            
        Returns:
            List[Type]: List of discovered tool classes.
        """
        if tools_dir is None:
            tools_dir = os.path.join(os.path.dirname(__file__), "tools")
        
        tool_classes = []
        
        # Get all Python files in the tools directory
        for file_path in Path(tools_dir).glob("*.py"):
            if file_path.name.startswith("__"):
                continue
                
            # Import the module
            module_name = f"agent.tools.{file_path.stem}"
            try:
                module = importlib.import_module(module_name)
                
                # Find all classes in the module that inherit from BaseTool
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        name != "BaseTool" and 
                        hasattr(obj, "register_all_tools")):
                        tool_classes.append(obj)
                        print(f"Discovered tool class: {name}")
            except Exception as e:
                print(f"Error importing {module_name}: {e}")
        
        self.tool_classes = tool_classes
        return tool_classes
    
    def register_tools_from_classes(self) -> int:
        """
        Register tools from discovered tool classes.
        
        Returns:
            int: Number of tools registered.
        """
        self.tools = {}
        self.tool_implementations = {}
        count = 0
        
        for tool_class in self.tool_classes:
            # Register all tools in the class
            tool_class.register_all_tools()
            
            # Get the registered tools and schemas
            class_tools = tool_class.get_all_tools()
            class_schemas = tool_class.get_all_schemas()
            
            # Add to our dictionaries
            self.tool_implementations.update(class_tools)
            
            # Convert schemas to OpenAI function calling format
            for name, schema in class_schemas.items():
                self.tools[name] = {
                    "type": "function",
                    "function": schema
                }
                count += 1
        
        print(f"Registered {count} tools from {len(self.tool_classes)} tool classes")
        return count
    
    def save_tool_definitions(self, output_file: str) -> bool:
        """
        Save tool definitions to a JSON file.
        
        Args:
            output_file: Path to the output JSON file.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Write to file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.tools, f, indent=2)
                
            print(f"Saved {len(self.tools)} tool definitions to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving tool definitions: {e}")
            return False
    
    def get_tool_schemas(self) -> Dict[str, Any]:
        """
        Get all tool schemas.
        
        Returns:
            Dict[str, Any]: Dictionary of tool schemas.
        """
        return self.tools
    
    def get_tool_implementations(self) -> Dict[str, Callable]:
        """
        Get all tool implementations.
        
        Returns:
            Dict[str, Callable]: Dictionary of tool implementations.
        """
        return self.tool_implementations


if __name__ == "__main__":
    # Example usage
    mapper = ReachyToolMapper()
    mapper.discover_tool_classes()
    mapper.register_tools_from_classes()
    mapper.save_tool_definitions(os.path.join(SCHEMAS_DIR, "reachy_tools.json")) 