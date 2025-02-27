#!/usr/bin/env python
"""
Script to refresh the SDK documentation and regenerate tools.

This script:
1. Clones or updates the SDK repository
2. Extracts SDK documentation
3. Collects SDK examples
4. Saves the documentation and examples
"""

import sys
from agent.utils.scrape_sdk_docs import (
    clone_or_update_repo,
    extract_sdk_documentation,
    collect_sdk_examples,
    save_sdk_documentation
)

def main():
    """Main function to refresh the SDK documentation."""
    print("Starting SDK documentation refresh...")
    
    # Step 1: Clone/update the repository
    success = clone_or_update_repo()
    if not success:
        print("Failed to clone/update repository. Trying with force_clone=True...")
        success = clone_or_update_repo(force_clone=True)
        if not success:
            print("Failed to clone repository even with force_clone=True. Aborting.")
            return 1
    
    # Step 2: Extract SDK API documentation
    sdk_docs = extract_sdk_documentation()
    print(f"Extracted documentation for {len(sdk_docs)} items")
    
    # Step 3: Collect SDK examples
    examples = collect_sdk_examples()
    print(f"Collected {len(examples)} examples")
    
    # Step 4: Save documentation and examples
    save_sdk_documentation(sdk_docs, examples)
    
    print("\nSDK documentation refresh complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 