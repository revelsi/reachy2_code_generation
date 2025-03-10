#!/usr/bin/env python
"""
Code Generation Agent for the Reachy 2 robot.

This module provides an agent that generates Python code for interacting with the Reachy 2 robot
based on natural language requests, using only the official Reachy 2 SDK API.
"""

import os
import sys
import json
import logging
import traceback
from typing import Dict, List, Any, Optional, TypedDict, Tuple
from openai import OpenAI
import httpx
import re

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code_generation_agent")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import OPENAI_API_KEY, MODEL

# Import WebSocket server for notifications
from api.websocket import get_websocket_server

# Configure OpenAI client with custom settings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", OPENAI_API_KEY),
    timeout=30.0,
    max_retries=2,
    base_url="https://api.openai.com/v1",
    http_client=httpx.Client(
        transport=httpx.HTTPTransport(retries=2),
        timeout=30.0,
        verify=True
    )
)

# WebSocket server for notifications
websocket_server = get_websocket_server()


class CodeValidationResult(TypedDict):
    """Result of code validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]


def load_api_documentation():
    """
    Load the API documentation from the JSON file.
    
    Returns:
        list: The API documentation.
    """
    try:
        doc_path = os.path.join(os.path.dirname(__file__), "docs", "api_documentation.json")
        with open(doc_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading API documentation: {e}")
        return []


def extract_parameter_details(signature: str, docstring: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract detailed parameter information from a function signature and docstring.
    
    Args:
        signature: The function signature
        docstring: The function docstring
        
    Returns:
        Dict mapping parameter names to their details
    """
    param_details = {}
    
    # Extract parameter names and types from signature
    if signature:
        # Extract the part between parentheses
        params_part = signature.split('(', 1)[1].rsplit(')', 1)[0] if '(' in signature else ""
        
        # Split by comma, but handle nested types with commas
        params = []
        current_param = ""
        bracket_count = 0
        
        for char in params_part:
            if char == ',' and bracket_count == 0:
                params.append(current_param.strip())
                current_param = ""
            else:
                current_param += char
                if char in '[{(':
                    bracket_count += 1
                elif char in ']})':
                    bracket_count -= 1
        
        if current_param:
            params.append(current_param.strip())
        
        # Process each parameter
        for param in params:
            if ':' in param:
                name, type_info = param.split(':', 1)
                name = name.strip()
                type_info = type_info.strip()
                
                # Skip 'self' parameter
                if name == 'self':
                    continue
                
                param_details[name] = {
                    "type": type_info,
                    "description": "",
                    "constraints": []
                }
    
    # Extract parameter descriptions from docstring
    if docstring:
        lines = docstring.split('\n')
        in_args_section = False
        current_param = None
        
        for line in lines:
            line = line.strip()
            
            # Check if we're in the Args section
            if line.startswith("Args:"):
                in_args_section = True
                continue
            
            # Check if we've left the Args section
            if in_args_section and (not line or line.startswith("Returns:") or line.startswith("Raises:")):
                in_args_section = False
                current_param = None
                continue
            
            # Process parameter descriptions
            if in_args_section:
                if ': ' in line:
                    # New parameter
                    param_name, param_desc = line.split(': ', 1)
                    param_name = param_name.strip()
                    
                    if param_name in param_details:
                        current_param = param_name
                        param_details[param_name]["description"] = param_desc.strip()
                        
                        # Extract constraints from description
                        desc_lower = param_desc.lower()
                        if "must be" in desc_lower or "should be" in desc_lower or "required" in desc_lower:
                            param_details[param_name]["constraints"].append(param_desc.strip())
                        
                        # Check for units information
                        if "degrees" in desc_lower or "radians" in desc_lower:
                            if "degrees" in desc_lower:
                                param_details[param_name]["units"] = "degrees"
                            else:
                                param_details[param_name]["units"] = "radians"
                elif current_param and line:
                    # Continuation of previous parameter description
                    param_details[current_param]["description"] += " " + line
                    
                    # Check for additional constraints
                    line_lower = line.lower()
                    if "must be" in line_lower or "should be" in line_lower or "required" in line_lower:
                        param_details[current_param]["constraints"].append(line.strip())
    
    return param_details


def add_special_constraints(class_name: str, method_name: str, param_details: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Add special constraints for known problematic functions.
    
    Args:
        class_name: The class name
        method_name: The method name
        param_details: The current parameter details
        
    Returns:
        Updated parameter details
    """
    # Special case for Arm.goto
    if class_name == "Arm" and method_name == "goto" and "target" in param_details:
        if "constraints" not in param_details["target"]:
            param_details["target"]["constraints"] = []
        
        param_details["target"]["constraints"].append("When target is a list, it MUST contain EXACTLY 7 joint values")
        param_details["target"]["constraints"].append("When using degrees=True, values should be in degrees; otherwise in radians")
    
    # Special case for ReachySDK initialization
    if class_name == "ReachySDK" and method_name == "__init__" and "host" in param_details:
        if "constraints" not in param_details["host"]:
            param_details["host"]["constraints"] = []
        
        param_details["host"]["constraints"].append("host parameter is REQUIRED (e.g., 'localhost' or IP address)")
    
    return param_details


def generate_api_summary(api_docs):
    """
    Generate a summary of the API documentation with enhanced parameter details.
    
    Args:
        api_docs: The API documentation.
        
    Returns:
        str: A summary of the API documentation.
    """
    if not api_docs:
        return "No API documentation available."
    
    # Define the official API modules (these are the ones from the Reachy SDK)
    official_api_modules = [
        "reachy2_sdk.reachy_sdk",
        "reachy2_sdk.parts",
        "reachy2_sdk.utils",
        "reachy2_sdk.config",
        "reachy2_sdk.media",
        "reachy2_sdk.orbita",
        "reachy2_sdk.sensors",
        "pollen_vision"
    ]
    
    # Extract classes and their methods with enhanced details
    classes = {}
    official_modules = set()
    official_classes = set()
    
    for item in api_docs:
        # Track official modules (only if they're in the official list)
        if item.get("type") == "module":
            module_name = item.get("name")
            if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                official_modules.add(module_name)
        
        # Process classes (only if they're from official modules)
        if item.get("type") == "class":
            class_name = item.get("name")
            module_name = item.get("module", "")
            
            # Only include classes from official modules
            if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                # Add to official classes
                if class_name:
                    official_classes.add(class_name)
                
                methods = []
                
                # Get methods for this class
                for method in item.get("methods", []):
                    method_name = method.get("name")
                    signature = method.get("signature", "")
                    docstring = method.get("docstring", "")
                    
                    if method_name and not method_name.startswith("_"):  # Skip private methods
                        # Extract parameter details
                        param_details = extract_parameter_details(signature, docstring)
                        
                        # Add special constraints for known problematic functions
                        param_details = add_special_constraints(class_name, method_name, param_details)
                        
                        # Format the method information
                        method_info = {
                            "name": method_name,
                            "signature": signature,
                            "docstring": docstring.split("\n")[0] if docstring else "",  # First line of docstring
                            "parameters": param_details
                        }
                        
                        methods.append(method_info)
                
                if methods:
                    classes[class_name] = methods
    
    # Format the enhanced summary
    summary = []
    
    # Add official modules
    summary.append("# Official Modules")
    for module in sorted(official_modules):
        summary.append(f"- {module}")
    summary.append("")
    
    # Add official classes
    summary.append("# Official Classes")
    for class_name in sorted(official_classes):
        summary.append(f"- {class_name}")
    summary.append("")
    
    # Add class methods with enhanced details
    summary.append("# Class Methods with Parameter Details")
    for class_name, methods in sorted(classes.items()):
        summary.append(f"## {class_name}")
        
        for method in sorted(methods, key=lambda x: x["name"]):
            method_name = method["name"]
            signature = method["signature"]
            docstring = method["docstring"]
            
            summary.append(f"### {method_name}{signature}")
            first_line = docstring.split('\n')[0] if docstring else ''
            summary.append(f"{first_line}")
            
            # Add parameter details
            if method["parameters"]:
                summary.append("Parameters:")
                for param_name, param_info in method["parameters"].items():
                    param_type = param_info.get("type", "")
                    param_desc = param_info.get("description", "")
                    
                    summary.append(f"- {param_name} ({param_type}): {param_desc}")
                    
                    # Add constraints if any
                    constraints = param_info.get("constraints", [])
                    if constraints:
                        summary.append("  Constraints:")
                        for constraint in constraints:
                            summary.append(f"  * {constraint}")
                    
                    # Add units if specified
                    if "units" in param_info:
                        summary.append(f"  * Units: {param_info['units']}")
            
            summary.append("")
        
        summary.append("")
    
    return "\n".join(summary)


class ReachyCodeGenerationAgent:
    """
    An agent that generates Python code for interacting with the Reachy 2 robot.
    
    This agent uses the OpenAI API to generate Python code based on natural language requests,
    and provides validation and explanation of the generated code.
    """
    
    def __init__(
        self, 
        model: str = "gpt-4o-mini", 
        api_key: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 4000,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0
    ):
        """
        Initialize the code generation agent.
        
        Args:
            model: The OpenAI model to use.
            api_key: The OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            temperature: The temperature for the model (0.0 to 1.0).
            max_tokens: The maximum number of tokens to generate.
            top_p: The top_p value for the model (0.0 to 1.0).
            frequency_penalty: The frequency penalty for the model (-2.0 to 2.0).
            presence_penalty: The presence penalty for the model (-2.0 to 2.0).
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = client  # Use the configured client
        
        logger.debug(f"Initialized code generation agent with model: {model}")
        
        # Conversation history
        self.messages = []
        
        # Load API documentation
        self.api_docs = load_api_documentation()
        self.api_summary = generate_api_summary(self.api_docs)
        
        # Extract official modules and classes for validation
        self.official_modules = set()
        self.official_classes = set()
        self._extract_official_api_elements()
        
        # System prompt for the agent
        self.system_prompt = f"""
        You are an AI assistant that generates Python code for controlling a Reachy 2 robot.
        
        OFFICIAL REACHY 2 SDK MODULES:
        - reachy2_sdk.reachy_sdk
        - reachy2_sdk.parts
        - reachy2_sdk.utils
        - reachy2_sdk.config
        - reachy2_sdk.media
        - reachy2_sdk.orbita
        - reachy2_sdk.sensors
        - pollen_vision
        
        CRITICAL WARNINGS:
        - NEVER use 'get_reachy()' or any functions from 'connection_manager.py'
        - Carefully read the API documentation and make sure you follow the arguments and parameters guidelines.
        - ALWAYS use properties correctly (e.g., reachy.r_arm NOT reachy.r_arm())
        - For arm goto(), ALWAYS provide EXACTLY 7 joint values
        
        REQUIRED CODE STRUCTURE:
        
        1. INITIALIZATION PHASE:
           - Import ReachySDK from reachy2_sdk
           - Connect to the robot: reachy = ReachySDK(host="localhost")
           - ALWAYS call reachy.turn_on() before any movement
           - ALWAYS call reachy.goto_posture('default') before any movement to reset the posture
        
        2. MAIN CODE PHASE:
           - Always use try/finally blocks for error handling
           - Access parts as properties (reachy.r_arm, reachy.head, etc.)
           - Use proper method signatures from the API documentation
        
        3. CLEANUP PHASE:
           - ALWAYS use reachy.turn_off_smoothly() (NOT turn_off())
           - ALWAYS call reachy.disconnect()
           - Put cleanup in a finally block
        
        EXAMPLE CODE TEMPLATE:
        ```python
        from reachy2_sdk import ReachySDK
        
        # Connect to the robot
        reachy = ReachySDK(host="localhost")
        
        try:
            # INITIALIZATION
            reachy.turn_on()
            
            # MAIN CODE
            # Your code here...
            
        finally:
            # CLEANUP
            reachy.turn_off_smoothly()
            reachy.disconnect()
        ```
        
        POLLEN VISION USAGE EXAMPLES:
        
        1. Object Detection with OwlVitWrapper:
        ```python
        from reachy2_sdk import ReachySDK
        from pollen_vision.vision_models.object_detection import OwlVitWrapper
        import numpy as np
        
        # Connect to the robot
        reachy = ReachySDK(host="localhost")
        
        try:
            # INITIALIZATION
            reachy.turn_on()
            
            # Access the camera
            camera = reachy.cameras.teleop()
            
            # Capture an image
            frame, _ = camera.get_frame(view=camera.CameraView.LEFT)
            
            # Initialize object detection
            detector = OwlVitWrapper()
            
            # Detect objects
            candidate_labels = ["apple", "banana", "cup"]
            detection_threshold = 0.1
            predictions = detector.infer(frame, candidate_labels, detection_threshold)
            
            # Process predictions
            if predictions:
                print(f"Detected {{len(predictions)}} objects")
                for pred in predictions:
                    print(f"Found {{pred['label']}} with confidence {{pred['confidence']}}")
            
        finally:
            # CLEANUP
            reachy.turn_off_smoothly()
            reachy.disconnect()
        ```
        
        2. Depth Estimation with DepthAnythingWrapper:
        ```python
        from reachy2_sdk import ReachySDK
        from pollen_vision.vision_models.monocular_depth_estimation import DepthAnythingWrapper
        import numpy as np
        
        # Connect to the robot
        reachy = ReachySDK(host="localhost")
        
        try:
            # INITIALIZATION
            reachy.turn_on()
            
            # Access the camera
            camera = reachy.cameras.teleop()
            
            # Capture an image
            frame, _ = camera.get_frame(view=camera.CameraView.LEFT)
            
            # Initialize depth estimation
            depth_estimator = DepthAnythingWrapper()
            
            # Get depth information
            depth_map = depth_estimator.get_depth(frame)
            
            # Process depth information
            print(f"Depth map shape: {{depth_map.shape}}")
            print(f"Average depth: {{np.mean(depth_map)}}")
            
        finally:
            # CLEANUP
            reachy.turn_off_smoothly()
            reachy.disconnect()
        ```
        
        Here is a summary of the available API classes and methods:
        
        {self.api_summary}
        
        Format your response with:
        1. A brief explanation of what the code does
        2. The complete Python code in a code block
        3. An explanation of how the code works and any important considerations
        """
        
        # Initialize conversation with system message
        self.reset_conversation()
    
    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        logger.debug("Reset conversation history")
    
    def process_message(self, message: str, max_correction_attempts: int = 3) -> Dict[str, Any]:
        """
        Process a user message and generate code.
        
        Args:
            message: The user message.
            max_correction_attempts: Maximum number of attempts to correct validation errors.
            
        Returns:
            Dict[str, Any]: The response, including generated code and validation results.
        """
        try:
            # Add user message to conversation history
            self.messages.append({"role": "user", "content": message})
            
            # Generate code
            code_response = self._generate_code()
            
            # Extract code from response
            code, explanation = self._extract_code_and_explanation(code_response)
            
            # Validate code
            validation_result = self._validate_code(code)
            
            # Attempt to correct validation errors recursively
            correction_attempts = 0
            while not validation_result["valid"] and correction_attempts < max_correction_attempts:
                correction_attempts += 1
                logger.info(f"Validation failed. Attempting correction (attempt {correction_attempts}/{max_correction_attempts})")
                
                # Create error feedback message
                error_feedback = f"The code you generated has the following errors that need to be fixed:\n"
                for error in validation_result["errors"]:
                    error_feedback += f"- {error}\n"
                
                # Add error feedback to conversation history
                self.messages.append({"role": "user", "content": error_feedback})
                
                # Generate corrected code
                code_response = self._generate_code()
                
                # Extract corrected code
                code, explanation = self._extract_code_and_explanation(code_response)
                
                # Validate corrected code
                validation_result = self._validate_code(code)
                
                # If validation passes, break the loop
                if validation_result["valid"]:
                    logger.info(f"Code corrected successfully after {correction_attempts} attempts")
                    break
            
            # Add final assistant response to conversation history
            self.messages.append({"role": "assistant", "content": code_response})
            
            # Prepare response
            response = {
                "message": explanation,
                "code": code,
                "validation": validation_result,
                "raw_response": code_response,
                "correction_attempts": correction_attempts
            }
            
            # Send notification via WebSocket
            self._send_websocket_notification(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "message": f"Error generating code: {str(e)}"
            }
    
    def _generate_code(self) -> str:
        """
        Generate Python code using the OpenAI API.
        
        Returns:
            str: The generated code response.
        """
        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty
            )
            
            # Extract and return the response content
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Failed to generate code: {e}")
    
    def _extract_code_and_explanation(self, response: str) -> tuple[str, str]:
        """
        Extract code and explanation from the response.
        
        Args:
            response: The response from the OpenAI API.
            
        Returns:
            tuple[str, str]: The extracted code and explanation.
        """
        # Look for code blocks
        import re
        code_blocks = re.findall(r'```(?:python)?\n(.*?)```', response, re.DOTALL)
        
        if code_blocks:
            # Extract the first code block
            code = code_blocks[0].strip()
            
            # Remove code blocks from the response to get the explanation
            explanation = re.sub(r'```(?:python)?\n.*?```', '', response, flags=re.DOTALL).strip()
            
            return code, explanation
        else:
            # No code blocks found, return empty code and the full response as explanation
            return "", response
    
    def _extract_official_api_elements(self):
        """Extract official modules and classes from the API documentation."""
        if not self.api_docs:
            logger.warning("No API documentation available for extracting official elements")
            return
        
        # Define the official API modules (these are the ones from the Reachy SDK)
        official_api_modules = [
            "reachy2_sdk.reachy_sdk",
            "reachy2_sdk.parts",
            "reachy2_sdk.utils",
            "reachy2_sdk.config",
            "reachy2_sdk.media",
            "reachy2_sdk.orbita",
            "reachy2_sdk.sensors",
            "pollen_vision"
        ]
            
        for item in self.api_docs:
            if item.get("type") == "module":
                module_name = item.get("name")
                # Only include modules from the official list
                if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                    self.official_modules.add(module_name)
            
            if item.get("type") == "class":
                class_name = item.get("name")
                module_name = item.get("module", "")
                # Only include classes from official modules
                if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                    if class_name:
                        self.official_classes.add(class_name)
        
        logger.debug(f"Extracted {len(self.official_modules)} official modules and {len(self.official_classes)} official classes")
    
    def _validate_code(self, code: str) -> CodeValidationResult:
        """
        Validate the generated code.
        
        Args:
            code: The generated code.
            
        Returns:
            CodeValidationResult: The validation result.
        """
        if not code:
            return {
                "valid": False,
                "errors": ["No code was generated"],
                "warnings": []
            }
        
        errors = []
        warnings = []
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
        
        # Check for required imports
        if "from reachy2_sdk import ReachySDK" not in code:
            warnings.append("Missing import for ReachySDK from reachy2_sdk")
        
        # Check for connection setup
        if "ReachySDK(" not in code:
            warnings.append("Code does not initialize ReachySDK to establish a connection")
        
        # Check for turn_on
        if "turn_on()" not in code:
            warnings.append("CRITICAL: Missing reachy.turn_on() call. Always turn on the robot before using it.")
        
        # Check for turn_off_smoothly instead of turn_off
        if "turn_off()" in code:
            warnings.append("CRITICAL: Using turn_off() instead of turn_off_smoothly(). Always use turn_off_smoothly() to prevent damage to the robot.")
        
        if "turn_off_smoothly()" not in code:
            warnings.append("CRITICAL: Missing reachy.turn_off_smoothly() call. Always turn off the robot smoothly when done.")
        
        # Check for error handling
        if "try:" not in code:
            warnings.append("No error handling (try/except) found in the code")
        
        # Check for cleanup
        if "disconnect()" not in code:
            warnings.append("No disconnect operation found in the code")
        
        # Check for finally block
        if "finally:" not in code:
            warnings.append("No finally block found for ensuring cleanup operations")
        
        # Check for potentially unsafe operations
        unsafe_patterns = [
            "os.system", "subprocess", "eval(", "exec(", "import shutil",
            "__import__", "open(", "pickle", "shelve", "marshal",
            "socket", "requests.post", "requests.put", "requests.delete"
        ]
        for pattern in unsafe_patterns:
            # Use more precise pattern matching to avoid false positives
            if pattern == "file(":
                # Check for the actual file() function, not substrings like "audio_file("
                import re
                if re.search(r'\bfile\(', code):
                    errors.append(f"Potentially unsafe operation detected: {pattern}")
            elif pattern in code:
                errors.append(f"Potentially unsafe operation detected: {pattern}")
        
        # Check for non-API imports and functions
        non_api_patterns = [
            "import agent", 
            "from agent", 
            "connection_manager",
            "get_reachy()",
            "get_reachy ",
            "connect_to_reachy",
            "disconnect_reachy"
        ]
        for pattern in non_api_patterns:
            if pattern in code:
                errors.append(f"Non-API code detected: The code uses internal functions that are not part of the official Reachy 2 SDK API.")
                break  # Only report this error once
        
        # Check for incorrect property usage (calling properties as methods)
        property_patterns = [
            "r_arm()", "l_arm()", "head()", "cameras()", 
            "gripper()", "r_gripper()", "l_gripper()"
        ]
        for pattern in property_patterns:
            if pattern in code:
                errors.append(f"Incorrect property usage: '{pattern}' is a property, not a method. Use without parentheses.")
        
        # Check for incorrect arm goto usage
        if "goto" in code:
            import re
            # Look for arm goto calls with incorrect number of joint positions
            arm_goto_matches = re.findall(r'(?:r_arm|l_arm|right_arm|left_arm)\.goto\s*\(\s*\[(.*?)\]', code, re.DOTALL)
            for match in arm_goto_matches:
                # Count the number of values in the joint positions array
                values = [v.strip() for v in match.split(',')]
                if len(values) != 7:
                    errors.append(f"Incorrect arm goto usage: The positions array must have exactly 7 values for the 7 joints, but found {len(values)}.")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _analyze_execution_error(self, stderr: str, output: str) -> str:
        """
        Analyze execution errors and provide helpful feedback.
        
        Args:
            stderr: Standard error output.
            output: Standard output.
            
        Returns:
            str: Helpful feedback about the error.
        """
        feedback = ""
        
        # Check for inverse kinematics errors
        if "No solution found for the given target" in stderr or "No solution found for the given target" in output:
            feedback += "INVERSE KINEMATICS ERROR: The target pose is not reachable by the robot arm.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Try a position closer to the robot's body\n"
            feedback += "2. Use a simpler orientation (e.g., facing forward)\n"
            feedback += "3. Check that the position values are within the robot's reach (typically within 0.6 meters)\n"
            feedback += "4. Consider using joint angles directly instead of inverse kinematics\n"
        
        # Check for connection errors
        elif "Failed to connect to" in stderr or "Connection refused" in stderr:
            feedback += "CONNECTION ERROR: Could not connect to the robot or simulator.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Make sure the robot or simulator is running\n"
            feedback += "2. Check that you're connecting to the correct IP address and port\n"
            feedback += "3. Verify that there are no firewall issues blocking the connection\n"
        
        # Check for import errors
        elif "ImportError" in stderr or "ModuleNotFoundError" in stderr:
            feedback += "IMPORT ERROR: Could not import required modules.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Make sure all required packages are installed\n"
            feedback += "2. Check for typos in import statements\n"
            feedback += "3. Verify that the module paths are correct\n"
        
        # Check for syntax errors
        elif "SyntaxError" in stderr:
            feedback += "SYNTAX ERROR: There's a syntax error in the generated code.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Check for missing parentheses, brackets, or quotes\n"
            feedback += "2. Verify that indentation is correct\n"
            feedback += "3. Look for typos or invalid syntax\n"
        
        # If no specific error was identified, provide general feedback
        if not feedback:
            feedback = "An error occurred during execution. Please check the error message for details."
        
        return feedback

    def execute_code(self, code: str, confirm: bool = True, force: bool = False) -> Dict[str, Any]:
        """
        Execute the generated code on the virtual Reachy robot.
        
        Args:
            code: The generated code to execute.
            confirm: Whether to ask for user confirmation before execution.
            force: Whether to force execution even if validation fails.
            
        Returns:
            Dict[str, Any]: The execution result.
        """
        if not code:
            return {
                "success": False,
                "message": "No code provided for execution",
                "output": ""
            }
        
        # Validate the code first
        validation_result = self._validate_code(code)
        
        # Check if the code is valid (but don't prevent execution if force=True)
        if not validation_result["valid"] and not force:
            # Instead of preventing execution, just add warnings and require confirmation
            validation_result["warnings"].append("Code validation failed. Execution may be risky.")
            
            # Always require confirmation for invalid code
            confirm = True
        
        # Check for critical warnings (but don't prevent execution if force=True)
        critical_warnings = [w for w in validation_result["warnings"] if "CRITICAL" in w]
        if critical_warnings and not force:
            # Instead of preventing execution, just add warnings and require confirmation
            validation_result["warnings"].append("Code contains critical issues that could damage the robot.")
            
            # Always require confirmation for code with critical warnings
            confirm = True
        
        # If confirmation is required, return the code and validation for UI to handle
        if confirm:
            return {
                "requires_confirmation": True,
                "code": code,
                "validation": validation_result,
                "message": "Code is ready for execution. Please confirm to proceed."
            }
        
        # Execute the code
        try:
            # Create a temporary file for the code
            import tempfile
            import os
            import subprocess
            import sys
            
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp_file:
                # Add basic imports and error handling
                temp_file.write("#!/usr/bin/env python3\n")
                temp_file.write("import sys\n")
                temp_file.write("import traceback\n")
                temp_file.write("import os\n\n")
                
                # Add environment setup
                temp_file.write("# Set PYTHONPATH to include current directory\n")
                temp_file.write("os.environ['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__)) + ':' + os.environ.get('PYTHONPATH', '')\n\n")
                
                # Add basic error handling
                temp_file.write("try:\n")
                # Indent the code
                indented_code = "    " + code.replace("\n", "\n    ")
                temp_file.write(indented_code)
                
                # Add exception handling
                temp_file.write("\nexcept ValueError as e:\n")
                temp_file.write("    if 'No solution found for the given target' in str(e):\n")
                temp_file.write("        print(\"ERROR: Inverse Kinematics Failed\\n\")\n")
                temp_file.write("        print(f\"{e}\\n\")\n")
                temp_file.write("        print(\"The target pose is not reachable by the robot arm. This could be because:\\n\")\n")
                temp_file.write("        print(\"1. The position is outside the robot's workspace\")\n")
                temp_file.write("        print(\"2. The orientation is not achievable with the robot's joint configuration\")\n")
                temp_file.write("        print(\"3. The arm would collide with itself or other parts of the robot\\n\")\n")
                temp_file.write("        print(\"Try adjusting the target position to be closer to the robot,\")\n")
                temp_file.write("        print(\"or use a different orientation that's easier for the robot to achieve.\")\n")
                temp_file.write("    else:\n")
                temp_file.write("        print(f\"Error executing code: {e}\")\n")
                temp_file.write("    traceback.print_exc()\n")
                temp_file.write("    sys.exit(1)\n")
                temp_file.write("except Exception as e:\n")
                temp_file.write("    print(f\"Error executing code: {e}\")\n")
                temp_file.write("    traceback.print_exc()\n")
                temp_file.write("    sys.exit(1)\n")
                
                temp_file_path = temp_file.name
            
            # Execute the code in a separate process
            logger.info(f"Executing code in {temp_file_path}")
            
            # Use the same Python interpreter that's running this code
            python_executable = sys.executable
            
            # Execute the code
            process = subprocess.Popen(
                [python_executable, temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=os.environ.copy()  # Pass the current environment variables
            )
            
            # Get the output
            stdout, stderr = process.communicate(timeout=60)  # 60 second timeout
            
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {e}")
            
            # Check if the execution was successful
            if process.returncode == 0:
                return {
                    "success": True,
                    "message": "Code executed successfully",
                    "output": stdout,
                    "stderr": stderr,
                    "return_code": process.returncode
                }
            else:
                # Analyze the error and provide helpful feedback
                feedback = self._analyze_execution_error(stderr, stdout)
                
                return {
                    "success": False,
                    "message": f"Code execution failed with return code {process.returncode}",
                    "output": stdout,
                    "stderr": stderr,
                    "return_code": process.returncode,
                    "feedback": feedback
                }
                
        except Exception as e:
            logger.error(f"Error executing code: {e}")
            logger.error(traceback.format_exc())
            return {
                "success": False,
                "message": f"Error executing code: {str(e)}",
                "output": "",
                "error": str(e)
            }
    
    def _send_websocket_notification(self, response: Dict[str, Any]) -> None:
        """
        Send a notification via WebSocket.
        
        Args:
            response: The response to send.
        """
        try:
            if websocket_server and hasattr(websocket_server, 'running') and websocket_server.running:
                message = {
                    "type": "code_execution",
                    "data": response
                }
                # Check if broadcast method exists
                if hasattr(websocket_server, 'broadcast'):
                    websocket_server.broadcast(json.dumps(message))
                    logger.debug("Sent WebSocket notification")
                else:
                    logger.debug("WebSocket server does not have broadcast method")
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")
            logger.error(traceback.format_exc()) 