#!/usr/bin/env python
"""
Verify the tool generation process.

This script checks that the tool generation process is working correctly by:
1. Verifying that the API documentation is loaded
2. Checking that tools are generated
3. Confirming that tool implementations are created
"""

import os
import json
import sys
from pathlib import Path

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the tool mapper
from agent.utils.tool_mapper import ReachyToolMapper

def verify_api_documentation():
    """Verify that the API documentation is loaded."""
    print("\nVerifying API documentation...")
    
    doc_path = os.path.join("agent", "docs", "api_documentation.json")
    if not os.path.exists(doc_path):
        print(f"Error: API documentation not found at {doc_path}")
        return False
    
    try:
        with open(doc_path, 'r') as f:
            docs = json.load(f)
        
        print(f"API documentation loaded: {len(docs)} items")
        return True
    except Exception as e:
        print(f"Error loading API documentation: {e}")
        return False

def verify_tool_schemas():
    """Verify that tool schemas are generated."""
    print("\nVerifying tool schemas...")
    
    schema_path = os.path.join("agent", "schemas", "reachy_tools.json")
    if not os.path.exists(schema_path):
        print(f"Error: Tool schemas not found at {schema_path}")
        return False
    
    try:
        with open(schema_path, 'r') as f:
            schemas = json.load(f)
        
        print(f"Tool schemas loaded: {len(schemas)} tools")
        
        # Group tools by module
        modules = {}
        for tool_name, tool_info in schemas.items():
            module = tool_info.get("module", "").replace("reachy2_sdk.", "")
            module = module.split(".")[0] if module else "misc"
            
            if module not in modules:
                modules[module] = []
                
            modules[module].append(tool_name)
        
        # Print tools by module
        print("\nTools by module:")
        for module, tool_names in sorted(modules.items()):
            print(f"{module}: {len(tool_names)} tools")
        
        return True
    except Exception as e:
        print(f"Error loading tool schemas: {e}")
        return False

def verify_tool_implementations():
    """Verify that tool implementations are created."""
    print("\nVerifying tool implementations...")
    
    tools_dir = os.path.join("agent", "tools")
    if not os.path.exists(tools_dir):
        print(f"Error: Tools directory not found at {tools_dir}")
        return False
    
    # Check for tool implementation files
    tool_files = [f for f in os.listdir(tools_dir) if f.endswith("_tools.py")]
    if not tool_files:
        print("Error: No tool implementation files found")
        return False
    
    print(f"Tool implementation files found: {len(tool_files)}")
    for file in tool_files:
        file_path = os.path.join(tools_dir, file)
        size = os.path.getsize(file_path) / 1024  # Size in KB
        print(f"  - {file} ({size:.1f} KB)")
    
    return True

def main():
    """Main verification function."""
    print("Starting tool verification...")
    
    # Verify API documentation
    if not verify_api_documentation():
        print("API documentation verification failed")
        return False
    
    # Verify tool schemas
    if not verify_tool_schemas():
        print("Tool schema verification failed")
        return False
    
    # Verify tool implementations
    if not verify_tool_implementations():
        print("Tool implementation verification failed")
        return False
    
    print("\nTool verification completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 