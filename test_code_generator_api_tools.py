#!/usr/bin/env python3
"""
Test script for the code generation agent with a modified prompt to use only API-documented tools.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the agent module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

# Import the code generation agent
from agent.code_generation_agent import ReachyCodeGenerationAgent

# Patch the WebSocket notification method to avoid errors
import types
def dummy_send_notification(self, response):
    """Dummy method to replace the WebSocket notification method"""
    pass

def load_api_documentation():
    """
    Load the API documentation from the JSON file.
    
    Returns:
        dict: The API documentation.
    """
    try:
        with open("agent/docs/api_documentation.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading API documentation: {e}")
        return []

def generate_api_summary(api_docs):
    """
    Generate a summary of the API documentation.
    
    Args:
        api_docs: The API documentation.
        
    Returns:
        str: A summary of the API documentation.
    """
    if not api_docs:
        return "No API documentation available."
    
    # Define the official API modules (these are the ones from the Reachy SDK)
    official_api_modules = [
        "reachy2_sdk.reachy_sdk",
        "reachy2_sdk.parts",
        "reachy2_sdk.utils",
        "reachy2_sdk.config",
        "reachy2_sdk.media",
        "reachy2_sdk.orbita",
        "reachy2_sdk.sensors"
    ]
    
    # Extract classes and their methods
    classes = {}
    official_modules = set()
    official_classes = set()
    
    for item in api_docs:
        # Track official modules (only if they're in the official list)
        if item.get("type") == "module":
            module_name = item.get("name")
            if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                official_modules.add(module_name)
        
        # Process classes (only if they're from official modules)
        if item.get("type") == "class":
            class_name = item.get("name")
            module_name = item.get("module", "")
            
            # Only include classes from official modules
            if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                # Add to official classes
                if class_name:
                    official_classes.add(class_name)
                
                methods = []
                
                # Get methods for this class
                for method in item.get("methods", []):
                    method_name = method.get("name")
                    signature = method.get("signature", "")
                    docstring = method.get("docstring", "").split("\n")[0] if method.get("docstring") else ""  # Get first line of docstring
                    
                    if method_name and not method_name.startswith("_"):  # Skip private methods
                        methods.append(f"- {method_name}{signature}: {docstring}")
                
                if methods:
                    classes[class_name] = methods
    
    # Format the summary
    summary = []
    
    # Add official modules
    summary.append("# Official Modules")
    for module in sorted(official_modules):
        summary.append(f"- {module}")
    summary.append("")
    
    # Add official classes
    summary.append("# Official Classes")
    for class_name in sorted(official_classes):
        summary.append(f"- {class_name}")
    summary.append("")
    
    # Add class methods
    summary.append("# Class Methods")
    for class_name, methods in classes.items():
        summary.append(f"## {class_name}")
        summary.append("\n".join(methods))
        summary.append("")
    
    return "\n".join(summary)

def main():
    """
    Main function to test the code generation agent with a modified prompt.
    """
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in your .env file or export it in your shell.")
        sys.exit(1)
    
    # Load API documentation
    api_docs = load_api_documentation()
    api_summary = generate_api_summary(api_docs)
    
    # Create the code generation agent
    agent = ReachyCodeGenerationAgent(
        api_key=api_key,
        model="gpt-3.5-turbo",  # Using a faster model for testing
        temperature=0.2,
        max_tokens=2000
    )
    
    # Patch the WebSocket notification method
    agent._send_websocket_notification = types.MethodType(dummy_send_notification, agent)
    
    # Update the system prompt to emphasize using only API-documented tools
    agent.system_prompt = f"""
    You are an AI assistant that generates Python code for controlling a Reachy 2 robot.
    
    OFFICIAL REACHY 2 SDK MODULES:
    - reachy2_sdk.reachy_sdk
    - reachy2_sdk.parts
    - reachy2_sdk.utils
    - reachy2_sdk.config
    - reachy2_sdk.media
    - reachy2_sdk.orbita
    - reachy2_sdk.sensors
    
    CRITICAL WARNINGS:
    - NEVER use 'get_reachy()' or any functions from 'connection_manager.py'
    - ALWAYS use properties correctly (e.g., reachy.r_arm NOT reachy.r_arm())
    - For arm goto(), ALWAYS provide EXACTLY 7 joint values
    
    REQUIRED CODE STRUCTURE:
    
    1. INITIALIZATION PHASE:
       - Import ReachySDK from reachy2_sdk.reachy_sdk
       - Connect to the robot: reachy = ReachySDK(host="localhost")
       - ALWAYS call reachy.turn_on() before any movement
    
    2. MAIN CODE PHASE:
       - Always use try/finally blocks for error handling
       - Access parts as properties (reachy.r_arm, reachy.head, etc.)
       - Use proper method signatures from the API documentation
    
    3. CLEANUP PHASE:
       - ALWAYS use reachy.turn_off_smoothly() (NOT turn_off())
       - ALWAYS call reachy.disconnect()
       - Put cleanup in a finally block
    
    EXAMPLE CODE TEMPLATE:
    ```python
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    # Connect to the robot
    reachy = ReachySDK(host="localhost")
    
    try:
        # INITIALIZATION
        reachy.turn_on()
        
        # MAIN CODE
        # Your code here...
        
    finally:
        # CLEANUP
        reachy.turn_off_smoothly()
        reachy.disconnect()
    ```
    
    Here is a summary of the available API classes and methods:
    
    {api_summary}
    
    Format your response with:
    1. A brief explanation of what the code does
    2. The complete Python code in a code block
    3. An explanation of how the code works and any important considerations
    """
    
    # Reset the conversation to apply the new system prompt
    agent.reset_conversation()
    
    print("Code Generation Agent initialized successfully with modified prompt.")
    print("Enter your requests, or type 'exit' to quit.")
    print()
    
    while True:
        # Get user input
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        
        # Process the user input
        print("\nGenerating code...")
        response = agent.process_message(user_input)
        
        # Check for errors
        if "error" in response:
            print(f"\nError: {response.get('message', 'Unknown error')}")
            continue
        
        # Extract the generated code and validation result
        generated_code = response.get("code", "No code generated.")
        validation_result = response.get("validation", {})
        is_valid = validation_result.get("valid", False)
        errors = validation_result.get("errors", [])
        warnings = validation_result.get("warnings", [])
        explanation = response.get("message", "No explanation provided.")
        
        # Print the results
        print("\n" + "=" * 80)
        print("EXPLANATION:")
        print("=" * 80)
        print(explanation)
        
        print("\n" + "=" * 80)
        print("GENERATED CODE:")
        print("=" * 80)
        print(generated_code)
        
        print("\n" + "=" * 80)
        print(f"VALIDATION: {'✅ Valid' if is_valid else '❌ Invalid'}")
        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"- {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- {warning}")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    main() 