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
from typing import Dict, List, Any, Optional, TypedDict, Tuple, Union
from openai import OpenAI
import httpx
import re

from .code_generation_interface import CodeGenerationInterface
from .prompt_config import get_prompt_sections, get_default_prompt_order

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

# Replace with a stub implementation for now
def get_websocket_server():
    """
    Stub implementation for the websocket server.
    
    Returns:
        object: A stub websocket server.
    """
    class StubWebSocketServer:
        def send_notification(self, *args, **kwargs):
            pass
    
    return StubWebSocketServer()

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


def load_kinematics_guide():
    """
    Load the kinematics guide from the markdown file.
    
    Returns:
        str: The kinematics guide content.
    """
    try:
        guide_path = os.path.join(os.path.dirname(__file__), "docs", "reachy2_kinematics_prompt.md")
        with open(guide_path, "r") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading kinematics guide: {e}")
        return "ARM KINEMATICS GUIDE NOT FOUND"


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
    Generate a concise summary of the API documentation with essential parameter details,
    focusing only on the most commonly used classes and methods.
    
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
    
    # Extract classes and their methods from the documentation
    classes = {}
    official_classes = set()
    
    # First pass: Collect all classes and their methods
    for item in api_docs:
        if item.get("type") == "class":
            class_name = item.get("name")
            module_name = item.get("module", "")
            
            # Only include classes from official modules
            if module_name and any(module_name.startswith(prefix) for prefix in official_api_modules):
                if class_name:
                    official_classes.add(class_name)
                    
                    # Store class info
                    classes[class_name] = {
                        "module": module_name,
                        "docstring": item.get("docstring", ""),
                        "methods": item.get("methods", [])
                    }
    
    # Format the enhanced summary
    summary = []
    
    # Add a concise header with common classes
    summary.append("# Common Classes and Methods")
    summary.append(", ".join(sorted(official_classes)))
    summary.append("")
    
    # Add class methods with enhanced details
    for class_name, class_info in sorted(classes.items()):
        summary.append(f"## {class_name}")
        summary.append(f"Module: {class_info['module']}")
        if class_info["docstring"]:
            summary.append(class_info["docstring"])
        summary.append("")
        
        # Process methods
        for method in class_info["methods"]:
            method_name = method.get("name")
            
            # Skip private methods (but allow special methods like __init__)
            if method_name.startswith("_") and not method_name.startswith("__"):
                continue
            
            signature = method.get("signature", "")
            docstring = method.get("docstring", "")
            
            # Extract parameter details
            param_details = extract_parameter_details(signature, docstring)
            
            # Add special constraints for known problematic functions
            param_details = add_special_constraints(class_name, method_name, param_details)
            
            # Add method name and simplified signature
            if method_name in ["__init__", "goto", "inverse_kinematics"]:
                # Show full signature for important methods
                if " -> " in signature:
                    signature = signature.split(" -> ")[0] + ")"
                summary.append(f"### {method_name}{signature}")
            else:
                # For other methods, show simplified signature
                summary.append(f"### {method_name}()")
            
            # Add first line of docstring if it exists and is meaningful
            if docstring and len(docstring) > 5:
                summary.append(docstring.split("\n")[0])
            
            # Add parameter details if they exist
            if param_details:
                has_important_params = False
                param_lines = []
                
                for param_name, param_info in param_details.items():
                    if not param_info.get("description") and not param_info.get("constraints"):
                        continue
                    
                    has_important_params = True
                    param_type = param_info.get("type", "")
                    param_desc = param_info.get("description", "")
                    
                    # Simplify parameter type display
                    if param_type and len(param_type) > 20:
                        if "List" in param_type:
                            param_type = "List"
                        elif "Optional" in param_type:
                            param_type = "Optional"
                        elif "Dict" in param_type:
                            param_type = "Dict"
                        elif "float | int" in param_type:
                            param_type = "number"
                        elif "npt.NDArray" in param_type:
                            param_type = "array"
                    
                    # Add parameter with type and description
                    param_line = f"- {param_name}"
                    if param_type:
                        param_line += f" ({param_type})"
                    if param_desc:
                        param_line += f": {param_desc}"
                    
                    param_lines.append(param_line)
                    
                    # Add constraints
                    constraints = param_info.get("constraints", [])
                    if constraints:
                        for constraint in constraints:
                            param_lines.append(f"  * {constraint}")
                    
                    # Add units
                    if "units" in param_info:
                        param_lines.append(f"  * Units: {param_info['units']}")
                
                if has_important_params:
                    summary.append("Parameters:")
                    summary.extend(param_lines)
            
            # Add special notes for Arm class about grippers
            if class_name == "Arm":
                summary.append("\nGripper Control:")
                summary.append("- Access the gripper through the arm.gripper property")
                summary.append("- Available methods:")
                summary.append("  * open(): Open the gripper fully")
                summary.append("  * close(): Close the gripper fully")
                summary.append("  * set_opening(value): Set gripper opening (0.0 to 1.0)")
                summary.append("\nExample:")
                summary.append("```python")
                summary.append("# Right arm gripper")
                summary.append("reachy.r_arm.gripper.open()")
                summary.append("reachy.r_arm.gripper.set_opening(0.5)  # Half open")
                summary.append("")
                summary.append("# Left arm gripper")
                summary.append("reachy.l_arm.gripper.close()")
                summary.append("```")
            
            summary.append("")
        
        summary.append("")
    
    # Add a note about additional classes
    summary.append("# Note")
    summary.append("This is a focused summary of the most commonly used classes and methods.")
    summary.append("For details on other classes and methods, please refer to the full API documentation.")
    
    return "\n".join(summary)


class ReachyCodeGenerationAgent:
    """
    An agent that generates Python code for interacting with the Reachy 2 robot.
    
    This agent uses the OpenAI API to generate Python code based on natural language requests,
    and provides validation and explanation of the generated code.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        kinematics_guide_path: str = "agent/docs/reachy2_kinematics_prompt.md",
    ):
        """Initialize the code generation agent.

        Args:
            api_key: The OpenAI API key.
            model: The OpenAI model to use.
            temperature: The temperature for the model (0.0 to 1.0).
            max_tokens: The maximum number of tokens to generate.
            kinematics_guide_path: Path to the kinematics guide.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kinematics_guide_path = kinematics_guide_path
        
        # Initialize logger
        self.logger = logging.getLogger("code_generation_agent")
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Initialize API documentation and official elements
        self.api_docs = load_api_documentation()
        self.official_modules = set()
        self.official_classes = set()
        
        # Initialize code generation interface
        self.interface = CodeGenerationInterface(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Extract official API elements
        self._extract_official_api_elements()
        
        self.logger.debug(f"Initialized code generation agent with model: {model}")
    
    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ]
        logger.debug("Reset conversation history")
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a message from the user.

        Args:
            message: The message from the user.

        Returns:
            Dict[str, Any]: The response from the agent.
        """
        system_prompt = self._build_system_prompt()
        
        # Generate code using the interface
        response = self.interface.generate_code(
            system_prompt=system_prompt,
            user_prompt=message,
        )
        
        return response
    
    def _generate_code(self) -> str:
        """
        Generate Python code using the OpenAI API.
        
        Returns:
            str: The generated code response.
        """
        try:
            # Call the OpenAI API
            response = self.interface.generate_code(
                system_prompt=self.system_prompt,
                user_prompt=self.messages[-1]["content"]
            )
            
            # Extract and return the response content
            return response
            
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
        # Initialize sets if they don't exist
        if not hasattr(self, 'official_modules'):
            self.official_modules = set()
        if not hasattr(self, 'official_classes'):
            self.official_classes = set()
            
        # Check if API docs are available
        if not hasattr(self, 'api_docs') or not self.api_docs:
            self.logger.warning("No API documentation available for extracting official elements")
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
        
        self.logger.debug(f"Extracted {len(self.official_modules)} official modules and {len(self.official_classes)} official classes")
    
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
            "gripper()", "r_gripper", "l_gripper",  # Updated to catch incorrect gripper access
            ".gripper()"  # Added to catch cases where gripper is called as a method
        ]
        for pattern in property_patterns:
            if pattern in code:
                if pattern in ["r_gripper", "l_gripper"]:
                    errors.append(f"Incorrect gripper access: Use 'arm.gripper' instead of '{pattern}' (e.g., reachy.r_arm.gripper)")
                elif pattern == "gripper()" or pattern == ".gripper()":
                    errors.append(f"Incorrect gripper usage: 'gripper' is a property, not a method. Use without parentheses (e.g., reachy.r_arm.gripper)")
                else:
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
            
        # Check for potential workspace issues
        workspace_warnings = self._check_workspace_issues(code)
        if workspace_warnings:
            warnings.extend(workspace_warnings)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
        
    def _check_workspace_issues(self, code: str) -> List[str]:
        """
        Check for potential workspace issues in the generated code.
        
        Args:
            code: The generated code.
            
        Returns:
            List[str]: List of warnings about potential workspace issues.
        """
        warnings = []
        
        # Define safe ranges
        safe_ranges = {
            "r_arm": {
                "x": (0.2, 0.4),  # forward from chest (meters)
                "y": (-0.3, -0.1),  # to the right of center (meters)
                "z": (-0.1, 0.3),  # vertical position (meters)
            },
            "l_arm": {
                "x": (0.2, 0.4),  # forward from chest (meters)
                "y": (0.1, 0.3),  # to the left of center (meters)
                "z": (-0.1, 0.3),  # vertical position (meters)
            }
        }
        
        # Check for potential out-of-range X values
        if "0.5" in code and ("x" in code.lower() or "position" in code.lower()):
            warnings.append("CRITICAL: Potential unreachable target - X value may be too large (> 0.4m)")
        
        # Check for potential out-of-range Y values for right arm
        if "y" in code.lower() and "-0.4" in code:
            warnings.append("CRITICAL: Potential unreachable target - Y value for right arm may be too far right (< -0.3m)")
        
        # Check for potential out-of-range Y values for left arm
        if "y" in code.lower() and "0.4" in code:
            warnings.append("CRITICAL: Potential unreachable target - Y value for left arm may be too far left (> 0.3m)")
        
        # Check for potential out-of-range Z values
        if "z" in code.lower() and ("0.4" in code or "-0.2" in code):
            warnings.append("CRITICAL: Potential unreachable target - Z value may be outside safe range (-0.1m to 0.3m)")
        
        # Check for numpy arrays that might define target positions
        if "np.array" in code and "[[" in code:
            # Look for potential transformation matrices
            if not all(limit in code for limit in ["0.2", "0.3", "0.4"]):
                warnings.append("CRITICAL: Target positions may be outside safe workspace limits. Ensure X: 0.2-0.4m, Y: ±0.1-0.3m, Z: -0.1-0.3m")
        
        # Check if the code includes reachability checks
        if "inverse_kinematics" in code and "try:" in code and "except" in code:
            # Code has proper error handling for inverse kinematics
            pass
        elif "inverse_kinematics" in code:
            warnings.append("CRITICAL: Using inverse_kinematics without proper error handling. Always use try/except to handle unreachable targets.")
        
        return warnings
    
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
        
        # Check for "Target was not reachable" message in output
        if "Target was not reachable" in output:
            feedback += "UNREACHABLE TARGET ERROR: The target pose is not reachable by the robot arm.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Try a position closer to the robot's body\n"
            feedback += "2. Use a simpler orientation (e.g., facing forward)\n"
            feedback += "3. Check that the position values are within the robot's reach (typically within 0.6 meters)\n"
            feedback += "4. Consider using joint angles directly instead of inverse kinematics or target poses\n"
        
        # Check for inverse kinematics errors
        elif "No solution found for the given target" in stderr or "No solution found for the given target" in output:
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
            self.logger.info(f"Executing code in {temp_file_path}")
            
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
                self.logger.warning(f"Failed to delete temporary file {temp_file_path}: {e}")
            
            # Check if the execution was successful
            if process.returncode == 0:
                # Even if the return code is 0, check for specific error messages in the output
                if "Target was not reachable" in stdout:
                    # Analyze the error and provide helpful feedback
                    feedback = self._analyze_execution_error(stderr, stdout)
                    
                    return {
                        "success": False,
                        "message": "Code execution failed: Target was not reachable",
                        "output": stdout,
                        "stderr": stderr,
                        "return_code": process.returncode,
                        "feedback": feedback
                    }
                else:
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
            self.logger.error(f"Error executing code: {e}")
            self.logger.error(traceback.format_exc())
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

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the code generation agent.
        
        Returns:
            str: The system prompt.
        """
        # Get prompt sections and default order
        sections = get_prompt_sections()
        section_order = get_default_prompt_order()
        
        # Load kinematics guide
        kinematics_guide = ""
        
        try:
            with open(self.kinematics_guide_path, "r") as f:
                kinematics_guide = f.read()
        except Exception as e:
            self.logger.error(f"Failed to load kinematics guide: {e}")
            kinematics_guide = "ERROR: Kinematics guide not found."
        
        # Generate API summary on-the-fly
        api_docs = load_api_documentation()
        if api_docs:
            api_summary = generate_api_summary(api_docs)
            self.logger.info("Generated API summary from documentation")
        else:
            self.logger.error("Failed to load API documentation")
            api_summary = "ERROR: API documentation not found."
        
        # Build the prompt by concatenating sections in order
        prompt_parts = []
        
        for section_name in section_order:
            if section_name in sections:
                prompt_parts.append(sections[section_name])
        
        # Insert kinematics guide and API summary at appropriate positions
        # Add them after the code structure section
        code_structure_index = section_order.index("code_structure")
        
        if code_structure_index >= 0 and code_structure_index < len(prompt_parts):
            prompt_parts.insert(code_structure_index + 1, f"KINEMATICS GUIDE:\n{kinematics_guide}")
            prompt_parts.insert(code_structure_index + 2, f"API SUMMARY:\n{api_summary}")
        
        # Join all parts with double newlines for better readability
        return "\n\n".join(prompt_parts) 