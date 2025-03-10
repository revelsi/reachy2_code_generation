#!/usr/bin/env python
"""
Simple script to launch the Reachy 2 Code Generation Interface.
"""
import os
import sys

def main():
    """Main function to launch the code generation interface."""
    print("\n==========================================================")
    print("         REACHY 2 CODE GENERATION INTERFACE")
    print("==========================================================")
    print("\nStarting the Reachy 2 Code Generation Interface...")
    print("This interface allows you to generate Python code for the Reachy 2 robot using natural language.")
    print("\nModel: GPT-4o-mini (optimized for Reachy 2 code generation)")
    print("\nCode Validation Process:")
    print("1. Syntax Check: Ensures the code has valid Python syntax")
    print("2. Import Validation: Verifies all imports are available")
    print("3. API Usage Check: Confirms correct usage of the Reachy API")
    print("4. Safety Check: Looks for potentially harmful operations")
    print("\nWhen issues are found, the model will attempt to fix them automatically.")
    print("\nLoading web interface...")
    print("Once loaded, you can access it in your web browser.")
    
    # Import the code generation interface
    from agent.code_generation_interface import main as run_interface
    
    # Run the interface
    run_interface()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1) 