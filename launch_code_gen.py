#!/usr/bin/env python
"""
Simplified launcher for the Reachy 2 Code Generation Pipeline.

This script provides a direct command-line interface for generating, evaluating, and optimizing
Python code for the Reachy 2 robot, using the streamlined generator-evaluator-optimizer workflow.
"""

import os
import sys
import argparse
import logging
import time
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("launch_code_gen")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import OPENAI_API_KEY, MODEL

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Reachy 2 Code Generation")
    parser.add_argument("--request", type=str, help="Natural language request for code generation")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    
    # Generation parameters
    gen_group = parser.add_argument_group("Generation Parameters")
    gen_group.add_argument("--generator-model", type=str, default=MODEL, help=f"Model for code generation (default: {MODEL})")
    gen_group.add_argument("--evaluator-model", type=str, default="gpt-4o-mini", help="Model for code evaluation (default: gpt-4o-mini)")
    gen_group.add_argument("--temperature", type=float, default=0.2, help="Temperature for generation (default: 0.2)")
    gen_group.add_argument("--max-tokens", type=int, default=4000, help="Max tokens for generation (default: 4000)")
    
    # Pipeline configuration
    pipeline_group = parser.add_argument_group("Pipeline Configuration")
    pipeline_group.add_argument("--no-optimize", action="store_true", help="Disable code optimization")
    pipeline_group.add_argument("--max-iterations", type=int, default=3, help="Maximum optimization iterations (default: 3)")
    pipeline_group.add_argument("--evaluation-threshold", type=float, default=75.0, help="Evaluation threshold (default: 75.0)")
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--execute", action="store_true", help="Execute the generated code on the connected Reachy robot")
    output_group.add_argument("--quiet", action="store_true", help="Minimize output")
    
    # UI mode (for backward compatibility)
    parser.add_argument("--ui", action="store_true", help="Launch with Gradio UI (for backward compatibility)")
    parser.add_argument("--port", type=int, default=7860, help="Port for Gradio UI (if --ui is used)")
    parser.add_argument("--share", action="store_true", help="Create public link for Gradio UI (if --ui is used)")
    
    # Debug options
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    return parser.parse_args()

def main():
    """Main function to launch the code generation pipeline."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
    
    # Get the API key
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY") or OPENAI_API_KEY
    
    if not api_key:
        logger.error("No OpenAI API key provided. Please set the OPENAI_API_KEY environment variable or use --api-key.")
        sys.exit(1)
    
    # Log configuration
    logger.info(f"Launching Reachy 2 Code Generation")
    logger.info(f"Generator model: {args.generator_model}")
    logger.info(f"Evaluator model: {args.evaluator_model}")
    logger.info(f"Temperature: {args.temperature}")
    logger.info(f"Optimization: {'Disabled' if args.no_optimize else 'Enabled'}")
    logger.info(f"Max iterations: {args.max_iterations}")
    logger.info(f"Evaluation threshold: {args.evaluation_threshold}")
    
    # UI Mode - Launch the Gradio interface for backward compatibility
    if args.ui:
        try:
            from agent.code_generation_interface import CodeGenerationInterface
            
            # Create the interface
            interface = CodeGenerationInterface(
                api_key=api_key,
                model=args.generator_model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                max_iterations=args.max_iterations,
                evaluation_threshold=args.evaluation_threshold
            )
            
            # Launch the interface
            logger.info(f"Launching Gradio interface on port {args.port} with share={args.share}")
            interface.launch_interface(share=args.share, port=args.port)
            return
        except Exception as e:
            logger.error(f"Error launching UI: {e}")
            logger.error(traceback.format_exc())
            logger.error("Falling back to command line mode")
    
    # CLI Mode - Direct pipeline execution
    # Import pipeline components
    from agent.code_generation_agent import ReachyCodeGenerationAgent
    from agent.code_evaluator import CodeEvaluator
    from agent.code_generation_pipeline import CodeGenerationPipeline
    
    # Create generator and evaluator
    generator = ReachyCodeGenerationAgent(
        api_key=api_key,
        model=args.generator_model,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    
    evaluator = CodeEvaluator(
        api_key=api_key,
        model=args.evaluator_model,
        temperature=max(0.1, args.temperature - 0.1)  # Lower temperature for evaluator
    )
    
    # Create the pipeline
    pipeline = CodeGenerationPipeline(
        generator=generator,
        evaluator=evaluator,
        evaluation_threshold=args.evaluation_threshold,
        max_iterations=args.max_iterations
    )
    
    # Get the user request
    user_request = args.request
    if not user_request:
        print("\nPlease enter your code generation request:")
        user_request = input("> ")
    
    # Run the pipeline
    if not args.quiet:
        print(f"\nGenerating code for: {user_request}")
        print("This may take a minute...")
    
    start_time = time.time()
    
    # Generate code
    result = pipeline.generate_code(
        user_request=user_request,
        optimize=not args.no_optimize
    )
    
    # Calculate duration if not provided
    if "duration" not in result:
        result["duration"] = time.time() - start_time
    
    # Get the final code
    original_code = result.get("generated_code", "")
    final_code = result.get("optimized_code") or original_code
    
    # Display the results
    if not args.quiet:
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
    else:
        # In quiet mode, just print the final code
        print(final_code)
    
    # Execute the code if requested
    if args.execute and final_code:
        try:
            # First try to import reachy_sdk to check if robot support is available
            import importlib
            reachy_sdk_spec = importlib.util.find_spec("reachy_sdk")
            
            if reachy_sdk_spec is None:
                print("\nCannot execute: reachy_sdk module not installed.")
                print("Please install the Reachy SDK to enable execution.")
            else:
                print("\nExecuting code on Reachy robot...")
                
                # Create a temporary script file
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp_file:
                    temp_file_path = temp_file.name
                    temp_file.write(final_code)
                
                try:
                    # Execute the code
                    import subprocess
                    process = subprocess.Popen(['python', temp_file_path], 
                                              stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE,
                                              text=True)
                    
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
                    else:
                        print(f"\nExecution failed with exit code {process.returncode}.")
                        
                except subprocess.TimeoutExpired:
                    process.kill()
                    print("\nExecution timed out after 30 seconds. The process was terminated.")
                finally:
                    # Clean up the temporary file
                    os.unlink(temp_file_path)
        except Exception as e:
            print(f"\nError during execution: {e}")
            print("Please check your Reachy robot connection and try again.")
    elif args.execute:
        print("\nNo code was generated, cannot execute.")

if __name__ == "__main__":
    main() 