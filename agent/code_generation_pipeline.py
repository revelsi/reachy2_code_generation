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
from config import MODEL

# Type alias for the pipeline result
PipelineResult = Dict[str, Any]

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Forward references for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent.code_generation_agent import ReachyCodeGenerationAgent
    from agent.code_evaluator import CodeEvaluator
    from websocket_server import WebsocketServer

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import components
from agent.code_generation_agent import ReachyCodeGenerationAgent
from agent.code_evaluator import CodeEvaluator

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

class CodeGenerationPipeline:
    """
    Pipeline for generating, evaluating, and improving code for the Reachy 2 robot.
    
    This pipeline:
    1. Generates initial code based on user requests using the LLM (using MODEL from config)
    2. Evaluates the generated code using the code evaluator (using GPT-4o-mini)
    3. Optimizing the code based on evaluation feedback using the integrated approach (using MODEL from config)
    
    The pipeline tracks the entire process and provides detailed reporting.
    """
    
    def __init__(
        self, 
        generator: 'ReachyCodeGenerationAgent',
        evaluator: Optional['CodeEvaluator'] = None,
        evaluation_threshold: float = 75.0,
        max_iterations: int = 3,
        generator_temperature: float = 0.2,
        callback_function: Optional[Callable] = None,
        websocket_server: Optional['WebsocketServer'] = None
    ):
        """
        Initialize the code generation pipeline.
        
        Args:
            generator: The code generator agent.
            evaluator: The code evaluator.
            evaluation_threshold: The threshold for considering code good enough (0-100).
            max_iterations: Maximum number of optimization iterations.
            generator_temperature: Temperature for the generator.
            callback_function: Function to call with status updates.
            websocket_server: Optional WebSocket server for status updates.
        """
        self.generator = generator
        self.evaluator = evaluator or CodeEvaluator()
        self.evaluation_threshold = evaluation_threshold
        self.max_iterations = max_iterations
        self.callback_function = callback_function
        self.websocket_server = websocket_server
        
        # Configure logging
        self.logger = logging.getLogger("pipeline")
        
        # Log configuration
        self.logger.info("Initializing Code Generation Pipeline with:")
        self.logger.info(f"  - Evaluation threshold: {evaluation_threshold}")
        self.logger.info(f"  - Max iterations: {max_iterations}")
        self.logger.info(f"  - Generator model: {MODEL}")
        
    def summarize_result(self, result: PipelineResult) -> str:
        """Summarize the pipeline result in a human-readable format."""
        if not result:
            return "No result available."
        
        summary = []
        summary.append(f"Code Generation Pipeline Summary for: {result['original_request']}")
        summary.append(f"Timestamp: {result['timestamp']}")
        summary.append(f"Duration: {result['duration']:.2f} seconds\n")
        
        summary.append(f"Final Score: {result['final_score']:.1f}/100")
        summary.append(f"Success: {'Yes' if result['success'] else 'No'}\n")
        
        # Add evaluation summary
        eval_result = result.get("evaluation_result", {})
        summary.append("Evaluation Results:")
        summary.append(f"- Score: {eval_result.get('score', 0.0):.1f}/100")
        summary.append(f"- Valid: {'Yes' if eval_result.get('valid', False) else 'No'}")
        
        if eval_result.get("errors", []):
            summary.append(f"- Errors: {len(eval_result.get('errors', []))}")
        if eval_result.get("warnings", []):
            summary.append(f"- Warnings: {len(eval_result.get('warnings', []))}")
            
        # Add optimization summary if available
        if result.get("optimization_result"):
            summary.append("\nOptimization Results:")
            summary.append(f"- Iterations: {result['iterations']}")
            
            changes = result["optimization_result"].get("changes_made", [])
            if changes:
                summary.append(f"- Changes Made: {len(changes)}")
                for change in changes[:3]:  # Show first 3 changes
                    summary.append(f"  * {change}")
                if len(changes) > 3:
                    summary.append(f"  * ... and {len(changes) - 3} more changes")
            else:
                summary.append("- No changes were made during optimization")
                
            if result["optimization_result"].get("explanation"):
                summary.append(f"- {result['optimization_result']['explanation']}")
        
        # Final code section
        final_code = result.get("optimized_code") or result.get("generated_code", "")
        if final_code:
            summary.append("\nFinal Code:")
            summary.append("```python")
            summary.append(final_code)
            summary.append("```")
        
        return "\n".join(summary)

    def _send_status_update(self, status: str) -> None:
        """
        Send a status update via WebSocket if available.
        
        Args:
            status: The status message to send.
        """
        if self.websocket_server:
            try:
                import json
                message = {
                    "type": "status_update",
                    "data": {
                        "status": status,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                
                # Check if broadcast method exists
                if hasattr(self.websocket_server, 'broadcast'):
                    self.websocket_server.broadcast(json.dumps(message))
                    self.logger.debug(f"Sent status update: {status}")
            except Exception as e:
                self.logger.error(f"Error sending status update: {e}")
                self.logger.error(traceback.format_exc())
                
        # Also call the callback function if provided
        if self.callback_function:
            try:
                self.callback_function(status)
            except Exception as e:
                self.logger.error(f"Error calling status callback: {e}")
                self.logger.error(traceback.format_exc())

    def generate_code(self, user_request: str, optimize: bool = True) -> PipelineResult:
        """
        Generate code from a natural language request, evaluate it, and optimize it using
        an integrated approach where the same generator is used for both initial generation
        and optimization with evaluation feedback.
        
        Args:
            user_request: The user's natural language request.
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
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # 1. Generate initial code
            self.logger.info("Generating initial code...")
            self._send_status_update("Generating initial code...")
            
            generation_response = self.generator.process_message(user_request)
            
            generated_code = generation_response.get("code", "")
            result["generated_code"] = generated_code
            
            if not generated_code:
                self.logger.warning("No code was generated")
                result["success"] = False
                return result
            
            # 2. Evaluate the generated code
            self.logger.info("Evaluating generated code...")
            self._send_status_update("Evaluating generated code...")
            
            evaluation_result = self.evaluator.evaluate_code(
                code=generated_code,
                user_request=user_request,
                evaluation_mode="standard"
            )
            
            result["evaluation_result"] = evaluation_result
            result["final_score"] = evaluation_result.get("score", 0.0)
            
            # Log evaluation results
            self.logger.info(f"Initial evaluation score: {evaluation_result.get('score', 0.0)}/100")
            self.logger.info(f"Valid: {evaluation_result.get('valid', False)}")
            if evaluation_result.get("errors", []):
                self.logger.info(f"Errors: {len(evaluation_result.get('errors', []))}")
            if evaluation_result.get("warnings", []):
                self.logger.info(f"Warnings: {len(evaluation_result.get('warnings', []))}")
            
            # Check if code is already good enough
            if evaluation_result.get("score", 0.0) >= self.evaluation_threshold:
                self.logger.info("Code already meets quality threshold, skipping optimization")
                result["success"] = True
                result["optimized_code"] = generated_code  # No optimization needed
                
                # Set duration and return result
                result["duration"] = time.time() - start_time
                return result
            
            # 3. Optimize the code if requested - Using integrated approach
            if optimize:
                self.logger.info("Using integrated optimization approach...")
                self._send_status_update("Optimizing code with integrated approach...")
                
                # Track optimization iterations
                current_code = generated_code
                current_score = evaluation_result.get("score", 0.0)
                changes = []
                iterations_count = 0
                
                # Perform optimization iterations
                for iteration in range(self.max_iterations):
                    iterations_count += 1
                    self.logger.info(f"Starting integrated optimization iteration {iteration + 1}/{self.max_iterations}")
                    
                    # Create optimization prompt with evaluation feedback
                    formatted_errors = "\n".join([f"- {error}" for error in evaluation_result.get("errors", [])])
                    formatted_warnings = "\n".join([f"- {warning}" for warning in evaluation_result.get("warnings", [])])
                    formatted_suggestions = "\n".join([f"- {suggestion}" for suggestion in evaluation_result.get("suggestions", [])])
                    
                    optimization_prompt = f"""
I need to improve the code I previously generated for the request: "{user_request}"

The initial code was:
```python
{current_code}
```

Evaluation feedback (score: {current_score}/100):

CRITICAL ERRORS TO FIX:
{formatted_errors if formatted_errors else "None"}

WARNINGS TO ADDRESS:
{formatted_warnings if formatted_warnings else "None"}

SUGGESTIONS FOR IMPROVEMENT:
{formatted_suggestions if formatted_suggestions else "None"}

ADDITIONAL EXPLANATION:
{evaluation_result.get("explanation", "No additional explanation provided.")}

Please improve this code while following ALL the original guidelines for the Reachy 2 robot API. 
Fix the errors and warnings, and implement the suggestions where appropriate.
Ensure the code follows best practices for safety, has proper error handling, and correctly uses the Reachy 2 SDK.
Return only the improved code without explanation.
"""
                    
                    # Use the same generator with the optimization prompt
                    self.logger.info(f"Generating improved code in iteration {iteration + 1}...")
                    optimization_response = self.generator.process_message(optimization_prompt)
                    
                    # Extract the optimized code
                    optimized_code = optimization_response.get("code", current_code)
                    
                    # Check if the code actually changed
                    if optimized_code == current_code:
                        self.logger.info(f"No changes made in iteration {iteration + 1}, stopping optimization")
                        break
                    
                    # Record that we made changes in this iteration
                    changes.append(f"Iteration {iteration + 1}: Code improved based on evaluation feedback")
                    
                    # Update the current code
                    current_code = optimized_code
                    
                    # Re-evaluate the optimized code
                    self.logger.info(f"Re-evaluating improved code from iteration {iteration + 1}...")
                    new_evaluation_result = self.evaluator.evaluate_code(
                        code=optimized_code,
                        user_request=user_request,
                        evaluation_mode="standard"
                    )
                    
                    # Update evaluation result and score
                    evaluation_result = new_evaluation_result
                    new_score = evaluation_result.get("score", 0.0)
                    
                    # Log the new score
                    self.logger.info(f"Iteration {iteration + 1} score: {new_score}/100")
                    
                    # Check if we've improved the score
                    if new_score > current_score:
                        self.logger.info(f"Score improved from {current_score} to {new_score}")
                        current_score = new_score
                        
                        # Check if we've reached the threshold
                        if current_score >= self.evaluation_threshold:
                            self.logger.info(f"Score {current_score} meets threshold {self.evaluation_threshold}, stopping optimization")
                            break
                    else:
                        self.logger.info(f"Score did not improve (was {current_score}, now {new_score})")
                        # If score didn't improve, we might still continue if there are more iterations left
                
                # Update result with optimization data
                result["optimized_code"] = current_code
                result["final_score"] = current_score
                result["iterations"] = iterations_count
                
                # Create a simplified optimization result structure for compatibility
                result["optimization_result"] = {
                    "original_code": generated_code,
                    "optimized_code": current_code,
                    "changes_made": changes,
                    "evaluation_score": current_score,
                    "success": len(changes) > 0,
                    "explanation": f"Integrated optimization completed with {len(changes)} iterations."
                }
                
                # Log optimization results
                if len(changes) > 0:
                    self.logger.info(f"Integrated optimization successful with {len(changes)} iterations")
                    self.logger.info(f"Final score: {current_score}/100")
                    result["success"] = True
                else:
                    self.logger.warning("Integrated optimization did not make any changes")
                    result["optimized_code"] = generated_code  # Use original code if optimization failed
            
            # Set success flag based on final score
            result["success"] = result["final_score"] >= self.evaluation_threshold
            
            # Set duration and return result
            result["duration"] = time.time() - start_time
            return result
            
        except Exception as e:
            self.logger.error(f"Error in code generation pipeline: {e}")
            self.logger.error(traceback.format_exc())
            
            # Return partial result on error
            result["success"] = False
            result["duration"] = time.time() - start_time
            return result


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
    parser.add_argument("--output", type=str, help="Output file for the generated code")
    
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
        model="gpt-4o-mini",  # Always use GPT-4o-mini for evaluation
        temperature=max(0.1, args.temperature - 0.1)  # Lower temperature for evaluation
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
    print(f"Using model for evaluation: gpt-4o-mini")
    print(f"Max iterations: {args.max_iterations}")
    print(f"Evaluation threshold: {args.evaluation_threshold}")
    print("Please wait, this may take a minute...")
    
    result = pipeline.generate_code(
        user_request=request,
        optimize=not args.no_optimize
    )
    
    # Print the summary
    print("\n" + "="*80)
    print(pipeline.summarize_result(result))
    print("="*80 + "\n")
    
    # Output the code
    code_to_output = result.get("optimized_code") or result.get("generated_code", "")
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(code_to_output)
        print(f"Generated code written to {args.output}")
    else:
        print("Generated Code:")
        print("="*80)
        print(code_to_output)
        print("="*80)


if __name__ == "__main__":
    main() 