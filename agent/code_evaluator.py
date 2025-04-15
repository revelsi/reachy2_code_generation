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
from config import OPENAI_API_KEY, MODEL, EVALUATOR_MODEL

# Import the prompt_config module
from agent.prompt_config import build_evaluator_prompt

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
        model: str = EVALUATOR_MODEL,
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
        
        self.logger.debug(f"Initialized code evaluator with model: {model}")
    
    def evaluate_code(
        self, 
        code: str, 
        user_request: str
    ) -> EvaluationResult:
        """
        Evaluate the generated code for correctness, safety, and quality.
        
        Args:
            code: The code to evaluate.
            user_request: The original user request for context.
            
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
        
        # Build the system prompt for code evaluation using the unified prompt system
        system_prompt = build_evaluator_prompt()
        
        # Add the user's context to the message
        user_message = f"""
ORIGINAL USER REQUEST:
{user_request}

CODE TO EVALUATE:
```python
{code}
```

Evaluate this code for correctness, safety, proper API usage, and code quality.
Follow the scoring guidelines and provide a detailed JSON response as specified.
"""
        
        try:
            # Call the OpenAI API
            # GPT models use standard parameters
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "response_format": {"type": "json_object"}  # Request JSON format
            }
                
            # Make the API call
            response = self.client.chat.completions.create(**params)
            
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
                
                result = {
                    "valid": valid,
                    "errors": errors,
                    "warnings": warnings,
                    "suggestions": suggestions,
                    "score": score,
                    "explanation": explanation
                }
                
                self.logger.info(f"Evaluation complete: Score: {score}/100, Valid: {valid}")
                return result
                
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Error parsing evaluation JSON: {json_error}")
                self.logger.error(f"Raw response: {evaluation_text}")
                
                # Create a fallback evaluation
                return {
                    "valid": False,
                    "errors": ["Error parsing evaluation JSON"],
                    "warnings": [],
                    "suggestions": ["Try generating code again"],
                    "score": 0.0,
                    "explanation": f"Error parsing evaluation response: {str(json_error)}"
                }
                
        except Exception as e:
            self.logger.error(f"Error evaluating code: {e}")
            self.logger.error(traceback.format_exc())
            
            # Create an error evaluation
            return {
                "valid": False,
                "errors": [f"Error during evaluation: {str(e)}"],
                "warnings": [],
                "suggestions": [],
                "score": 0.0,
                "explanation": f"An error occurred during evaluation: {str(e)}"
            }
    
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