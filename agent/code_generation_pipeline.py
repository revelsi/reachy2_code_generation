#!/usr/bin/env python
"""
Code Generation Pipeline for the Reachy 2 robot.

This module provides a pipeline for generating, evaluating, and optimizing Python code
using the integrated generator-optimizer approach.
It implements the evaluator-feedback workflow for better code quality.
"""

import os
import sys
import json
import time
import logging
import traceback
from typing import Dict, List, Any, Optional, TypedDict, Tuple, Union, Callable

# Import configuration
from config import MODEL, EVALUATOR_MODEL

# Type alias for the pipeline result
PipelineResult = Dict[str, Any]

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pipeline")

# Forward references for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent.code_generation_agent import ReachyCodeGenerationAgent
    from agent.code_evaluator import CodeEvaluator

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Type definitions for pipeline results
class EvaluationResult(TypedDict, total=False):
    """Result of code evaluation."""
    score: float
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    explanation: str

class OptimizationResult(TypedDict, total=False):
    """Result of code optimization."""
    original_code: str
    optimized_code: str
    changes_made: List[str]
    evaluation_score: float
    success: bool
    explanation: str

class PipelineResult(TypedDict):
    """Result of code generation pipeline."""
    original_request: str
    generated_code: str
    optimized_code: str
    evaluation_result: EvaluationResult
    optimization_result: Optional[OptimizationResult]
    final_score: float
    success: bool
    iterations: int
    duration: float
    timestamp: str
    raw_response: str

class CodeGenerationPipeline:
    """
    Simplified pipeline for generating, evaluating, and improving code for the Reachy 2 robot.
    
    This pipeline:
    1. Generates initial code based on user requests
    2. Evaluates the generated code using the code evaluator
    3. Optimizes the code based on evaluation feedback
    4. Repeats the evaluate-optimize cycle until quality threshold is met or max iterations reached
    """
    
    def __init__(
        self, 
        generator: 'ReachyCodeGenerationAgent',
        evaluator: 'CodeEvaluator',
        evaluation_threshold: float = 75.0,
        max_iterations: int = 2,
        callback_function: Optional[Callable] = None
    ):
        """
        Initialize the code generation pipeline.
        
        Args:
            generator: The code generator agent.
            evaluator: The code evaluator.
            evaluation_threshold: The threshold for considering code good enough (0-100).
            max_iterations: Maximum number of optimization iterations.
            callback_function: Function to call with status updates.
        """
        self.generator = generator
        self.evaluator = evaluator
        self.evaluation_threshold = evaluation_threshold
        self.max_iterations = max_iterations
        self.callback_function = callback_function
        
        # Configure logging
        self.logger = logging.getLogger("pipeline")
        
        # Log configuration
        self.logger.info("Initializing Code Generation Pipeline with:")
        self.logger.info(f"  - Evaluation threshold: {evaluation_threshold}")
        self.logger.info(f"  - Max iterations: {max_iterations}")
        
    def generate_code(self, user_request: str, history: Optional[Union[List[Dict[str, str]], List[List[str]]]] = None, optimize: bool = True) -> PipelineResult:
        """
        Generate code from a natural language request, evaluate it, and optimize it.
        
        Args:
            user_request: The user's natural language request.
            history: Optional chat history, either as List[Dict] or List[List]. 
            optimize: Whether to optimize the generated code.
            
        Returns:
            PipelineResult: The result of the pipeline, including all stages.
        """
        start_time = time.time()
        
        # Initialize result data
        result = {
            "original_request": user_request,
            "generated_code": "",
            "optimized_code": "",
            "evaluation_result": {},
            "optimization_result": None,
            "final_score": 0.0,
            "success": False,
            "iterations": 0,
            "duration": 0.0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "raw_response": ""
        }
        
        try:
            # 1. Generate initial code using the generator agent
            self.logger.info("Generating initial code...")
            self._notify("Generating initial code...")
            
            try:
                # Pass history to the generator for context
                response = self.generator.generate_code(user_request=user_request, history=history)
                generated_code = response.get("code", "")
                raw_response = response.get("raw_response", "")
                result["raw_response"] = raw_response
                
                if not generated_code:
                    self.logger.warning("No code was generated")
                    result["success"] = False
                    return result
                    
                result["generated_code"] = generated_code
                
            except Exception as gen_error:
                self.logger.error(f"Error generating code: {gen_error}")
                self.logger.error(traceback.format_exc())
                return result
                
            # 2. Evaluate the generated code
            self.logger.info("Evaluating generated code...")
            self._notify("Evaluating generated code...")
            
            try:
                evaluation_result = self.evaluator.evaluate_code(
                    code=generated_code,
                    user_request=user_request
                )
                
                result["evaluation_result"] = evaluation_result
                result["final_score"] = evaluation_result.get("score", 0.0)
                
                self._log_evaluation_result(evaluation_result)
                
            except Exception as eval_error:
                self.logger.error(f"Error evaluating code: {eval_error}")
                self.logger.error(traceback.format_exc())
                return result
                
            # Check if code is already good enough
            if evaluation_result.get("score", 0.0) >= self.evaluation_threshold:
                self.logger.info("Code already meets quality threshold, skipping optimization")
                result["success"] = True
                result["optimized_code"] = generated_code
                result["duration"] = time.time() - start_time
                return result
                
            # 3. Optimize the code if requested
            if optimize:
                self.logger.info("Starting code optimization...")
                self._notify("Optimizing code...")
                
                current_code = generated_code
                current_score = evaluation_result.get("score", 0.0)
                current_evaluation = evaluation_result
                iterations_count = 0
                changes = []
                
                # Perform optimization iterations
                for iteration in range(self.max_iterations):
                    iterations_count += 1
                    self.logger.info(f"Starting optimization iteration {iteration + 1}/{self.max_iterations}")
                    
                    # Create detailed feedback for optimization
                    optimization_feedback = self._format_evaluation_feedback(current_evaluation)
                    
                    # Generate optimized code
                    try:
                        optimized_code = self._optimize_code(
                            code=current_code,
                            user_request=user_request,
                            feedback=optimization_feedback
                        )
                        
                        # Skip if no changes were made
                        if optimized_code == current_code:
                            self.logger.info(f"No changes made in iteration {iteration + 1}")
                            break
                            
                        # Update current code
                        current_code = optimized_code
                        changes.append(f"Iteration {iteration + 1}: Code improved based on feedback")
                        
                    except Exception as opt_error:
                        self.logger.error(f"Error in optimization iteration {iteration + 1}: {opt_error}")
                        self.logger.error(traceback.format_exc())
                        break
                        
                    # Re-evaluate the optimized code
                    try:
                        new_evaluation = self.evaluator.evaluate_code(
                            code=current_code,
                            user_request=user_request
                        )
                        
                        new_score = new_evaluation.get("score", 0.0)
                        self.logger.info(f"Iteration {iteration + 1} score: {new_score}/100")
                        
                        # Update evaluation and score
                        current_evaluation = new_evaluation
                        
                        # Check if we've improved
                        if new_score > current_score:
                            self.logger.info(f"Score improved from {current_score} to {new_score}")
                            current_score = new_score
                            
                            # Check if we've reached the threshold
                            if current_score >= self.evaluation_threshold:
                                self.logger.info(f"Score {current_score} meets threshold, stopping")
                                break
                                
                        else:
                            self.logger.info(f"Score did not improve (was {current_score}, now {new_score})")
                            
                    except Exception as eval_error:
                        self.logger.error(f"Error evaluating optimized code: {eval_error}")
                        self.logger.error(traceback.format_exc())
                        break
                
                # Update result with optimization data
                result["optimized_code"] = current_code
                result["final_code"] = current_code
                result["final_score"] = current_score
                result["iterations"] = iterations_count
                result["evaluation_result"] = current_evaluation
                
                # Create optimization result summary
                result["optimization_result"] = {
                    "original_code": generated_code,
                    "optimized_code": current_code,
                    "changes_made": changes,
                    "evaluation_score": current_score,
                    "success": len(changes) > 0,
                    "explanation": f"Optimization completed with {len(changes)} iterations."
                }
                
                # Set success flag based on final score
                result["success"] = current_score >= self.evaluation_threshold
                
            # Set final duration
            result["duration"] = time.time() - start_time
            return result
            
        except Exception as e:
            self.logger.error(f"Error in code generation pipeline: {e}")
            self.logger.error(traceback.format_exc())
            
            # Return partial result
            result["success"] = False
            result["duration"] = time.time() - start_time
            return result
    
    def _notify(self, message: str) -> None:
        """Send a notification via the callback function if provided."""
        if self.callback_function:
            try:
                self.callback_function(message)
            except Exception as e:
                self.logger.error(f"Error in notification callback: {e}")
    
    def _log_evaluation_result(self, evaluation: Dict[str, Any]) -> None:
        """Log the evaluation result."""
        self.logger.info(f"Evaluation score: {evaluation.get('score', 0.0)}/100")
        self.logger.info(f"Valid: {evaluation.get('valid', False)}")
        
        if evaluation.get("errors", []):
            self.logger.info(f"Errors: {len(evaluation.get('errors', []))}")
            for error in evaluation.get("errors", [])[:3]:  # Log first 3 errors
                self.logger.info(f"  - {error}")
                
        if evaluation.get("warnings", []):
            self.logger.info(f"Warnings: {len(evaluation.get('warnings', []))}")
            for warning in evaluation.get("warnings", [])[:3]:  # Log first 3 warnings
                self.logger.info(f"  - {warning}")
    
    def _format_evaluation_feedback(self, evaluation: Dict[str, Any]) -> str:
        """Format evaluation feedback for the optimization step."""
        errors = "\n".join([f"- {error}" for error in evaluation.get("errors", [])])
        warnings = "\n".join([f"- {warning}" for warning in evaluation.get("warnings", [])])
        suggestions = "\n".join([f"- {suggestion}" for suggestion in evaluation.get("suggestions", [])])
        
        feedback = f"""
Evaluation feedback (score: {evaluation.get('score', 0.0)}/100):

CRITICAL ERRORS TO FIX:
{errors if errors else "None"}

WARNINGS TO ADDRESS:
{warnings if warnings else "None"}

SUGGESTIONS FOR IMPROVEMENT:
{suggestions if suggestions else "None"}

ADDITIONAL EXPLANATION:
{evaluation.get("explanation", "No additional explanation provided.")}
"""
        
        return feedback
    
    def _optimize_code(self, code: str, user_request: str, feedback: str) -> str:
        """Optimize code based on evaluation feedback."""
        # Build the optimization prompt
        optimization_prompt = f"""I need to improve code for the request: "{user_request}"

ORIGINAL CODE:
```python
{code}
```

EVALUATION FEEDBACK:
{feedback}

Please optimize this code following the optimization instructions in your system prompt.
Focus on fixing all errors first, then address warnings and implement suggested improvements.
Follow ALL best practices for the Reachy 2 robot SDK, especially regarding safety and error handling.
Return ONLY the improved Python code without explanation."""

        # Call the generator to optimize the code
        response = self.generator.generate_code(optimization_prompt)
        optimized_code = response.get("code", code)
        
        return optimized_code
        
    def summarize_result(self, result: Dict[str, Any]) -> str:
        """
        Create a minimal summary of the pipeline result for backward compatibility.
        
        Args:
            result: The pipeline result.
            
        Returns:
            str: A minimal summary.
        """
        # Extract key information
        score = result.get("final_score", 0)
        success = result.get("success", False)
        evaluation = result.get("evaluation_result", {})
        
        # Format the summary
        status = "✅ SUCCESS" if success else "⚠️ ISSUES DETECTED"
        summary = f"Code Generation: {status} (Score: {score:.1f}/100)"
        
        return summary


def main():
    """
    Main function for running the code generation pipeline as a standalone script.
    """
    import argparse
    from openai import OpenAI
    
    parser = argparse.ArgumentParser(description="Reachy 2 Code Generation Pipeline")
    parser.add_argument("--request", type=str, help="Natural language request for code generation")
    parser.add_argument("--api-key", type=str, help="OpenAI API key (if not set in environment)")
    parser.add_argument("--no-optimize", action="store_true", help="Skip the optimization step")
    parser.add_argument("--max-iterations", type=int, default=3, help="Maximum optimization iterations")
    parser.add_argument("--temperature", type=float, default=0.2, help="Temperature for generation")
    parser.add_argument("--evaluation-threshold", type=float, default=75.0, help="Score threshold for considering code good enough")
    parser.add_argument("--execute", action="store_true", help="Execute the generated code on the connected Reachy robot")
    
    args = parser.parse_args()
    
    # Get the API key from environment or argument
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("ERROR: No OpenAI API key provided. Please set the OPENAI_API_KEY environment variable or use --api-key.")
        sys.exit(1)
    
    # Get the request
    request = args.request
    if not request:
        print("Please enter your code generation request:")
        request = input("> ")
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create generator and evaluator
    from agent.code_generation_agent import ReachyCodeGenerationAgent
    from agent.code_evaluator import CodeEvaluator
    
    generator = ReachyCodeGenerationAgent(
        api_key=api_key,
        model=MODEL,
        temperature=args.temperature
    )
    
    evaluator = CodeEvaluator(
        api_key=api_key,
        model=EVALUATOR_MODEL,  # Use the centralized evaluator model constant
        temperature=0.1  # Lower temperature for evaluation
    )
    
    # Create the pipeline
    pipeline = CodeGenerationPipeline(
        generator=generator,
        evaluator=evaluator,
        max_iterations=args.max_iterations,
        evaluation_threshold=args.evaluation_threshold
    )
    
    # Generate code
    print(f"Generating code for: {request}")
    print(f"Using model for generation: {MODEL}")
    print(f"Using model for evaluation: {EVALUATOR_MODEL}")
    print(f"Max iterations: {args.max_iterations}")
    print(f"Evaluation threshold: {args.evaluation_threshold}")
    print("Please wait, this may take a minute...")
    
    result = pipeline.generate_code(
        user_request=request,
        optimize=not args.no_optimize
    )
    
    # Display evaluation results
    evaluation = result.get("evaluation_result", {})
    success = result.get("success", False)
    score = result.get("final_score", 0)
    
    print("\n" + "="*80)
    print(f"CODE GENERATION {'SUCCESSFUL' if success else 'COMPLETED WITH ISSUES'}")
    print(f"Score: {score:.1f}/100")
    
    if evaluation.get("errors"):
        print("\nErrors:")
        for error in evaluation.get("errors", []):
            print(f"  - {error}")
    
    if evaluation.get("warnings"):
        print("\nWarnings:")
        for warning in evaluation.get("warnings", []):
            print(f"  - {warning}")
    
    print("="*80 + "\n")
    
    # Get the final code
    final_code = result.get("optimized_code") or result.get("generated_code", "")
    
    # Display the code
    print("Generated Code:")
    print("="*80)
    print(final_code)
    print("="*80)
    
    # Execute the code if requested and the robot is connected
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