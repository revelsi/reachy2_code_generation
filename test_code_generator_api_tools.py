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
from dotenv import load_dotenv

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

def main():
    """
    Main function to test the code generation agent with enhanced API summary.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test the code generation agent with enhanced API summary')
    parser.add_argument('--model', type=str, default=os.getenv('MODEL', 'gpt-3.5-turbo'),
                        help='The OpenAI model to use (default: from MODEL env var or gpt-3.5-turbo)')
    parser.add_argument('--temperature', type=float, default=0.2,
                        help='The temperature parameter for the model (default: 0.2)')
    parser.add_argument('--max-tokens', type=int, default=2000,
                        help='The maximum number of tokens to generate (default: 2000)')
    parser.add_argument('--test-queries', action='store_true',
                        help='Run predefined test queries instead of interactive mode')
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
    
    # Define test queries that target specific API functions with complex parameters
    test_queries = [
        "Move the right arm to a specific position with joint values [0, 0, 0, 0, 0, 0, 0] in degrees",
        "Initialize the robot with host 'localhost' and connect to it",
        "Make the robot look at a point in space at coordinates (0.5, 0.3, 0.2)",
        "Move the robot's right arm to a Cartesian position using a 4x4 transformation matrix",
        "Turn on the robot, move the left arm to a joint position of [10, 20, 30, 40, 50, 60, 70] degrees, wait for 2 seconds, then turn off",
        "Make the robot's head track a moving object at coordinates that change from (0.3, 0.2, 0.5) to (0.5, 0.3, 0.2) over 3 seconds",
        "Create a program that makes the robot wave its right hand by moving the wrist joint back and forth 3 times",
        "Move the mobile base forward 1 meter, then turn 90 degrees to the right",
        "Get the current positions of all joints in the right arm and print them",
        "Create a function that checks if a position is reachable by the right arm using inverse kinematics"
    ]
    
    if args.test_queries:
        # Run predefined test queries
        print("\nRunning predefined test queries...")
        
        for i, query in enumerate(test_queries):
            print(f"\n\n{'='*80}")
            print(f"TEST QUERY {i+1}/{len(test_queries)}:")
            print(f"{query}")
            print(f"{'='*80}\n")
            
            # Process the query
            response = agent.process_message(query)
            
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
            print("\n" + "-" * 80)
            print("EXPLANATION:")
            print("-" * 80)
            print(explanation)
            
            print("\n" + "-" * 80)
            print("GENERATED CODE:")
            print("-" * 80)
            print(generated_code)
            
            print("\n" + "-" * 80)
            print(f"VALIDATION: {'✅ Valid' if is_valid else '❌ Invalid'}")
            if errors:
                print("\nErrors:")
                for error in errors:
                    print(f"- {error}")
            if warnings:
                print("\nWarnings:")
                for warning in warnings:
                    print(f"- {warning}")
            print("-" * 80 + "\n")
            
        print("\nAll test queries completed.")
    
    else:
        # Interactive mode
        print("\nEnter your requests, or type 'exit' to quit.")
        print("Type 'test' to run a predefined test query by number (1-10).")
        print()
        
        while True:
            # Get user input
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            # Check if user wants to run a test query
            if user_input.lower().startswith("test"):
                try:
                    # Extract test query number
                    parts = user_input.split()
                    if len(parts) > 1 and parts[1].isdigit():
                        query_num = int(parts[1])
                        if 1 <= query_num <= len(test_queries):
                            user_input = test_queries[query_num - 1]
                            print(f"\nRunning test query {query_num}:")
                            print(f"{user_input}")
                        else:
                            print(f"Invalid test query number. Please use a number between 1 and {len(test_queries)}.")
                            continue
                    else:
                        print("Available test queries:")
                        for i, query in enumerate(test_queries):
                            print(f"{i+1}. {query}")
                        continue
                except Exception as e:
                    print(f"Error parsing test query: {e}")
                    continue
            
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