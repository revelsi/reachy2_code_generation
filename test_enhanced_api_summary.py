#!/usr/bin/env python
"""
Test script for the enhanced API summary generation.

This script loads the API documentation, generates an enhanced summary,
and prints out the summary for inspection.
"""

import os
import sys
import json

# Add the agent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.code_generation_agent import load_api_documentation, generate_api_summary

def main():
    """
    Main function to test the enhanced API summary generation.
    """
    print("Loading API documentation...")
    api_docs = load_api_documentation()
    
    if not api_docs:
        print("Error: Could not load API documentation")
        return
    
    print(f"Loaded {len(api_docs)} API documentation items.")
    
    print("\nGenerating enhanced API summary...")
    enhanced_summary = generate_api_summary(api_docs)
    
    # Save the summary to a file for easier inspection
    output_path = "enhanced_api_summary.txt"
    with open(output_path, "w") as f:
        f.write(enhanced_summary)
    
    print(f"\nSaved enhanced API summary to {output_path}")
    
    # Test specific function details
    print("\nTesting parameter details extraction for key methods:")
    
    # Find Arm.goto method
    arm_goto_found = False
    for item in api_docs:
        if item.get("type") == "class" and item.get("name") == "Arm":
            for method in item.get("methods", []):
                if method.get("name") == "goto":
                    arm_goto_found = True
                    print("\nFound Arm.goto method:")
                    print(f"Signature: {method.get('signature', '')}")
                    
                    # Test parameter extraction
                    from agent.code_generation_agent import extract_parameter_details, add_special_constraints
                    param_details = extract_parameter_details(method.get('signature', ''), method.get('docstring', ''))
                    param_details = add_special_constraints("Arm", "goto", param_details)
                    
                    print("\nExtracted parameter details:")
                    for param_name, param_info in param_details.items():
                        print(f"\n- {param_name} ({param_info.get('type', '')}):")
                        print(f"  Description: {param_info.get('description', '')}")
                        
                        constraints = param_info.get('constraints', [])
                        if constraints:
                            print("  Constraints:")
                            for constraint in constraints:
                                print(f"    * {constraint}")
                        
                        if 'units' in param_info:
                            print(f"  Units: {param_info['units']}")
                    
                    break
            break
    
    if not arm_goto_found:
        print("Could not find Arm.goto method in API documentation.")
    
    # Find ReachySDK.__init__ method
    sdk_init_found = False
    for item in api_docs:
        if item.get("type") == "class" and item.get("name") == "ReachySDK":
            for method in item.get("methods", []):
                if method.get("name") == "__init__":
                    sdk_init_found = True
                    print("\nFound ReachySDK.__init__ method:")
                    print(f"Signature: {method.get('signature', '')}")
                    
                    # Test parameter extraction
                    from agent.code_generation_agent import extract_parameter_details, add_special_constraints
                    param_details = extract_parameter_details(method.get('signature', ''), method.get('docstring', ''))
                    param_details = add_special_constraints("ReachySDK", "__init__", param_details)
                    
                    print("\nExtracted parameter details:")
                    for param_name, param_info in param_details.items():
                        print(f"\n- {param_name} ({param_info.get('type', '')}):")
                        print(f"  Description: {param_info.get('description', '')}")
                        
                        constraints = param_info.get('constraints', [])
                        if constraints:
                            print("  Constraints:")
                            for constraint in constraints:
                                print(f"    * {constraint}")
                    
                    break
            break
    
    if not sdk_init_found:
        print("Could not find ReachySDK.__init__ method in API documentation.")

if __name__ == "__main__":
    main() 