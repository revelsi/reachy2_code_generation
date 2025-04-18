#!/usr/bin/env python
"""
Integration script for the Reachy tool mapper.

This script creates a fresh set of tools by:
1. Extracting SDK documentation
2. Generating tool definitions
3. Generating tool implementations
4. Saving everything to the appropriate locations
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the tool mapper
from agent.utils.tool_mapper import ReachyToolMapper

# Configuration
SCHEMAS_DIR = os.path.join(parent_dir, "schemas")
TOOLS_DIR = os.path.join(parent_dir, "tools")
DOCS_DIR = os.path.join(parent_dir, "docs")

def clean_directory(directory: str):
    """
    Clean a directory by removing all files except __init__.py and base_tool.py.
    
    Args:
        directory: Directory to clean.
    """
    if not os.path.exists(directory):
        return
        
    for item in os.listdir(directory):
        if item in ["__init__.py", "base_tool.py", "__pycache__", "scrape_sdk_docs.py", "mock_reachy.py", "connection_manager.py"]:
            continue
        
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def main():
    """Main integration function."""
    print("Starting fresh tool generation...")
    
    # Clean existing directories
    print("\nCleaning existing tool files...")
    clean_directory(TOOLS_DIR)
    clean_directory(SCHEMAS_DIR)
    
    # Path to the raw API documentation
    raw_docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                "data/raw_docs/extracted/raw_api_docs.json")
    
    # Check if we need to generate raw documentation
    if not os.path.exists(raw_docs_path):
        # Step 1: Generate raw API documentation using scrape_sdk_docs.py
        try:
            print("\nGenerating raw API documentation...")
            from agent.utils.scrape_sdk_docs import extract_sdk_documentation, save_sdk_documentation, collect_sdk_examples
            
            # Extract documentation from SDK
            sdk_docs = extract_sdk_documentation()
            if not sdk_docs:
                print("Failed to extract SDK documentation. Exiting.")
                return False
            
            # Collect SDK examples
            examples = collect_sdk_examples()
            
            # Save raw documentation
            save_sdk_documentation(sdk_docs, examples)
            print("Raw API documentation generation complete.")
        except Exception as e:
            print(f"Error generating raw API documentation: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print(f"\nRaw API documentation already exists at {raw_docs_path}")
        print("Skipping raw documentation generation and using existing file.")
    
    # Step 2: Process the raw documentation with tool_mapper.py
    print("\nProcessing API documentation...")
    
    # Create tool mapper
    mapper = ReachyToolMapper()
    
    # Load and process API documentation
    doc_path = os.path.join(DOCS_DIR, "api_documentation.json")
    if not mapper.load_api_documentation(doc_path):
        print("Failed to load and process API documentation. Exiting.")
        return False
    
    # Step 3: Map API to tools
    print("\nMapping API to tools...")
    tools = mapper.map_api_to_tools()
    
    if not tools:
        print("No tools were generated. Exiting.")
        return False
    
    # Store tools in mapper
    mapper.tool_schemas = tools
    
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
    for module, tool_names in sorted(modules.items()):
        print(f"{module}: {len(tool_names)} tools")
    
    # Step 4: Save tool definitions
    print("\nSaving tool definitions...")
    tools_file = os.path.join(SCHEMAS_DIR, "reachy_tools.json")
    
    try:
        with open(tools_file, "w") as f:
            json.dump(tools, f, indent=2)
        print(f"Saved tool definitions to {tools_file}")
    except Exception as e:
        print(f"Error saving tool definitions: {e}")
        return False
    
    # Step 5: Generate tool implementations
    print("\nGenerating tool implementations...")
    try:
        if not mapper.generate_tool_implementations(TOOLS_DIR):
            print("Failed to generate tool implementations.")
            return False
        print("Successfully generated tool implementations.")
    except Exception as e:
        print(f"Error generating tool implementations: {e}")
        return False
    
    print("\nTool generation completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 