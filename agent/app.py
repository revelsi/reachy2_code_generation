#!/usr/bin/env python
"""
Core application functionality for the Reachy 2 Code Generation Pipeline.

This module provides the main application logic for generating, evaluating, and optimizing
Python code for the Reachy 2 robot, supporting both CLI and UI modes.
"""

import os
import sys
import logging
import time
import traceback
import tempfile
import importlib
import subprocess
from typing import Dict, Any, Optional, Union

# Configure logging
logger = logging.getLogger("reachy_app")

# Import configuration
from config import OPENAI_API_KEY, MODEL, EVALUATOR_MODEL

def launch_ui(
    api_key: Optional[str] = None,
    generator_model: str = MODEL,
    evaluator_model: str = EVALUATOR_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4000,
    max_iterations: int = 2,
    evaluation_threshold: float = 75.0,
    port: int = 7860,
    share: bool = False
) -> None:
    """
    Launch the Gradio web interface.
    
    Args:
        api_key: The OpenAI API key.
        generator_model: The model to use for code generation.
        evaluator_model: The model to use for code evaluation.
        temperature: The temperature for generation.
        max_tokens: The maximum number of tokens to generate.
        max_iterations: The maximum number of optimization iterations.
        evaluation_threshold: The evaluation threshold.
        port: The port to run the Gradio server on.
        share: Whether to create a public share link.
    """
    try:
        from agent.code_generation_interface import CodeGenerationInterface
        
        # Create the interface
        interface = CodeGenerationInterface(
            api_key=api_key or os.environ.get("OPENAI_API_KEY") or OPENAI_API_KEY,
            model=generator_model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_iterations=max_iterations,
            evaluation_threshold=evaluation_threshold
        )
        
        # Launch the interface
        logger.info(f"Launching Gradio interface on port {port} with share={share}")
        interface.launch_interface(share=share, port=port)
    except Exception as e:
        logger.error(f"Error launching UI: {e}")
        logger.error(traceback.format_exc())
        raise RuntimeError(f"Failed to launch UI: {e}")

def run_code_generation(
    request: Optional[str] = None,
    api_key: Optional[str] = None,
    generator_model: str = MODEL,
    evaluator_model: str = EVALUATOR_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4000,
    optimize: bool = True,
    max_iterations: int = 2,
    evaluation_threshold: float = 75.0,
    execute: bool = False,
    quiet: bool = False
) -> Dict[str, Any]:
    """
    Run the code generation pipeline from the command line.
    
    Args:
        request: The natural language request.
        api_key: The OpenAI API key.
        generator_model: The model to use for code generation.
        evaluator_model: The model to use for code evaluation.
        temperature: The temperature for generation.
        max_tokens: The maximum number of tokens to generate.
        optimize: Whether to optimize the generated code.
        max_iterations: The maximum number of optimization iterations.
        evaluation_threshold: The evaluation threshold.
        execute: Whether to execute the generated code.
        quiet: Whether to minimize output.
        
    Returns:
        Dict[str, Any]: The result of the code generation pipeline.
    """
    # Get the API key
    api_key = api_key or os.environ.get("OPENAI_API_KEY") or OPENAI_API_KEY
    
    if not api_key:
        raise ValueError("No OpenAI API key provided")
    
    # Import pipeline components
    from agent.code_generation_agent import ReachyCodeGenerationAgent
    from agent.code_evaluator import CodeEvaluator
    from agent.code_generation_pipeline import CodeGenerationPipeline
    
    # Create generator and evaluator with appropriate parameters
    generator_kwargs = {
        "api_key": api_key,
        "model": generator_model,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    generator = ReachyCodeGenerationAgent(**generator_kwargs)
    
    evaluator_kwargs = {
        "api_key": api_key,
        "model": evaluator_model,
        "temperature": max(0.1, temperature - 0.1)  # Lower temperature for evaluator
    }
    
    evaluator = CodeEvaluator(**evaluator_kwargs)
    
    # Create the pipeline
    pipeline = CodeGenerationPipeline(
        generator=generator,
        evaluator=evaluator,
        evaluation_threshold=evaluation_threshold,
        max_iterations=max_iterations
    )
    
    # Get the user request if not provided
    user_request = request
    if not user_request:
        print("\nPlease enter your code generation request:")
        user_request = input("> ")
    
    # Log or display info
    if not quiet:
        print(f"\nGenerating code for: {user_request}")
        print("This may take a minute...")
    
    start_time = time.time()
    
    # Generate code
    result = pipeline.generate_code(
        user_request=user_request,
        optimize=optimize
    )
    
    # Calculate duration if not provided
    if "duration" not in result:
        result["duration"] = time.time() - start_time
    
    # Get the final code
    original_code = result.get("generated_code", "")
    final_code = result.get("optimized_code") or original_code
    
    # Store final code in the result
    result["final_code"] = final_code
    
    # Display the results
    if not quiet:
        display_results(result, user_request)
    else:
        # In quiet mode, just print the final code
        print(final_code)
    
    # Execute the code if requested
    if execute and final_code:
        execution_result = execute_code(final_code)
        result["execution_result"] = execution_result
    elif execute:
        print("\nNo code was generated, cannot execute.")
        result["execution_result"] = {
            "success": False,
            "message": "No code was generated, cannot execute."
        }
    
    return result

def display_results(result: Dict[str, Any], user_request: str) -> None:
    """
    Display the results of the code generation pipeline.
    
    Args:
        result: The result of the code generation pipeline.
        user_request: The original user request.
    """
    final_code = result.get("final_code", "")
    
    print("\n" + "="*80)
    print(f"CODE GENERATION RESULTS")
    print("="*80)
    
    print(f"\nUser request: {user_request}")
    print(f"Final score: {result.get('final_score', 0):.1f}/100")
    print(f"Success: {'Yes' if result.get('success', False) else 'No'}")
    print(f"Time taken: {result.get('duration', 0):.2f} seconds")
    
    if 'iterations' in result:
        print(f"Optimization iterations: {result['iterations']}")
    
    # Show final code
    print("\nFINAL CODE:")
    print("-"*80)
    print(final_code)
    print("-"*80)
    
    # Show evaluation information
    evaluation = result.get("evaluation_result", {})
    if evaluation:
        if evaluation.get("errors"):
            print("\nERRORS:")
            for error in evaluation["errors"]:
                print(f"  - {error}")
        
        if evaluation.get("warnings"):
            print("\nWARNINGS:")
            for warning in evaluation["warnings"]:
                print(f"  - {warning}")
        
        if evaluation.get("suggestions"):
            print("\nSUGGESTIONS:")
            for suggestion in evaluation["suggestions"]:
                print(f"  - {suggestion}")

def execute_code(code: str) -> Dict[str, Any]:
    """
    Execute the generated code.
    
    Args:
        code: The code to execute.
        
    Returns:
        Dict[str, Any]: The execution result.
    """
    try:
        # First try to import reachy_sdk to check if robot support is available
        reachy_sdk_spec = importlib.util.find_spec("reachy_sdk")
        
        if reachy_sdk_spec is None:
            print("\nCannot execute: reachy_sdk module not installed.")
            print("Please install the Reachy SDK to enable execution.")
            return {
                "success": False,
                "message": "reachy_sdk module not installed",
                "output": "",
                "stderr": ""
            }
        
        print("\nExecuting code on Reachy robot...")
        
        # Create a temporary script file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(code)
        
        try:
            # Execute the code
            process = subprocess.Popen(
                ['python', temp_file_path], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=30)  # 30 second timeout
            
            # Print execution results
            if stdout:
                print("\nExecution output:")
                print(stdout)
            
            if stderr:
                print("\nExecution errors:")
                print(stderr)
                
            if process.returncode == 0:
                print("\nCode executed successfully on Reachy robot.")
                return {
                    "success": True,
                    "message": "Code executed successfully",
                    "output": stdout,
                    "stderr": stderr,
                    "return_code": process.returncode
                }
            else:
                print(f"\nExecution failed with exit code {process.returncode}.")
                return {
                    "success": False,
                    "message": f"Execution failed with exit code {process.returncode}",
                    "output": stdout,
                    "stderr": stderr,
                    "return_code": process.returncode
                }
                
        except subprocess.TimeoutExpired:
            process.kill()
            print("\nExecution timed out after 30 seconds. The process was terminated.")
            return {
                "success": False,
                "message": "Execution timed out after 30 seconds",
                "output": "",
                "stderr": "Timeout error"
            }
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    except Exception as e:
        print(f"\nError during execution: {e}")
        print("Please check your Reachy robot connection and try again.")
        return {
            "success": False,
            "message": f"Error during execution: {str(e)}",
            "output": "",
            "stderr": traceback.format_exc()
        }

# Simple entry point for direct execution
if __name__ == "__main__":
    import argparse
    import sys
    import os
    
    # Add parent directory to sys.path so we can import agent modules
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    parser = argparse.ArgumentParser(description="Reachy 2 Code Generation App")
    parser.add_argument("--ui", action="store_true", help="Launch with Gradio UI")
    parser.add_argument("--request", type=str, help="Natural language request for code generation")
    
    args = parser.parse_args()
    
    if args.ui:
        launch_ui()
    elif args.request:
        result = run_code_generation(request=args.request)
        print(f"Score: {result.get('final_score', 0)}")
    else:
        print("Please specify --ui to launch the UI or --request to generate code.") 