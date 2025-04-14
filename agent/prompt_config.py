#!/usr/bin/env python
"""
Prompt configuration for the Reachy Code Generation Agent.

This module contains the prompt sections used by the code generation agent.
Separating these from the main code makes it easier to maintain and update the prompts.
"""

import os
import sys
import json
import logging
import importlib.util
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("prompt_config")

# Core role definition
CORE_ROLE = """
You are an AI assistant that generates Python code for controlling a Reachy 2 robot. Approach your task with a spatial understanding as if you were the robot itself - consider the physical constraints, joint limits, and reachable workspace from the robot's perspective.

When planning movements, visualize the robot's body - its two arms with 7 joints each, its head, and its sensors. Think about how each joint rotation affects the position and orientation of the end effectors (hands), and ensure all movements stay within safe, reachable areas.
"""

# Define constants
OFFICIAL_API_MODULES_BASE = """
Official Reachy SDK Modules:
- reachy2_sdk
- reachy2_sdk.parts
- reachy2_sdk.utils
- reachy2_sdk.config
- reachy2_sdk.media
- reachy2_sdk.orbita
- reachy2_sdk.sensors
"""

# Check if pollen_vision is installed and include it in the modules list if it is
if importlib.util.find_spec("pollen_vision") is not None:
    OFFICIAL_API_MODULES = OFFICIAL_API_MODULES_BASE + "- pollen_vision\n"
else:
    OFFICIAL_API_MODULES = OFFICIAL_API_MODULES_BASE

# Simplified critical warnings section - removed detailed validation instructions
CRITICAL_WARNINGS_SIMPLIFIED = """
CRITICAL GUIDANCE FOR CODE GENERATION:
- Connect to the robot using ReachySDK(host="...")
- Always turn on with reachy.turn_on() before movement
- Always turn off with reachy.turn_off_smoothly() (NOT turn_off())
- Always disconnect with reachy.disconnect()
- Properties are accessed WITHOUT parentheses (e.g., reachy.r_arm NOT reachy.r_arm())
- Gripper access must be through arm property (e.g., reachy.r_arm.gripper.open())
- For arm goto(), provide EXACTLY 7 joint values
- Include time.sleep() after movement commands
- Use try/finally blocks for proper cleanup
- Handle "Target was not reachable" errors when using inverse kinematics
- **IMPORTANT:** You MUST adhere strictly to the provided 'API SUMMARY' section below. Do NOT use any functions, classes, or parameters not explicitly listed in the summary.
"""

# Simplified code structure section
CODE_STRUCTURE_SIMPLIFIED = """
REQUIRED CODE STRUCTURE:

1. INITIALIZATION PHASE:
   - Import ReachySDK from reachy2_sdk
   - Import time module for sleep calls
   - Connect to the robot: reachy = ReachySDK(host="localhost")
   - Turn on the robot: reachy.turn_on()
   - Reset posture: reachy.goto_posture('default')

2. MAIN CODE PHASE:
   - Implement the requested functionality using the Reachy SDK
   - Add time.sleep() after movement commands
   - Use try/except blocks for error handling

3. CLEANUP PHASE:
   - Use a finally block for cleanup operations
   - Call reachy.turn_off_smoothly()
   - Call reachy.disconnect()
"""

# Basic example template
BASIC_EXAMPLE = """
EXAMPLE CODE TEMPLATE:
```python
from reachy2_sdk import ReachySDK
import time

# Connect to the robot
reachy = ReachySDK(host="localhost")

try:
    # INITIALIZATION
    reachy.turn_on()
    reachy.goto_posture('default')
    time.sleep(2)  # Wait for posture to complete
    
    # MAIN CODE
    # Using joint angle control (RECOMMENDED for reliability)
    # This moves the right arm to a forward extended position
    reachy.r_arm.goto([0, 0, 0, -90, 0, 0, 0], duration=1.0)
    time.sleep(1.5)  # Wait for movement to complete
    
    # Move to a slightly different position
    reachy.r_arm.goto([0, 10, -10, -90, 0, 0, 0], duration=1.0)
    time.sleep(1.5)  # Wait for movement to complete
    
finally:
    # CLEANUP
    reachy.turn_off_smoothly()
    reachy.disconnect()
```
"""

# Example with reachability check
REACHABILITY_EXAMPLE = """
EXAMPLE WITH REACHABILITY CHECK:
```python
from reachy2_sdk import ReachySDK
import numpy as np
import time
from reachy2_sdk.utils.utils import get_pose_matrix  # Utility for creating pose matrices

# Connect to the robot
reachy = ReachySDK(host="localhost")

try:
    # INITIALIZATION
    reachy.turn_on()
    reachy.goto_posture('default')
    time.sleep(2)  # Wait for posture to complete
    
    # MAIN CODE
    # IMPORTANT: Cartesian control is less reliable than joint angle control
    # Always have a fallback strategy using joint angles
    
    # OPTION 1 (RECOMMENDED): Using the utility function to create a target pose
    # Parameters: position [x, y, z], orientation in Euler angles [roll, pitch, yaw]
    # This creates a pose with the hand facing forward (-90° rotation around Y axis)
    target_pose = get_pose_matrix([0.3, -0.2, 0.1], [0, -90, 0])
    
    # OPTION 2: Creating the matrix manually with proper orientation
    # target_pose = np.array([[0, 0, -1, 0.3],  # Proper orientation with X position
    #                         [0, 1, 0, -0.2],  # Proper orientation with Y position
    #                         [1, 0, 0, 0.1],   # Proper orientation with Z position
    #                         [0, 0, 0, 1]])    # Homogeneous coordinates
    
    # Check if the target pose is reachable before attempting to move
    try:
        # Try to calculate joint positions using inverse kinematics
        print("Attempting to calculate inverse kinematics...")
        joint_positions = reachy.r_arm.inverse_kinematics(target_pose)
        print("Target is reachable! Moving to target position...")
        
        # If we get here, the target is reachable, so we can move to it
        reachy.r_arm.goto(joint_positions, duration=1.0)
        time.sleep(1.5)  # Wait for movement to complete
        
    except ValueError as error:
        print(f"Target is not reachable: {error}")
        # IMPORTANT: Always have a fallback strategy using joint angles
        print("Using a fallback position with joint angles instead...")
        reachy.r_arm.goto([0, 10, -10, -90, 0, 0, 0], duration=1.0)
        time.sleep(1.5)  # Wait for movement to complete
    
finally:
    # CLEANUP
    reachy.turn_off_smoothly()
    reachy.disconnect()
```
"""

# Safe target pose ranges
SAFE_RANGES = """
SAFE TARGET POSE RANGES (EXTREMELY IMPORTANT):

REACHY COORDINATE SYSTEM:
- X axis: forward direction from Reachy
- Y axis: right-to-left direction
- Z axis: upward direction
- Origin: midpoint between shoulders (center of Pollen's logo)
- Units: meters (e.g., [0.3, -0.2, 0.1] is 30cm forward, 20cm right, 10cm up)

IMPORTANT NOTE: Direct Cartesian control has been found to be unreliable with the Reachy robot.
For most reliable results, use joint angle control instead of Cartesian coordinates.

JOINT ANGLE CONTROL (RECOMMENDED):
- Use reachy.r_arm.goto([j1, j2, j3, j4, j5, j6, j7], duration=1.0) for right arm
- Use reachy.l_arm.goto([j1, j2, j3, j4, j5, j6, j7], duration=1.0) for left arm

RELIABLE JOINT ANGLE CONFIGURATIONS:
- Right arm extended forward: [0, 0, 0, -90, 0, 0, 0]
- Right arm slightly to the side: [0, 10, -10, -90, 0, 0, 0]
- Right arm upward: [-45, 0, 0, -45, 0, 0, 0]
- Left arm extended forward: [0, 0, 0, -90, 0, 0, 0]
- Left arm slightly to the side: [0, -10, 10, -90, 0, 0, 0]
- Left arm upward: [-45, 0, 0, -45, 0, 0, 0]

IF YOU MUST USE CARTESIAN CONTROL:
1. ALWAYS use inverse_kinematics() with try/except to check reachability first
2. ALWAYS have a fallback strategy using joint angles if the target is unreachable
3. Keep movements small and incremental
4. Target pose orientation is critical:
   - Identity rotation matrix = hand facing downward
   - For hand facing forward = -90° rotation around Y axis
5. RECOMMENDED: Use the utility function get_pose_matrix() from reachy2_sdk.utils.utils:
   ```python
   from reachy2_sdk.utils.utils import get_pose_matrix
   # Parameters: position [x, y, z], orientation in Euler angles [roll, pitch, yaw]
   # For hand facing forward (common orientation):
   target_pose = get_pose_matrix([0.3, -0.2, 0.1], [0, -90, 0])
   ```

6. If creating matrices manually, use the proper rotation matrix for hand-forward orientation:
   ```python
   # Proper matrix for hand facing forward:
   target_pose = np.array([[0, 0, -1, x],  # Note the rotation part
                           [0, 1, 0, y],    # is NOT the identity matrix
                           [1, 0, 0, z],
                           [0, 0, 0, 1]])
   ```

REACHABILITY CHECKING:
1. The inverse_kinematics() function will raise an exception if a pose is unreachable
2. Always implement try/except blocks to handle unreachable targets gracefully
3. A target may be unreachable because:
   - It's too far away from the robot
   - It would require joints to exceed their physical limits
   - It would require impossible orientations

WORKSPACE GUIDELINES:
1. Keep targets CLOSE to the robot's body (typically within 60cm)
2. For complex movements, use joint angles directly instead of Cartesian coordinates
3. ALWAYS include error handling for unreachable targets
4. When creating paths or shapes, test each point individually for reachability
5. Note that Reachy lacks self-collision avoidance beyond joint limits

COMMON MISTAKES TO AVOID:
1. Using the identity rotation matrix for Cartesian control (this will likely fail)
2. Assuming a target pose is reachable without checking
3. Creating paths where ANY point is outside the reachable workspace
4. Not having a fallback strategy using joint angles
5. Using Cartesian control without proper error handling

"""

# Optimization instructions for handling evaluator feedback
OPTIMIZATION_INSTRUCTIONS = """
CODE OPTIMIZATION INSTRUCTIONS:

This prompt may be used both for initial code generation AND for optimizing previously generated code.
When you receive code optimization requests containing evaluation feedback, you should:

1. Carefully analyze all reported errors, warnings, and suggestions
2. Fix ALL critical errors before addressing other issues
3. Implement suggested improvements to enhance safety, reliability, and code quality
4. Maintain the same functionality while making the code more robust
5. Ensure proper error handling, especially for inverse kinematics and unreachable targets
6. Add appropriate comments to explain complex logic or safety measures
7. Follow ALL coding standards and safety practices for the Reachy 2 robot

Common optimization patterns:
- Add proper try/finally structure if missing
- Fix property access (e.g., change reachy.r_arm() to reachy.r_arm)
- Ensure arm.goto() always has exactly 7 joint values
- Add time.sleep() after movement commands
- Add fallback strategies for inverse kinematics
- Verify that cleanup operations happen in a finally block
- Remove potentially unsafe functions like os.system()
- Validate position values to ensure they are within safe ranges

When optimizing, ALWAYS maintain the core functionality requested by the user.
"""

# Response format instructions
RESPONSE_FORMAT = """
Format your response with:
1. A brief explanation of what the code does
2. The complete Python code in a code block
3. An explanation of how the code works and any important considerations
"""

# Functions to load API documentation and generate API summary
def load_api_documentation():
    """
    Load the API documentation from the JSON file.
    
    Returns:
        list: The API documentation as a list.
    """
    try:
        doc_path = os.path.join(os.path.dirname(__file__), "docs", "api_documentation.json")
        with open(doc_path, "r") as f:
            api_docs = json.load(f)
            
            # Handle format difference - ensure we return a list
            # This ensures compatibility between different versions of API docs
            # Some versions return a dictionary while others return a list
            if isinstance(api_docs, dict):
                logger.info("API documentation loaded in dictionary format, converting to list")
                # If it's a dictionary, we need to transform it to a list format
                # compatible with the existing code
                return list(api_docs.values())
            elif isinstance(api_docs, list):
                logger.info("API documentation loaded in list format")
                return api_docs
            else:
                logger.error(f"Unknown API documentation format: {type(api_docs)}")
                return []
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

def get_official_api_modules():
    """
    Get the list of official API modules, including pollen_vision if installed.
    
    Returns:
        List[str]: List of official API module prefixes.
    """
    # Define the base official API modules (these are the ones from the Reachy SDK)
    official_api_modules = [
        "reachy2_sdk.reachy_sdk",
        "reachy2_sdk.parts",
        "reachy2_sdk.utils",
        "reachy2_sdk.config",
        "reachy2_sdk.media",
        "reachy2_sdk.orbita",
        "reachy2_sdk.sensors",
    ]
    
    # Check if pollen_vision is installed and add it to official modules if it is
    try:
        if importlib.util.find_spec("pollen_vision") is not None:
            logger.info("pollen_vision module found, adding to official API modules")
            official_api_modules.append("pollen_vision")
        else:
            logger.info("pollen_vision module not found, skipping")
    except ImportError:
        logger.info("pollen_vision module not found, skipping")
    
    return official_api_modules

def generate_api_summary(api_docs=None):
    """
    Generate a concise summary of the API documentation with essential parameter details.
    
    Args:
        api_docs: The API documentation (loads it automatically if not provided).
        
    Returns:
        str: A summary of the API documentation.
    """
    # Load API docs if not provided
    if api_docs is None:
        api_docs = load_api_documentation()
    
    if not api_docs:
        return "No API documentation available."
    
    # Get official API modules
    official_api_modules = get_official_api_modules()
    
    # Extract classes and their methods from the documentation
    classes = {}
    official_classes = set()
    
    # Process API docs (which should be a list)
    for item in api_docs:
        if isinstance(item, dict) and item.get("type") == "class":
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
    
    # Format the simplified summary
    summary = []
    
    # Add a concise header with common classes
    summary.append("# REACHY SDK API REFERENCE")
    summary.append("Available classes: " + ", ".join(sorted(official_classes)))
    summary.append("")
    
    # Process priority classes first (most commonly used)
    priority_classes = ["ReachySDK", "Arm", "Head", "MobileBase"]
    processed_classes = set()
    
    for class_name in priority_classes:
        if class_name in classes:
            class_info = classes[class_name]
            summary.append(f"## {class_name}")
            summary.append(f"Module: {class_info['module']}")
            
            # Add a brief one-liner description
            if class_info["docstring"]:
                first_line = class_info["docstring"].split("\n")[0]
                summary.append(first_line)
            summary.append("")
            
            # Identify properties vs methods based on naming conventions and signature patterns
            properties = []
            methods = []
            
            for method in class_info["methods"]:
                method_name = method.get("name")
                
                # Skip private methods (but allow special methods like __init__)
                if method_name.startswith("_") and not method_name.startswith("__"):
                    continue
                
                # Check if this is a property
                signature = method.get("signature", "")
                is_property = (
                    # Check for property decorator if available
                    "property" in method.get("decorators", []) or
                    # Common pattern for properties: only self parameter
                    ("(self)" in signature or "(self) ->" in signature) or
                    # Known properties for common classes
                    (class_name == "ReachySDK" and method_name in [
                        "r_arm", "l_arm", "head", "mobile_base", "cameras", "joints", "tripod"
                    ]) or
                    (class_name == "Arm" and method_name in ["gripper"]) or
                    (class_name == "Head" and method_name in ["cameras"])
                )
                
                if is_property:
                    properties.append(method)
                else:
                    methods.append(method)
            
            # Add properties in compact format (without parentheses)
            if properties:
                property_names = []
                for prop in properties:
                    property_names.append(prop.get("name"))
                summary.append("Properties: " + ", ".join(property_names))
                summary.append("")
            
            # Add methods in compact format (with parentheses for clarity)
            if methods:
                # First add important methods with their signatures
                important_methods = []
                other_methods = []
                
                for method in methods:
                    method_name = method.get("name")
                    
                    # Important methods get full signatures
                    if method_name in ["__init__", "goto", "inverse_kinematics"]:
                        signature = method.get("signature", "")
                        if " -> " in signature:
                            signature = signature.split(" -> ")[0] + ")"
                        important_methods.append(f"{method_name}{signature}")
                        
                        # Add parameter details only for these critical methods
                        docstring = method.get("docstring", "")
                        param_details = extract_parameter_details(signature, docstring)
                        param_details = add_special_constraints(class_name, method_name, param_details)
                        
                        # Add only critical parameters (target in goto, etc.)
                        critical_params = []
                        for param_name, param_info in param_details.items():
                            constraints = param_info.get("constraints", [])
                            if constraints:
                                param_type = param_info.get("type", "")
                                if len(param_type) > 20:  # Simplify complex types
                                    if "List" in param_type: param_type = "List"
                                    elif "Optional" in param_type: param_type = "Optional"
                                    elif "Dict" in param_type: param_type = "Dict"
                                
                                critical_params.append(f"  - {param_name} ({param_type}): {constraints[0]}")
                        
                        if critical_params:
                            important_methods.extend(critical_params)
                    else:
                        # Other methods just get names with parentheses
                        other_methods.append(f"{method_name}()")
                
                # Add important methods first, then other methods
                if important_methods:
                    summary.append("Important Methods:")
                    summary.extend(important_methods)
                    summary.append("")
                
                if other_methods:
                    summary.append("Other Methods: " + ", ".join(other_methods))
                    summary.append("")
            
            processed_classes.add(class_name)
        
    # Process remaining classes very briefly
    if len(classes) > len(processed_classes):
        summary.append("## Other Classes")
        for class_name in sorted(set(classes.keys()) - processed_classes):
            class_info = classes[class_name]
            methods = [m.get("name") for m in class_info["methods"] 
                      if not m.get("name").startswith("_") or m.get("name").startswith("__")]
            if methods:
                summary.append(f"- {class_name}: {', '.join(methods[:5])}" + 
                              ("..." if len(methods) > 5 else ""))
        
        summary.append("")
    
    return "\n".join(summary)

# Pre-generate API summary when the module is loaded
API_SUMMARY = generate_api_summary()
logger.info("Pre-generated API summary")

# Pre-load kinematics guide
KINEMATICS_GUIDE = load_kinematics_guide()
logger.info("Pre-loaded kinematics guide")

# Function to get all prompt sections
def get_prompt_sections():
    """
    Get all prompt sections as a dictionary.
    
    Returns:
        dict: A dictionary of prompt section names to their content.
    """
    return {
        "core_role": CORE_ROLE,
        "official_modules": OFFICIAL_API_MODULES,
        "critical_warnings": CRITICAL_WARNINGS_SIMPLIFIED,  # Using simplified warnings now
        "code_structure": CODE_STRUCTURE_SIMPLIFIED,  # Using simplified structure now
        "basic_example": BASIC_EXAMPLE,
        "optimization_instructions": OPTIMIZATION_INSTRUCTIONS,  # Add optimization instructions
        "response_format": RESPONSE_FORMAT,
        # Add pre-generated content
        "api_summary": API_SUMMARY,
        "kinematics_guide": KINEMATICS_GUIDE
    }

# Function to get the default prompt sections order
def get_default_prompt_order():
    """
    Get the default order of prompt sections.
    
    Returns:
        list: A list of section names in the default order.
    """
    return [
        "core_role",
        "official_modules",
        "critical_warnings",
        "code_structure",
        "basic_example",
        "optimization_instructions",
        "kinematics_guide",
        "api_summary",
        "response_format"
    ] 