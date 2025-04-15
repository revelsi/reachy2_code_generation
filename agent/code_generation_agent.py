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

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code_generation_agent")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import OPENAI_API_KEY, MODEL, EVALUATOR_MODEL, AVAILABLE_MODELS, get_model_config

# Import the unified prompt builder
from agent.prompt_config import build_generator_prompt

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


class ReachyCodeGenerationAgent:
    """
    An agent that generates Python code for interacting with the Reachy 2 robot.
    
    This agent uses the OpenAI API to generate Python code based on natural language requests,
    and provides validation and explanation of the generated code.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = MODEL,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        model_config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the Reachy code generation agent.

        Args:
            api_key: The OpenAI API key.
            model: The OpenAI model to use.
            temperature: The temperature for the model (0.0 to 1.0).
            max_tokens: The maximum number of tokens to generate.
            top_p: The top_p value for the model (0.0 to 1.0).
            frequency_penalty: The frequency penalty for the model (-2.0 to 2.0).
            presence_penalty: The presence penalty for the model (-2.0 to 2.0).
            model_config: Optional model configuration dictionary.
        """
        # Set up logger
        self.logger = logger
        
        # Get OpenAI API key from environment if not provided
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY", OPENAI_API_KEY)
            if not api_key:
                raise ValueError("No OpenAI API key provided")
        
        # Store API key
        self.api_key = api_key
        
        # Set up model configuration
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        
        # Override with model_config if provided
        if model_config:
            self.model = model_config.get("model", self.model)
            self.temperature = model_config.get("temperature", self.temperature)
            self.max_tokens = model_config.get("max_tokens", self.max_tokens)
            self.top_p = model_config.get("top_p", self.top_p)
            self.frequency_penalty = model_config.get("frequency_penalty", self.frequency_penalty)
            self.presence_penalty = model_config.get("presence_penalty", self.presence_penalty)
        
        # Build system prompt
        self.system_prompt = self._build_system_prompt()
        
        # Extract official API elements
        self._extract_official_api_elements()
        
        # Create a code generation interface for generating code
        from agent.code_generation_interface import CodeGenerationInterface
        self.interface = CodeGenerationInterface(
            api_key=api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty
        )
        
        # Initialize conversation history
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
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
            Dict[str, Any]: The response from the agent with code, message, and raw_response.
        """
        try:
            system_prompt = self._build_system_prompt()
            
            # Generate code using the interface
            response = self.interface.generate_code(
                system_prompt=system_prompt,
                user_prompt=message,
            )
            
            # Ensure response is properly formatted
            if not isinstance(response, dict):
                logger.error(f"Interface returned non-dictionary response: {type(response)}")
                return {
                    "code": "",
                    "message": "Error: Failed to generate code due to an internal error.",
                    "raw_response": str(response)
                }
                
            # Ensure all required fields are present
            if "code" not in response:
                code, explanation = self._extract_code_and_explanation(response.get("raw_response", ""))
                response["code"] = code
                response["message"] = explanation
            
            return response
            
        except Exception as e:
            logger.error(f"Error in process_message: {e}")
            logger.error(traceback.format_exc())
            return {
                "code": "",
                "message": f"Error generating code: {str(e)}",
                "raw_response": ""
            }
    
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
        """Extract the official API modules and classes."""
        # Use the prompt_config functions to get API information
        from agent.prompt_config import load_api_documentation, get_official_api_modules
        
        # Initialize 
        self.official_modules = []
        self.official_classes = set()
        
        # Load API documentation through prompt_config
        api_docs = load_api_documentation()  # This now returns a list format
        
        if api_docs:
            # Get official modules
            self.official_modules = get_official_api_modules()
            
            # Extract classes from the documentation
            # Process API docs as a list of items
            for item in api_docs:
                if isinstance(item, dict) and item.get("type") == "class":
                    class_name = item.get("name")
                    module_name = item.get("module", "")
                    
                    # Only include classes from official modules
                    if module_name and any(module_name.startswith(prefix) for prefix in self.official_modules):
                        if class_name:
                            self.official_classes.add(class_name)
        
        self.logger.debug(f"Extracted {len(self.official_modules)} official modules and {len(self.official_classes)} official classes")
    
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
        
        # First check for connection issues - look in both stderr and output
        if "is not connected" in stderr or "is not connected" in output or "not reachy.is_connected" in output:
            feedback += "CONNECTION ERROR: Reachy robot is not connected.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Always verify connection with 'if not reachy.is_connected:' before proceeding\n"
            feedback += "2. Make sure the Reachy robot or simulator is running\n"
            feedback += "3. Check that the host parameter is correct in ReachySDK() initialization\n"
            feedback += "4. Ensure the gRPC port (default: 50051) is not blocked\n"
            feedback += "5. Verify the robot's network connectivity if using a physical robot\n"
            return feedback
        
        # Check for NoneType errors on robot parts (common indication of connection issues)
        if "'NoneType' object has no attribute" in stderr:
            import re
            none_attr_match = re.search(r"'NoneType' object has no attribute '(.+?)'", stderr)
            if none_attr_match:
                attr_name = none_attr_match.group(1)
                feedback += "CONNECTION ERROR: Robot part is not properly connected or initialized.\n\n"
                feedback += f"The '{attr_name}' method was called on a None object, which typically happens when:\n"
                feedback += "1. The robot is not connected, despite reachy.is_connected returning True\n"
                feedback += "2. The robot part (arm, head, etc.) is not available or not fully initialized\n"
                feedback += "3. The gRPC connection is partially established but not fully functional\n\n"
                feedback += "Suggestions:\n"
                feedback += "1. Make sure the robot or simulator is fully running before connecting\n"
                feedback += "2. Check that all robot parts are properly detected in the simulator or on the physical robot\n"
                feedback += "3. Try disconnecting and reconnecting to the robot\n"
                feedback += "4. Verify the host parameter is correct and the robot is reachable\n"
                return feedback
        
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
        
        # Check for API errors
        elif "AttributeError: " in stderr:
            import re
            attr_match = re.search(r"AttributeError: '(.+?)' object has no attribute '(.+?)'", stderr)
            if attr_match:
                obj_type, attr_name = attr_match.groups()
                feedback += f"API USAGE ERROR: The '{obj_type}' object does not have an attribute named '{attr_name}'.\n\n"
                feedback += "Suggestions:\n"
                feedback += f"1. Check the spelling of '{attr_name}'\n"
                feedback += f"2. Verify that '{attr_name}' is a valid property or method of '{obj_type}'\n"
                feedback += "3. Refer to the Reachy 2 SDK documentation for the correct API\n"
            else:
                feedback += "API USAGE ERROR: Incorrect attribute access.\n\n"
                feedback += "Suggestions:\n"
                feedback += "1. Check the API documentation for correct property and method names\n"
                feedback += "2. Verify that you're accessing properties and methods on the correct objects\n"
        
        # Check for gripper errors
        elif "gripper" in stderr.lower() and ("error" in stderr.lower() or "exception" in stderr.lower()):
            feedback += "GRIPPER ERROR: Issue with gripper control.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Access the gripper through the arm: reachy.r_arm.gripper\n"
            feedback += "2. Use the correct gripper methods: .open() or .close() or .move()\n"
            feedback += "3. Check if the gripper is properly attached and functioning\n"
        
        # Check for connection errors
        elif "connection" in stderr.lower() and ("error" in stderr.lower() or "exception" in stderr.lower()):
            feedback += "CONNECTION ERROR: Issue connecting to the Reachy robot.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Verify that the Reachy robot or simulation is running\n"
            feedback += "2. Check the host IP or hostname is correct\n"
            feedback += "3. Verify that the gRPC service is running and accessible\n"
        
        # Generic Python errors
        elif "ImportError: " in stderr or "ModuleNotFoundError: " in stderr:
            feedback += "IMPORT ERROR: Missing Python module.\n\n"
            feedback += "Suggestions:\n"
            feedback += "1. Ensure all required packages are installed\n"
            feedback += "2. Check for typos in import statements\n"
            feedback += "3. Verify that you're using the correct import path\n"
        
        # Default generic error feedback
        else:
            feedback += "EXECUTION ERROR: The code encountered an error during execution.\n\n"
            feedback += "Error details from the logs:\n"
            
            # Extract the most relevant parts of the error
            error_lines = []
            for line in stderr.split('\n'):
                if "Error:" in line or "Exception:" in line:
                    error_lines.append(line)
            
            # If no specific error lines were found, include the last few lines
            if not error_lines and stderr:
                error_lines = stderr.split('\n')[-3:]
            
            # Add the error lines to the feedback
            for line in error_lines:
                feedback += f"- {line.strip()}\n"
            
            feedback += "\nSuggestions:\n"
            feedback += "1. Check for logical errors in your code\n"
            feedback += "2. Verify that you're using the Reachy 2 SDK correctly\n"
            feedback += "3. Add more explicit error handling to identify the issue\n"
        
        return feedback

    def execute_code(self, code: str, confirm: bool = True, force: bool = False) -> Dict[str, Any]:
        """
        Execute the generated code.
        
        Args:
            code: The code to execute.
            confirm: Whether to require confirmation before execution.
            force: Whether to force execution even if validation fails.
            
        Returns:
            Dict[str, Any]: The execution result.
        """
        if not code or not code.strip():
            return {
                "success": False,
                "message": "No code provided for execution",
                "output": ""
            }
        
        # INTERNAL VALIDATION PHASE - Results not shown in the execution feedback section
        validation_passed = True
        validation_messages = []
        
        # Validate the code using the CodeEvaluator if available
        try:
            from agent.code_evaluator import CodeEvaluator
            evaluator = CodeEvaluator(api_key=self.api_key, model=EVALUATOR_MODEL)
            validation_result = evaluator.evaluate_code(code, "Validate code before execution")
            valid = validation_result.get("valid", False)
            warnings = validation_result.get("warnings", [])
            errors = validation_result.get("errors", [])
            
            # Record validation result for internal use only
            validation_passed = valid
            validation_messages = errors + warnings
            
        except Exception as e:
            self.logger.warning(f"Could not use CodeEvaluator for validation: {e}")
            # Simple basic check if evaluator is not available
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError as e:
                validation_passed = False
                validation_messages = [f"Syntax error: {str(e)}"]
        
        # Check if the code is valid (but don't prevent execution if force=True)
        if not validation_passed and not force:
            # For internal confirmation logic only, not for UI display
            confirm = True
        
        # Check for internal critical warnings
        has_critical_warnings = any("CRITICAL" in w for w in validation_messages)
        if has_critical_warnings and not force:
            # For internal confirmation logic only
            confirm = True
        
        # If confirmation is required, return validation for UI to handle
        # This keeps validation info separate from execution feedback
        if confirm:
            return {
                "requires_confirmation": True,
                "code": code,
                "validation": {
                    "valid": validation_passed,
                    "errors": [m for m in validation_messages if "CRITICAL" in m or m in errors],
                    "warnings": [m for m in validation_messages if "CRITICAL" not in m and m not in errors]
                },
                "message": "Code is ready for execution. Please confirm to proceed.",
                "feedback": "Waiting for execution confirmation. Click 'Execute Code' to proceed."
            }
        
        # EXECUTION PHASE - Results shown in the execution feedback section
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
            
            # Check if the execution was successful - THIS IS WHAT SHOWS IN EXECUTION FEEDBACK
            if process.returncode == 0:
                # Even if the return code is 0, check for specific error messages in the output
                if "Target was not reachable" in stdout:
                    # Analyze the error and provide helpful feedback
                    execution_feedback = self._analyze_execution_error(stderr, stdout)
                    
                    return {
                        "success": False,
                        "message": "Code execution failed: Target was not reachable",
                        "output": stdout,
                        "stderr": stderr,
                        "return_code": process.returncode,
                        "feedback": execution_feedback  # This is only about execution results
                    }
                else:
                    return {
                        "success": True,
                        "message": "Code executed successfully",
                        "output": stdout,
                        "stderr": stderr,
                        "return_code": process.returncode,
                        "feedback": "Code executed successfully." + ("\n\nOutput:\n" + stdout if stdout.strip() else " No output was produced.")
                    }
            else:
                # Analyze the error and provide helpful feedback
                execution_feedback = self._analyze_execution_error(stderr, stdout)
                
                return {
                    "success": False,
                    "message": f"Code execution failed with return code {process.returncode}",
                    "output": stdout,
                    "stderr": stderr,
                    "return_code": process.returncode,
                    "feedback": execution_feedback  # This is only about execution results
                }
                
        except Exception as e:
            self.logger.error(f"Error executing code: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "success": False,
                "message": f"Error executing code: {str(e)}",
                "output": "",
                "error": str(e),
                "feedback": f"Error executing code: {str(e)}\n\nThis may be due to:\n- Missing dependencies\n- Invalid syntax\n- Permission issues\n- Robot connectivity problems"
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
        """Build the system prompt for code generation.
        
        Returns:
            str: The system prompt for code generation.
        """
        try:
            # Use the unified prompt builder
            system_prompt = build_generator_prompt()
            return system_prompt
        except Exception as e:
            self.logger.error(f"Error building system prompt: {e}")
            self.logger.error(traceback.format_exc())
            # Return a basic fallback prompt if the builder fails
            return """You are an AI assistant that generates Python code for controlling a Reachy 2 robot."""

    def generate_code(self, user_request: str) -> Dict[str, Any]:
        """Generate code using the OpenAI API with a simple direct approach.
        
        Args:
            user_request: The user request to generate code for.
            
        Returns:
            Dict with generated code and metadata.
        """
        self.logger.info(f"Generating code for request: {user_request[:100]}...")
        
        try:
            # Build system prompt - use the comprehensive prompt instead of simplified version
            system_prompt = self._build_system_prompt()

            # Simple OpenAI API call
            client = OpenAI(api_key=self.api_key)
            
            # GPT models use standard parameters
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_request}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "frequency_penalty": self.frequency_penalty,
                "presence_penalty": self.presence_penalty
            }
            
            # Make the API call
            response = client.chat.completions.create(**params)
            
            # Extract content
            content = response.choices[0].message.content
            
            # Extract code from content
            code = self._extract_code(content)
            
            return {
                "code": code,
                "raw_response": content,
                "model": self.model,
                "success": bool(code)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "code": "",
                "error": str(e),
                "success": False,
                "raw_response": ""
            }
    
    def _extract_code(self, content: str) -> str:
        """Extract code from the response content.
        
        Args:
            content: Raw response content.
            
        Returns:
            str: Extracted code.
        """
        # First check for Python code blocks
        if "```python" in content:
            parts = content.split("```python")
            if len(parts) > 1:
                code_parts = parts[1].split("```", 1)
                if code_parts:
                    return code_parts[0].strip()
        
        # Otherwise check for any code blocks
        if "```" in content:
            parts = content.split("```")
            if len(parts) > 1:
                return parts[1].strip()
        
        # If no code blocks found, return the whole content
        return content.strip() 