#!/usr/bin/env python
"""
Code Evaluator for the Reachy 2 robot code generation system.

This module provides a code evaluator that analyzes and provides feedback
on generated Python code for the Reachy 2 robot.
"""

import os
import sys
import json
import logging
import traceback
from typing import Dict, List, Any, Optional, TypedDict, Tuple, Union
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code_evaluator")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import OPENAI_API_KEY, MODEL

class EvaluationResult(TypedDict):
    """Result of code evaluation."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    score: float
    explanation: str

class CodeEvaluator:
    """
    A code evaluator that analyzes Python code for the Reachy 2 robot.
    
    This evaluator uses the OpenAI API to analyze Python code for potential issues
    and provides detailed feedback on code quality, correctness, and safety.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,  # Lower temperature for more consistent evaluation
        max_tokens: int = 2048,
    ):
        """Initialize the code evaluator.

        Args:
            api_key: The OpenAI API key.
            model: The OpenAI model to use.
            temperature: The temperature for the model (0.0 to 1.0).
            max_tokens: The maximum number of tokens to generate.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize logger
        self.logger = logging.getLogger("code_evaluator")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Load evaluation criteria
        self.evaluation_criteria = self._load_evaluation_criteria()
        
        self.logger.debug(f"Initialized code evaluator with model: {model}")
    
    def _load_evaluation_criteria(self) -> Dict[str, Any]:
        """
        Load the evaluation criteria.
        
        Returns:
            Dict[str, Any]: The evaluation criteria.
        """
        # This could be loaded from a file in the future
        return {
            "syntax": {
                "weight": 10,
                "description": "Check for syntax errors and code structure issues."
            },
            "api_usage": {
                "weight": 30,
                "description": "Verify correct usage of the Reachy 2 SDK API."
            },
            "safety": {
                "weight": 35,
                "description": "Analyze code for potential safety issues with robot operation."
            },
            "error_handling": {
                "weight": 15,
                "description": "Check for proper error handling and recovery mechanisms."
            },
            "code_quality": {
                "weight": 10,
                "description": "Assess overall code quality, readability, and maintainability."
            }
        }
    
    def evaluate_code(
        self, 
        code: str, 
        user_request: str,
        evaluation_mode: str = "standard"
    ) -> EvaluationResult:
        """
        Evaluate the generated code for correctness, safety, and quality.
        
        Args:
            code: The code to evaluate.
            user_request: The original user request for context.
            evaluation_mode: The evaluation mode (standard, detailed, or safety-focus).
            
        Returns:
            EvaluationResult: The evaluation result.
        """
        if not code:
            return {
                "valid": False,
                "errors": ["No code provided for evaluation"],
                "warnings": [],
                "suggestions": [],
                "score": 0.0,
                "explanation": "No code was provided for evaluation."
            }
        
        # Build the system prompt for code evaluation
        system_prompt = self._build_evaluation_prompt(evaluation_mode)
        
        # Build the user prompt with the code and request
        user_prompt = f"""
ORIGINAL USER REQUEST:
{user_request}

GENERATED CODE TO EVALUATE:
```python
{code}
```

Please evaluate this code based on the criteria specified. 
Provide a clear analysis, listing any errors, warnings, and suggestions.
"""
        
        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}  # Request JSON format
            )
            
            # Extract the evaluation from the response
            evaluation_text = response.choices[0].message.content
            
            try:
                # Parse the JSON response
                evaluation = json.loads(evaluation_text)
                
                # Extract the relevant fields with defaults if missing
                valid = evaluation.get("valid", False)
                errors = evaluation.get("errors", [])
                warnings = evaluation.get("warnings", [])
                suggestions = evaluation.get("suggestions", [])
                score = evaluation.get("score", 0.0)
                explanation = evaluation.get("explanation", "No explanation provided.")
                
                # Validate and ensure proper types
                if not isinstance(errors, list):
                    errors = [str(errors)] if errors else []
                if not isinstance(warnings, list):
                    warnings = [str(warnings)] if warnings else []
                if not isinstance(suggestions, list):
                    suggestions = [str(suggestions)] if suggestions else []
                if not isinstance(score, (int, float)):
                    try:
                        score = float(score)
                    except (ValueError, TypeError):
                        score = 0.0
                
                # Cap score between 0 and 100
                score = max(0.0, min(100.0, score))
                
                return {
                    "valid": valid,
                    "errors": errors,
                    "warnings": warnings,
                    "suggestions": suggestions,
                    "score": score,
                    "explanation": explanation
                }
                
            except json.JSONDecodeError:
                # If JSON parsing fails, extract information manually
                self.logger.error(f"Error parsing evaluation JSON: {evaluation_text}")
                
                # Try to extract information from the text
                lines = evaluation_text.split("\n")
                errors = []
                warnings = []
                suggestions = []
                score = 0.0
                explanation = evaluation_text  # Use the full text as explanation
                
                # Extract information based on common patterns
                for line in lines:
                    line = line.strip()
                    if "ERROR:" in line or "Error:" in line:
                        errors.append(line)
                    elif "WARNING:" in line or "Warning:" in line:
                        warnings.append(line)
                    elif "SUGGESTION:" in line or "Suggestion:" in line:
                        suggestions.append(line)
                    elif "SCORE:" in line or "Score:" in line:
                        try:
                            score_part = line.split(":", 1)[1].strip()
                            score = float(score_part.split("/")[0])  # Handle formats like "75/100"
                        except (ValueError, IndexError):
                            pass
                
                return {
                    "valid": len(errors) == 0,
                    "errors": errors,
                    "warnings": warnings,
                    "suggestions": suggestions,
                    "score": score,
                    "explanation": explanation
                }
                
        except Exception as e:
            self.logger.error(f"Error evaluating code: {e}")
            self.logger.error(traceback.format_exc())
            
            return {
                "valid": False,
                "errors": [f"Evaluation error: {str(e)}"],
                "warnings": [],
                "suggestions": [],
                "score": 0.0,
                "explanation": f"An error occurred during evaluation: {str(e)}"
            }
    
    def _build_evaluation_prompt(self, evaluation_mode: str) -> str:
        """
        Build the system prompt for code evaluation.
        
        Args:
            evaluation_mode: The evaluation mode.
            
        Returns:
            str: The system prompt.
        """
        # Base prompt for all evaluation modes
        base_prompt = """
You are an expert code evaluator specializing in Python code for the Reachy 2 robot.
Your job is to thoroughly analyze code snippets and provide detailed feedback on correctness, safety, and quality.

You must evaluate the code based on the following criteria:
1. Syntax and Structure: Check for syntax errors and proper code structure
2. API Usage: Verify correct usage of the Reachy 2 SDK API
3. Safety: Analyze potential safety issues with robot operation
4. Error Handling: Check for proper error handling and recovery mechanisms
5. Code Quality: Assess overall code quality, readability, and maintainability

CRITICAL REQUIREMENTS FOR REACHY CODE:
- Robot code MUST connect to the robot: ReachySDK(host="...")
- Robot code MUST call reachy.turn_on() before any movement
- Robot code MUST call reachy.turn_off_smoothly() (NOT turn_off()) and reachy.disconnect() in cleanup
- Robot code MUST use properties correctly (e.g., reachy.r_arm NOT reachy.r_arm())
- For arm.goto(), it MUST provide EXACTLY 7 joint values
- Gripper control MUST be through arm.gripper property (e.g., reachy.r_arm.gripper)

PROPERTY VS METHOD USAGE:
- Properties are accessed WITHOUT parentheses: 
  ✅ right_arm = reachy.r_arm
  ❌ right_arm = reachy.r_arm()

- The following are PROPERTIES (no parentheses): 
  * r_arm, l_arm, head, mobile_base, cameras, joints, gripper

- Gripper access must be through arm property:
  ✅ reachy.r_arm.gripper.open()
  ❌ reachy.r_gripper.open()
  ❌ reachy.r_arm().gripper().open()

SAFETY CHECKS:
- Check for unreachable target positions in Cartesian space
- Verify target positions are within safe workspace limits
- Ensure proper error handling for inverse kinematics
- Check for proper cleanup in finally blocks

You MUST return your evaluation in JSON format with the following fields:
{
  "valid": boolean,
  "errors": [list of critical errors],
  "warnings": [list of non-critical warnings],
  "suggestions": [list of improvement suggestions],
  "score": float (0-100),
  "explanation": string (explanation of evaluation)
}

Be extremely thorough and provide actionable feedback. Consider the original user request when evaluating if the code meets the user's requirements.
"""

        # Additional instructions based on evaluation mode
        mode_specific_instructions = ""
        
        if evaluation_mode == "detailed":
            mode_specific_instructions = """
DETAILED EVALUATION MODE:
Provide highly detailed feedback on all aspects of the code, including:
- Comprehensive analysis of each function and code block
- Detailed suggestions for improvement with code examples
- Compare different approaches that could have been used
- Evaluate how well the code meets the specific requirements from the user request
- Provide a detailed scoring breakdown for each evaluation criterion
"""
        elif evaluation_mode == "safety-focus":
            mode_specific_instructions = """
SAFETY-FOCUSED EVALUATION MODE:
Focus primarily on safety aspects of the robot code:
- Extensively evaluate workspace boundaries and joint limit safety
- Analyze potential collision scenarios
- Evaluate error recovery mechanisms
- Check for proper shutdown sequences
- Assess the robustness of inverse kinematics error handling
- Consider edge cases that could lead to unsafe robot behavior
"""
        
        # Combine the prompts
        return base_prompt + mode_specific_instructions
    
    def summarize_evaluation(self, result: EvaluationResult) -> str:
        """
        Summarize the evaluation result in a human-readable format.
        
        Args:
            result: The evaluation result.
            
        Returns:
            str: A summary of the evaluation result.
        """
        summary = []
        
        # Add a header with the overall score
        summary.append(f"## Code Evaluation Score: {result['score']:.1f}/100")
        
        # Add validity status
        if result['valid']:
            summary.append("✅ **Valid code**")
        else:
            summary.append("❌ **Invalid code**")
        
        # Add errors section if there are any
        if result['errors']:
            summary.append("\n### Critical Errors:")
            for error in result['errors']:
                summary.append(f"- 🚫 {error}")
        
        # Add warnings section if there are any
        if result['warnings']:
            summary.append("\n### Warnings:")
            for warning in result['warnings']:
                summary.append(f"- ⚠️ {warning}")
        
        # Add suggestions section if there are any
        if result['suggestions']:
            summary.append("\n### Suggestions:")
            for suggestion in result['suggestions']:
                summary.append(f"- 💡 {suggestion}")
        
        # Add explanation if there is one
        if result['explanation']:
            summary.append("\n### Explanation:")
            summary.append(result['explanation'])
        
        return "\n".join(summary) 