#!/usr/bin/env python
"""
Simplified launcher for the Reachy 2 Code Generation Pipeline.

This script provides a simple command-line interface for launching
the code generation application for the Reachy 2 robot.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

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
from config import OPENAI_API_KEY, MODEL, EVALUATOR_MODEL

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Reachy 2 Code Generation")
    parser.add_argument("--request", type=str, help="Natural language request for code generation")
    parser.add_argument("--api-key", help="OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)")
    
    # Generation parameters
    gen_group = parser.add_argument_group("Generation Parameters")
    gen_group.add_argument("--generator-model", type=str, default=MODEL, help=f"Model for code generation (default: {MODEL})")
    gen_group.add_argument("--evaluator-model", type=str, default=EVALUATOR_MODEL, help=f"Model for code evaluation (default: {EVALUATOR_MODEL})")
    gen_group.add_argument("--temperature", type=float, default=0.2, help="Temperature for generation (default: 0.2)")
    gen_group.add_argument("--max-tokens", type=int, default=4000, help="Max tokens for generation (default: 4000)")
    
    # Pipeline configuration
    pipeline_group = parser.add_argument_group("Pipeline Configuration")
    pipeline_group.add_argument("--no-optimize", action="store_true", help="Disable code optimization")
    pipeline_group.add_argument("--max-iterations", type=int, default=1, help="Maximum optimization iterations (default: 1)")
    pipeline_group.add_argument("--evaluation-threshold", type=float, default=75.0, help="Evaluation threshold (default: 75.0)")
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--execute", action="store_true", help="Execute the generated code on the connected Reachy robot")
    output_group.add_argument("--quiet", action="store_true", help="Minimize output")
    
    # UI mode
    parser.add_argument("--ui", action="store_true", help="Launch with Gradio UI")
    parser.add_argument("--port", type=int, default=7860, help="Port for Gradio UI (if --ui is used)")
    parser.add_argument("--share", action="store_true", help="Create public link for Gradio UI (if --ui is used)")
    
    # Debug options
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    return parser.parse_args()

def main():
    """Main function to launch the code generation application."""
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
    
    # Import the app module
    from agent.app import launch_ui, run_code_generation
    
    try:
        # UI Mode - Launch the Gradio interface
        if args.ui:
            launch_ui(
                api_key=api_key,
                generator_model=args.generator_model,
                evaluator_model=args.evaluator_model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                max_iterations=args.max_iterations,
                evaluation_threshold=args.evaluation_threshold,
                port=args.port,
                share=args.share
            )
        # CLI Mode - Run the code generation pipeline
        else:
            run_code_generation(
                request=args.request,
                api_key=api_key,
                generator_model=args.generator_model,
                evaluator_model=args.evaluator_model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                optimize=not args.no_optimize,
                max_iterations=args.max_iterations,
                evaluation_threshold=args.evaluation_threshold,
                execute=args.execute,
                quiet=args.quiet
            )
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 