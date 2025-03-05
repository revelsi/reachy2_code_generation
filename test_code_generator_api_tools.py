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

def execute_code_directly(generated_code):
    """
    Execute the generated code directly in a separate process.
    This approach bypasses the agent's execution method and runs the code
    directly in the current environment, which may have better access to
    the Virtual Reachy in Docker.
    
    Args:
        generated_code: The code to execute
        
    Returns:
        dict: The execution result
    """
    try:
        # Create a temporary file for the code
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp_file:
            # Add a shebang line
            temp_file.write("#!/usr/bin/env python3\n")
            # Add imports for better error handling
            temp_file.write("import sys\n")
            temp_file.write("import traceback\n")
            temp_file.write("import os\n")
            temp_file.write("import time\n\n")
            
            # Add environment setup to ensure proper connection to Virtual Reachy
            temp_file.write("# Environment setup for Virtual Reachy connection\n")
            temp_file.write("os.environ['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__)) + ':' + os.environ.get('PYTHONPATH', '')\n")
            
            # Add connection retry logic
            temp_file.write("\n# Connection retry logic for Virtual Reachy\n")
            temp_file.write("def try_connect_to_reachy(max_retries=3, retry_delay=2):\n")
            temp_file.write("    from agent.tools.connection_manager import connect_to_reachy, get_connection_info\n")
            temp_file.write("    for attempt in range(max_retries):\n")
            temp_file.write("        try:\n")
            temp_file.write("            print(f'Connection attempt {attempt+1}/{max_retries}...')\n")
            temp_file.write("            reachy = connect_to_reachy(host='localhost')\n")
            temp_file.write("            info = get_connection_info()\n")
            temp_file.write("            print(f'Connection successful: {info}')\n")
            temp_file.write("            return reachy\n")
            temp_file.write("        except Exception as e:\n")
            temp_file.write("            print(f'Connection attempt {attempt+1} failed: {e}')\n")
            temp_file.write("            if attempt < max_retries - 1:\n")
            temp_file.write("                print(f'Retrying in {retry_delay} seconds...')\n")
            temp_file.write("                time.sleep(retry_delay)\n")
            temp_file.write("            else:\n")
            temp_file.write("                print('All connection attempts failed.')\n")
            temp_file.write("                raise\n\n")
            
            # Add error handling wrapper around the original code
            temp_file.write("try:\n")
            
            # Check if the code already has a connection to Reachy
            if "connect_to_reachy" in generated_code and "ReachySDK" not in generated_code:
                # The code uses our connection manager, so we'll use the retry function
                modified_code = generated_code.replace("connect_to_reachy(host='localhost')", "try_connect_to_reachy()")
                modified_code = modified_code.replace("connect_to_reachy(host=\"localhost\")", "try_connect_to_reachy()")
                # Indent the modified code
                indented_code = "    " + modified_code.replace("\n", "\n    ")
                temp_file.write(indented_code)
            elif "ReachySDK" in generated_code:
                # The code uses the SDK directly, add retry logic around it
                modified_code = generated_code.replace("ReachySDK(host='localhost')", 
                                                     "try_connect_to_reachy()")
                modified_code = modified_code.replace("ReachySDK(host=\"localhost\")", 
                                                     "try_connect_to_reachy()")
                # Indent the modified code
                indented_code = "    " + modified_code.replace("\n", "\n    ")
                temp_file.write(indented_code)
            else:
                # Just indent the original code
                indented_code = "    " + generated_code.replace("\n", "\n    ")
                temp_file.write(indented_code)
            
            # Add exception handling
            temp_file.write("\nexcept Exception as e:\n")
            temp_file.write("    print(f\"Error executing code: {e}\")\n")
            temp_file.write("    traceback.print_exc()\n")
            temp_file.write("    sys.exit(1)\n")
            
            temp_file_path = temp_file.name
        
        # Make the file executable
        os.chmod(temp_file_path, 0o755)
        
        print(f"\nExecuting code from temporary file: {temp_file_path}")
        
        # Execute the code in a separate process using the current Python interpreter
        process = subprocess.Popen(
            [sys.executable, temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ.copy()  # Pass the current environment variables
        )
        
        # Get the output with a timeout
        stdout, stderr = process.communicate(timeout=60)  # 60 second timeout
        
        # Clean up the temporary file
        try:
            os.unlink(temp_file_path)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file {temp_file_path}: {e}")
        
        # Check if the execution was successful
        success = process.returncode == 0
        
        return {
            "success": success,
            "output": stdout,
            "stderr": stderr,
            "return_code": process.returncode,
            "message": "Code executed successfully" if success else f"Code execution failed with return code {process.returncode}"
        }
        
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            "success": False,
            "output": "",
            "stderr": "Execution timed out after 60 seconds",
            "return_code": -1,
            "message": "Code execution timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "stderr": str(e),
            "return_code": -1,
            "message": f"Error executing code: {str(e)}"
        }

def execute_code_with_confirmation(agent, generated_code, is_valid, errors, warnings):
    """
    Helper function to execute code with user confirmation.
    
    Args:
        agent: The ReachyCodeGenerationAgent instance
        generated_code: The code to execute
        is_valid: Whether the code passed validation
        errors: List of validation errors
        warnings: List of validation warnings
        
    Returns:
        None
    """
    # Check if the virtual Reachy robot is available
    reachy_available = is_reachy_available()
    if not reachy_available:
        print("\n" + "=" * 80)
        print("⚠️ WARNING: Virtual Reachy robot is not available on default port!")
        print("=" * 80)
        print("The virtual Reachy robot simulator does not appear to be running on the default port.")
        print("This may cause connection issues during code execution.")
        print("=" * 80 + "\n")
    
    # Ask if the user wants to execute the code
    execute_choice = input("Do you want to execute this code on the virtual Reachy robot? (yes/no): ").strip().lower()
    if execute_choice not in ["yes", "y"]:
        print("Code execution skipped.")
        return
    
    # Prepare for execution
    print("\nPreparing to execute code...")
    
    # Allow execution even if validation failed
    force_execution = not is_valid
    if force_execution:
        print("\nWARNING: Code validation failed, but proceeding with execution as requested.")
        print("This may cause unexpected behavior or errors.")
    
    # Ask how the user wants to execute the code
    execution_method = input("\nHow would you like to execute the code?\n1. Use direct execution (recommended)\n2. Use agent's execution method\n3. Save to a file for manual execution\nEnter choice (1/2/3): ").strip()
    
    if execution_method == "3":
        # Save the code to a file
        filename = "generated_reachy_code.py"
        with open(filename, "w") as f:
            # Add a shebang line and make the file executable
            f.write("#!/usr/bin/env python3\n")
            f.write("# Generated code for Reachy robot\n\n")
            f.write(generated_code)
        
        # Make the file executable
        os.chmod(filename, 0o755)
        
        print(f"\nCode saved to {filename}")
        print("You can execute it manually with:")
        print(f"  python {filename}")
        return
    
    if execution_method == "1":
        # Use direct execution
        print("\n" + "=" * 80)
        print("CODE READY FOR EXECUTION")
        print("=" * 80)
        print("The following code will be executed directly:")
        print("\n" + "-" * 40)
        print(generated_code)
        print("-" * 40 + "\n")
        
        if not is_valid:
            print("\nWARNING: This code did not pass validation. Execute at your own risk.")
            if errors:
                print("\nErrors:")
                for error in errors:
                    print(f"- {error}")
            if warnings:
                print("\nWarnings:")
                for warning in warnings:
                    print(f"- {warning}")
        
        # Final confirmation
        final_confirm = input("Are you sure you want to execute this code? (yes/no): ").strip().lower()
        if final_confirm not in ["yes", "y"]:
            print("Code execution cancelled.")
            return
        
        # Execute the code directly
        print("\nExecuting code directly...")
        execution_result = execute_code_directly(generated_code)
    else:
        # Use the agent's execution method
        execution_result = agent.execute_code(generated_code, confirm=True, force=force_execution)
        
        # Check if confirmation is required
        if execution_result.get("requires_confirmation", False):
            print("\n" + "=" * 80)
            print("CODE READY FOR EXECUTION")
            print("=" * 80)
            print("The following code will be executed on the virtual Reachy robot:")
            print("\n" + "-" * 40)
            print(execution_result.get("safe_code", generated_code))
            print("-" * 40 + "\n")
            
            if not is_valid:
                print("\nWARNING: This code did not pass validation. Execute at your own risk.")
                if errors:
                    print("\nErrors:")
                    for error in errors:
                        print(f"- {error}")
                if warnings:
                    print("\nWarnings:")
                    for warning in warnings:
                        print(f"- {warning}")
            
            # Final confirmation
            final_confirm = input("Are you sure you want to execute this code? (yes/no): ").strip().lower()
            if final_confirm not in ["yes", "y"]:
                print("Code execution cancelled.")
                return
            
            # Execute the code
            print("\nExecuting code...")
            execution_result = agent.execute_code(generated_code, confirm=False, force=force_execution)
    
    # Display execution results
    print("\n" + "=" * 80)
    print("EXECUTION RESULTS:")
    print("=" * 80)
    if execution_result.get("success", False):
        print("✅ Code executed successfully!")
    else:
        print("❌ Code execution failed!")
    
    if execution_result.get("output"):
        print("\nOutput:")
        print("-" * 40)
        print(execution_result.get("output", "No output"))
        print("-" * 40)
    
    if execution_result.get("stderr"):
        print("\nErrors:")
        print("-" * 40)
        print(execution_result.get("stderr"))
        print("-" * 40)
    
    print("\nMessage:", execution_result.get("message", "No message"))
    
    if execution_result.get("critical_warnings"):
        print("\nCritical Warnings:")
        for warning in execution_result.get("critical_warnings", []):
            print(f"- {warning}")
    
    print("=" * 80 + "\n")

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
        
        # Execute the code with confirmation
        execute_code_with_confirmation(agent, generated_code, is_valid, errors, warnings)

if __name__ == "__main__":
    main()