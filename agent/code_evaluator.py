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
        
        # Build the system prompt for code evaluation
        system_prompt = """You are a Python code evaluator specialized in Reachy 2 robot code.
You will analyze code for safety, correctness, and proper API usage, providing detailed feedback.

EVALUATION CRITERIA:
1. CORRECTNESS: Does the code fulfill the user's request? Does it accomplish the task properly?
2. SAFETY: Does the code use safe position ranges? Does it prevent damage to the robot?
3. API USAGE: Does the code correctly use the Reachy 2 SDK API?
4. ERROR HANDLING: Does the code include proper error handling, especially for inverse kinematics?
5. CODE STRUCTURE: Does the code follow the required structure with initialization, operation, and cleanup?
6. CODE QUALITY: Is the code well-structured, documented, and maintainable?

REQUIRED CODE STRUCTURE:
A. INITIALIZATION PHASE:
   - Import ReachySDK from reachy2_sdk
   - Import time module for sleep calls
   - Connect to the robot: reachy = ReachySDK(host="localhost")
   - Turn on the robot: reachy.turn_on()
   - Reset posture: reachy.goto_posture('default')

B. MAIN CODE PHASE:
   - Implement the requested functionality
   - Add time.sleep() after movement commands
   - Use try/except blocks for error handling

C. CLEANUP PHASE:
   - Use a finally block for cleanup operations
   - Turn off robot smoothly: reachy.turn_off_smoothly() (NOT turn_off())
   - Disconnect: reachy.disconnect()

CRITICAL SAFETY REQUIREMENTS:
1. ALWAYS use turn_on() before movement
2. ALWAYS use turn_off_smoothly() NOT turn_off()
3. ALWAYS disconnect() when done
4. For arm.goto(), provide EXACTLY 7 joint values
5. Properties are accessed WITHOUT parentheses (e.g., reachy.r_arm NOT reachy.r_arm())
6. Gripper is accessed through arm property (e.g., reachy.r_arm.gripper.open())
7. ALWAYS use try/finally blocks for proper cleanup
8. ALWAYS handle "Target was not reachable" errors when using inverse kinematics

WORKSPACE SAFETY:
- These values are provided as general guidelines based on observed behavior, not absolute limits
- Reachable workspace is approximately a sphere around each shoulder with arm's length radius
- Typical effective reach: positions within ~0.6 meters of the robot's torso
- For right arm Cartesian control, common reachable values include:
  * X: 0.2 to 0.5 meters (forward from chest)
  * Y: -0.5 to -0.1 meters (right side of robot)
  * Z: -0.2 to 0.4 meters (vertical axis)
- For left arm Cartesian control, common reachable values include:
  * X: 0.2 to 0.5 meters (forward from chest)
  * Y: 0.1 to 0.5 meters (left side of robot)
  * Z: -0.2 to 0.4 meters (vertical axis)
- Values outside these ranges may be unreachable or require awkward joint configurations
- Note that reachability also depends on the orientation, not just position
- For most reliable operation, stay well within these limits and use joint control

CONTROL METHODOLOGY GUIDANCE:
- STRONGLY PREFER joint control over Cartesian control whenever possible
- Joint control is MORE RELIABLE as it directly controls motors without inverse kinematics calculations
- Joint control GUARANTEES the position is reachable (if within joint limits)
- Cartesian control often fails with "Target not reachable" errors even for seemingly valid positions
- When joint control is used, arm movements are more predictable and safer
- If Cartesian control must be used, ALWAYS implement proper error handling with fallback to joint control
- For simple point-to-point movements, joint control should be the default approach
- Pre-defined joint configurations are safer than attempting to calculate them through inverse kinematics

IDEAL JOINT ANGLE CONFIGURATIONS:
- Right arm extended forward: [0, 0, 0, -90, 0, 0, 0]
- Right arm slightly to the side: [0, 10, -10, -90, 0, 0, 0]
- Right arm upward: [-45, 0, 0, -45, 0, 0, 0]
- Left arm extended forward: [0, 0, 0, -90, 0, 0, 0]
- Left arm slightly to the side: [0, -10, 10, -90, 0, 0, 0]
- Left arm upward: [-45, 0, 0, -45, 0, 0, 0]

REAL SDK EXAMPLES FROM OFFICIAL REPOSITORY:
1. BASIC SETUP AND POSTURE EXAMPLE:
```python
# From set_default_posture.py
import logging
import time
from reachy2_sdk import ReachySDK

# Connect to Reachy
reachy = ReachySDK(host="localhost")

# Check if connection is successful
if not reachy.is_connected:
    exit("Reachy is not connected.")

# Print basic information
print("Reachy basic information:")
print(reachy.info)
print("Reachy joint status:")
print(reachy.r_arm.joints)

# Turning on Reachy
print("Turning on Reachy...")
reachy.turn_on()

time.sleep(0.2)

# Set to default posture
print("Set to default posture...")
reachy.goto_posture("default")
```

2. PROPER ARM CONTROL AND INVERSE KINEMATICS WITH ERROR HANDLING:
```python
# Adapted from draw_square.py
import logging
import time
import numpy as np
from reachy2_sdk import ReachySDK

# Connect to Reachy
reachy = ReachySDK(host="localhost")
if not reachy.is_connected:
    exit("Reachy is not connected.")

try:
    # Initialize Reachy
    print("Turning on Reachy")
    reachy.turn_on()
    time.sleep(0.2)
    
    # Set to initial posture  
    print("Set to Elbow 90 pose ...")
    reachy.goto_posture("elbow_90", wait=True)
    
    # Build a target pose matrix
    target_pose = np.array([
        [0, 0, -1, 0.4],
        [0, 1, 0, -0.3],
        [1, 0, 0, 0],
        [0, 0, 0, 1]
    ])
    
    # Use inverse kinematics with error handling
    try:
        # Get the position in the joint space
        joints_positions = reachy.r_arm.inverse_kinematics(target_pose)
        # Move Reachy's right arm to this point
        reachy.r_arm.goto(joints_positions, duration=2, wait=True)
    except ValueError as e:
        print(f"Target position unreachable: {e}")
        # Use a fallback safe position
        reachy.r_arm.goto([0, 10, -10, -90, 0, 0, 0], duration=2)
        
    # Get current position for feedback
    current_pos = reachy.r_arm.forward_kinematics()
    print("Current pose: ", current_pos)
    
    # Return to default posture
    reachy.goto_posture("default", wait=True)
    
finally:
    # Proper cleanup
    time.sleep(0.2)
    reachy.turn_off_smoothly()
    reachy.disconnect()
```

3. GRIPPER CONTROL EXAMPLE:
```python
# From arm_and_gripper examples
from reachy2_sdk import ReachySDK
import time

# Connect to the robot
reachy = ReachySDK(host="localhost")
try:
    # Initialize
    reachy.turn_on()
    reachy.goto_posture("elbow_90", wait=True)
    
    # Open/close gripper with proper waiting
    reachy.r_arm.gripper.close()
    while reachy.r_arm.gripper.is_moving():
        time.sleep(0.1)
    
    reachy.r_arm.gripper.open()
    while reachy.r_arm.gripper.is_moving():
        time.sleep(0.1)
    
    # Partial opening and position checking
    reachy.r_arm.gripper.set_opening(55)
    while reachy.r_arm.gripper.is_moving():
        time.sleep(0.1)
    
    current_opening = reachy.r_arm.gripper.get_current_opening()
    print(f"Current gripper opening: {current_opening}")
    
finally:
    # Return to default posture and turn off
    reachy.goto_posture("default", wait=True)
    reachy.turn_off_smoothly()
    reachy.disconnect()
```

COMMON ERRORS TO CHECK:
1. Syntax errors or runtime errors
2. Missing import for ReachySDK from reachy2_sdk
3. Missing robot connection setup: ReachySDK(host=...)
4. Missing reachy.turn_on() call
5. Using turn_off() instead of turn_off_smoothly()
6. Missing finally block for cleanup
7. Missing reachy.disconnect() in cleanup
8. Incorrect property usage with parentheses (e.g., reachy.r_arm())
9. Incorrect gripper access (should be reachy.r_arm.gripper)
10. arm.goto() with incorrect number of joint values (must be 7)
11. Potential security risks (os.system, subprocess, eval, exec)
12. Non-API code usage (internal functions not in the official SDK)
13. Missing try/except for inverse_kinematics
14. Missing fallback strategy if inverse kinematics fails
15. Using identity rotation matrix for Cartesian control
16. Using Cartesian control when joint control would be simpler and more reliable
17. Overreliance on complex kinematics without proper error handling
18. Not using pre-defined postures (default, elbow_90) when appropriate

PROVIDE YOUR EVALUATION IN THIS JSON FORMAT:
{
  "valid": true/false,
  "score": 0-100,
  "errors": ["error1", "error2"],
  "warnings": ["warning1", "warning2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "explanation": "Overall explanation"
}

SCORING GUIDELINES:
- 90-100: Excellent code, no errors, follows all guidelines
- 75-89: Good code with minor issues or lacking some best practices
- 50-74: Functional code with some warnings or safety concerns
- 25-49: Poor code with multiple errors but fixable
- 0-24: Severely problematic code with critical errors

Your evaluation must be comprehensive, detailed, and precise, focused on helping improve the code."""
        
        # Build the user prompt with the code and request
        user_prompt = f"""
ORIGINAL USER REQUEST:
{user_request}

GENERATED CODE TO EVALUATE:
```python
{code}
```

Please evaluate this code based on all the criteria and guidelines specified.
Provide a thorough analysis, listing any errors, warnings, and specific improvement suggestions.
Consider both technical correctness and safety for the Reachy 2 robot.
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