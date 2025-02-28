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
from typing import Dict, List, Any, Optional, TypedDict
from openai import OpenAI
import httpx

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


def generate_api_summary(api_docs):
    """
    Generate a summary of the API documentation.
    
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
        "reachy2_sdk.sensors"
    ]
    
    # Extract classes and their methods
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
                    docstring = method.get("docstring", "").split("\n")[0] if method.get("docstring") else ""  # Get first line of docstring
                    
                    if method_name and not method_name.startswith("_"):  # Skip private methods
                        methods.append(f"- {method_name}{signature}: {docstring}")
                
                if methods:
                    classes[class_name] = methods
    
    # Format the summary
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
    
    # Add class methods
    summary.append("# Class Methods")
    for class_name, methods in classes.items():
        summary.append(f"## {class_name}")
        summary.append("\n".join(methods))
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
        model: str = "gpt-4-turbo", 
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
        
        CRITICAL WARNINGS:
        - NEVER use 'get_reachy()' or any functions from 'connection_manager.py'
        - Carefully read the API documentation and make sure you follow the arguments and parameters guidelines.
        - ALWAYS use properties correctly (e.g., reachy.r_arm NOT reachy.r_arm())
        - For arm goto(), ALWAYS provide EXACTLY 7 joint values
        
        REQUIRED CODE STRUCTURE:
        
        1. INITIALIZATION PHASE:
           - Import ReachySDK from reachy2_sdk.reachy_sdk
           - Connect to the robot: reachy = ReachySDK(host="localhost")
           - ALWAYS call reachy.turn_on() before any movement
        
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
        from reachy2_sdk.reachy_sdk import ReachySDK
        
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
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message and generate Python code.
        
        Args:
            message: The user message.
            
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
            
            # Add assistant response to conversation history
            self.messages.append({"role": "assistant", "content": code_response})
            
            # Prepare response
            response = {
                "message": explanation,
                "code": code,
                "validation": validation_result,
                "raw_response": code_response
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
            "reachy2_sdk.sensors"
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
        if "from reachy2_sdk.reachy_sdk import ReachySDK" not in code:
            warnings.append("Missing import for ReachySDK from reachy2_sdk.reachy_sdk")
        
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
        
        # Check for imports that are not in the official modules
        import_lines = [line.strip() for line in code.split('\n') if line.strip().startswith(('import ', 'from '))]
        for line in import_lines:
            # Skip standard library imports
            if any(line.startswith(f"import {mod}") or line.startswith(f"from {mod} import") 
                  for mod in ['os', 'sys', 'time', 'math', 'random', 'json', 'datetime']):
                continue
                
            # Check if the import is from an official module
            is_official = False
            for module in self.official_modules:
                if line.startswith(f"import {module}") or line.startswith(f"from {module} import"):
                    is_official = True
                    break
            
            if not is_official and not line.startswith("from reachy2_sdk.reachy_sdk import ReachySDK"):
                errors.append(f"Unofficial import detected: {line}. Only use modules from the official Reachy 2 SDK.")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _send_websocket_notification(self, data: Dict[str, Any]) -> None:
        """
        Send a notification via WebSocket.
        
        Args:
            data: The data to send.
        """
        try:
            if websocket_server and hasattr(websocket_server, 'running') and websocket_server.running:
                message = {
                    "type": "code_generation",
                    "data": data
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