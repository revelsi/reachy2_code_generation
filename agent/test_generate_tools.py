#!/usr/bin/env python
"""
Test script to generate tool definitions and implementations.

This script uses the ReachyToolMapper to generate tool definitions and implementations
without requiring an OpenAI API key.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.agent.tool_mapper import ReachyToolMapper


def generate_tools(focus_modules=None):
    """
    Generate tool definitions and implementations.
    
    Args:
        focus_modules: Optional list of module names to focus on.
    """
    # Default modules to focus on for basic robot control
    if focus_modules is None:
        focus_modules = ["parts", "orbita", "utils"]
    
    print(f"Generating tools for modules: {focus_modules}")
    
    # Create tool mapper
    mapper = ReachyToolMapper()
    
    # Load API documentation
    print("\nLoading API documentation...")
    if not mapper.load_api_documentation():
        print("Failed to load API documentation. Exiting.")
        return False
    
    # Map API to tools
    print("\nMapping API to tools...")
    tools = mapper.map_api_to_tools(focus_modules=focus_modules)
    
    if not tools:
        print("No tools were generated. Exiting.")
        return False
    
    # Print some statistics
    print(f"\nGenerated {len(tools)} tool definitions.")
    
    # Group tools by module
    modules = {}
    for tool_name, tool_info in tools.items():
        module = tool_info.get("module", "").replace("reachy2_sdk.", "")
        module = module.split(".")[0] if module else "misc"
        
        if module not in modules:
            modules[module] = []
            
        modules[module].append(tool_name)
    
    # Print tools by module
    print("\nTools by module:")
    for module, module_tools in modules.items():
        print(f"  {module}: {len(module_tools)} tools")
        for tool in module_tools[:5]:  # Print first 5 tools per module
            print(f"    - {tool}")
        if len(module_tools) > 5:
            print(f"    - ... and {len(module_tools) - 5} more")
    
    # Save tool schemas
    print("\nSaving tool schemas...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemas_dir = os.path.join(current_dir, "schemas")
    os.makedirs(schemas_dir, exist_ok=True)
    
    mapper.save_tool_schemas()
    
    # Generate tool implementations
    print("\nGenerating tool implementations...")
    tools_dir = os.path.join(current_dir, "tools")
    os.makedirs(tools_dir, exist_ok=True)
    
    mapper.generate_tool_implementations(tools_dir)
    
    # Count generated files
    implementation_files = [f for f in os.listdir(tools_dir) if f.endswith(".py")]
    print(f"\nGenerated {len(implementation_files)} implementation files:")
    for file in implementation_files:
        print(f"  - {file}")
    
    print("\nTool generation completed successfully!")
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Reachy 2 tool definitions and implementations")
    parser.add_argument("--focus", nargs="+", help="Focus on specific modules (e.g., parts orbita)")
    
    args = parser.parse_args()
    
    generate_tools(focus_modules=args.focus) 