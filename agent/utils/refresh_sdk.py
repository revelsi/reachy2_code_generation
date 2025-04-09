#!/usr/bin/env python
"""
Script to refresh the SDK documentation and regenerate tools.

This script integrates the complete pipeline:
1. scrape_sdk_docs.py: Clones/updates repositories and extracts raw documentation
2. tool_mapper.py: Processes raw documentation to create optimized API documentation
3. integrate_tools.py: Generates tool definitions and implementations

This ensures all components are properly synchronized.
"""

import os
import sys
from agent.utils.scrape_sdk_docs import (
    clone_or_update_repo,
    extract_sdk_documentation,
    collect_sdk_examples,
    save_sdk_documentation,
    should_extract_vision_documentation,
    extract_vision_documentation,
    REACHY_SDK_GIT_URL,
    REPO_DIR,
    POLLEN_VISION_GIT_URL,
    VISION_REPO_DIR
)

def main():
    """Main function to refresh the SDK documentation and tools."""
    print("Starting SDK documentation refresh and tool generation pipeline...")
    
    #########################################
    # STEP 1: Generate Raw API Documentation
    #########################################
    print("\n=== PHASE 1: Raw API Documentation Generation ===")
    
    # Clone/update the SDK repository
    success = clone_or_update_repo(REACHY_SDK_GIT_URL, REPO_DIR)
    if not success:
        print("Failed to clone/update SDK repository. Trying with force_clone=True...")
        success = clone_or_update_repo(REACHY_SDK_GIT_URL, REPO_DIR, force_clone=True)
        if not success:
            print("Failed to clone SDK repository even with force_clone=True. Aborting.")
            return 1
    
    # Check if we should extract vision documentation
    extract_vision = should_extract_vision_documentation()
    vision_docs = None
    
    if extract_vision:
        print("Vision documentation extraction requested.")
        # Clone/update the pollen-vision repository
        success = clone_or_update_repo(POLLEN_VISION_GIT_URL, VISION_REPO_DIR)
        if not success:
            print("Failed to clone/update pollen-vision repository. Trying with force_clone=True...")
            success = clone_or_update_repo(POLLEN_VISION_GIT_URL, VISION_REPO_DIR, force_clone=True)
            if not success:
                print("Failed to clone pollen-vision repository even with force_clone=True.")
                print("Will continue without vision documentation.")
                extract_vision = False
    else:
        print("Vision documentation extraction not requested. Skipping.")
    
    # Extract SDK API documentation
    sdk_docs = extract_sdk_documentation()
    print(f"Extracted documentation for {len(sdk_docs)} items from Reachy 2 SDK")
    
    # Extract vision API documentation if requested
    if extract_vision:
        vision_docs = extract_vision_documentation()
        print(f"Extracted documentation for {len(vision_docs)} items from pollen-vision")
    
    # Collect SDK examples
    examples = collect_sdk_examples()
    print(f"Collected {len(examples)} examples")
    
    # Save raw documentation and examples
    save_sdk_documentation(sdk_docs, examples, vision_docs)
    print("Raw API documentation generation complete.")
    
    ############################################
    # STEP 2: Process and Optimize Documentation
    ############################################
    print("\n=== PHASE 2: API Documentation Processing ===")
    
    try:
        from agent.utils.tool_mapper import ReachyToolMapper
        
        # Create tool mapper
        mapper = ReachyToolMapper()
        
        # Load and process API documentation
        doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "api_documentation.json")
        if not mapper.load_api_documentation(doc_path):
            print("Failed to load and process API documentation. Aborting.")
            return 1
        
        print("API documentation processing complete.")
    except Exception as e:
        print(f"Error processing API documentation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    ###########################################
    # STEP 3: Generate Tool Definitions
    ###########################################
    print("\n=== PHASE 3: Tool Generation ===")
    
    try:
        from agent.utils.integrate_tools import main as integrate_tools_main
        
        # Run the integrate_tools main function
        print("Generating tool definitions and implementations...")
        if not integrate_tools_main():
            print("Failed to generate tool definitions and implementations. Aborting.")
            return 1
            
        print("Tool generation complete.")
    except Exception as e:
        print(f"Error generating tools: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\nComplete SDK refresh and tool generation pipeline finished successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 