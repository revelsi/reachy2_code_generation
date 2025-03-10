#!/usr/bin/env python3
"""
Test script for the code generation agent with enhanced API summary generation.
This script allows testing with personalized user queries to evaluate the agent's
ability to generate accurate code with proper function calls.
"""

import os
import sys
import json
import argparse
import socket
import subprocess
from dotenv import load_dotenv
import time

# Add the parent directory to the path so we can import the agent module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

# Import the code generation agent and API summary functions
from agent.code_generation_agent import ReachyCodeGenerationAgent, load_api_documentation

# Patch the WebSocket notification method to avoid errors
import types
def dummy_send_notification(self, response):
    """Dummy method to replace the WebSocket notification method"""
    pass

def is_reachy_available(host="localhost", port=50051):
    """
    Check if the virtual Reachy robot is available by attempting to connect to its gRPC port.
    
    Args:
        host: The hostname where the virtual Reachy is running
        port: The gRPC port for the virtual Reachy (default is 50051)
        
    Returns:
        bool: True if the virtual Reachy is available, False otherwise
    """
    import socket
    
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        s.settimeout(2)
        # Attempt to connect
        result = s.connect_ex((host, port))
        # Close the socket
        s.close()
        # If result is 0, the connection was successful
        return result == 0
    except Exception as e:
        print(f"Error checking Reachy availability: {e}")
        return False

def execute_code_with_confirmation(agent, code, validation_result):
    """Execute the generated code with user confirmation."""
    # Ask for confirmation
    user_input = input("\nDo you want to execute this code on the virtual Reachy robot? (yes/no): ")
    
    if user_input.lower() in ["yes", "y"]:
        print("\nPreparing to execute code...")
        
        # Force execution even if validation failed
        force_execution = not validation_result["valid"]
        
        # Execute the code
        execution_result = agent.execute_code(code, confirm=False, force=force_execution)
        
        print("\nEXECUTION RESULTS:")
        print("-"*80)
        
        if execution_result["success"]:
            print("✅ Code executed successfully!")
        else:
            print(f"❌ Code execution failed: {execution_result.get('message', 'Unknown error')}")
        
        # Print output
        if execution_result.get("output"):
            print("\nOutput:")
            print(execution_result["output"])
        
        # Print stderr if available and not empty
        if execution_result.get("stderr") and execution_result["stderr"].strip():
            print("\nErrors/Warnings:")
            print(execution_result["stderr"])
        
        print("-"*80)
    else:
        print("\nCode execution skipped.")
    
    return

def main():
    """Main function to run the test script."""
    # Check if the virtual Reachy robot is available
    reachy_available = is_reachy_available()
    if not reachy_available:
        print("\n" + "=" * 80)
        print("⚠️ WARNING: Virtual Reachy robot is not available on default port!")
        print("=" * 80)
        print("The virtual Reachy robot simulator does not appear to be running on the default port.")
        print("This may cause connection issues during code execution.")
        print("=" * 80 + "\n")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test the code generation agent with API tools.")
    parser.add_argument('--model', type=str, default=os.getenv('MODEL', 'gpt-3.5-turbo'),
                        help='The OpenAI model to use (default: from MODEL env var or gpt-3.5-turbo)')
    parser.add_argument('--temperature', type=float, default=0.2,
                        help='The temperature parameter for the model (default: 0.2)')
    parser.add_argument('--max-tokens', type=int, default=2000,
                        help='The maximum number of tokens to generate (default: 2000)')
    args = parser.parse_args()
    
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in your .env file or export it in your shell.")
        sys.exit(1)
    
    # Create the code generation agent
    print(f"Initializing code generation agent with model: {args.model}")
    agent = ReachyCodeGenerationAgent(
        api_key=api_key,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    
    # Patch the WebSocket notification method
    agent._send_websocket_notification = types.MethodType(dummy_send_notification, agent)
    
    # Reset the conversation to apply the system prompt with enhanced API summary
    agent.reset_conversation()
    
    print("Code Generation Agent initialized successfully with enhanced API summary.")
    
    # Interactive mode
    print("\nEnter your requests, or type 'exit' to quit.")
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
        
        # Print the results
        print("\n" + "=" * 80)
        print("EXPLANATION:")
        print("=" * 80)
        print(response.get("message", "No explanation provided."))
        
        print("\n" + "=" * 80)
        print("GENERATED CODE:")
        print("=" * 80)
        print(generated_code)
        
        print("\n" + "=" * 80)
        print(f"VALIDATION: {'✅ Valid' if validation_result.get('valid', False) else '❌ Invalid'}")
        
        # Display correction attempts information if available
        correction_attempts = response.get("correction_attempts", 0)
        if correction_attempts > 0:
            print(f"\nCode was automatically corrected after {correction_attempts} attempt(s)")
            
        if validation_result.get("errors", []):
            print("\nErrors:")
            for error in validation_result.get("errors", []):
                print(f"- {error}")
        if validation_result.get("warnings", []):
            print("\nWarnings:")
            for warning in validation_result.get("warnings", []):
                print(f"- {warning}")
        print("=" * 80 + "\n")
        
        # Execute the code with confirmation
        execute_code_with_confirmation(agent, generated_code, validation_result)

if __name__ == "__main__":
    main()