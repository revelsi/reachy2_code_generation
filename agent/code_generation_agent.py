#!/usr/bin/env python
"""
Code Generation Agent for the Reachy 2 robot.

This module provides an agent that generates Python code for interacting with the Reachy 2 robot
based on natural language requests.
"""

import os
import sys
import json
import logging
import traceback
from typing import Dict, List, Any, Optional, Literal, TypedDict, Annotated
from dotenv import load_dotenv
import time
import asyncio
from openai import OpenAI
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code_generation_agent")

# Load environment variables
load_dotenv()

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import get_model_config, OPENAI_API_KEY

# Import LangChain message types
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    BaseMessage
)

# Import WebSocket server for notifications
from api.websocket import get_websocket_server

# Configure OpenAI client with custom settings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", OPENAI_API_KEY),
    timeout=30.0,  # Increase timeout
    max_retries=2,  # Add retries
    base_url="https://api.openai.com/v1",  # Explicitly set base URL
    http_client=httpx.Client(
        transport=httpx.HTTPTransport(retries=2),
        timeout=30.0,
        verify=True  # Ensure SSL verification is enabled
    )
)

# WebSocket server for notifications
websocket_server = get_websocket_server()
websocket_clients = set()


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
        
        # Tool schemas
        self.tool_schemas = []
        
        # Conversation history
        self.messages = []
        
        # System prompt for the agent
        self.system_prompt = """
        You are an AI assistant that generates Python code for controlling a Reachy 2 robot.
        
        When a user asks you to perform an action with the robot, analyze their request and generate
        Python code that uses the Reachy 2 SDK to accomplish the task. Your code should be:
        
        1. Syntactically correct and executable
        2. Well-structured and organized
        3. Properly commented to explain key steps
        4. Error-handled with try/except blocks
        5. Safe and considerate of the robot's physical limitations
        
        Include imports, connection setup, and any necessary cleanup. Always use the connection manager
        to get a connection to the robot using `get_reachy()` from `agent.tools.connection_manager`.
        
        Format your response with:
        1. A brief explanation of what the code does
        2. The complete Python code in a code block
        3. An explanation of how the code works and any important considerations
        
        If you're unsure about a request or if it seems unsafe, explain your concerns and suggest
        alternatives.
        """
        
        # Initialize conversation with system message
        self.reset_conversation()
    
    def set_tool_schemas(self, tool_schemas: List[Dict[str, Any]]) -> None:
        """
        Set the tool schemas for the agent.
        
        Args:
            tool_schemas: List of tool schemas.
        """
        self.tool_schemas = tool_schemas
        logger.info(f"Set {len(tool_schemas)} tool schemas")
    
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
            # Prepare tool schema information
            tool_info = self._prepare_tool_info()
            
            # Add tool information to the conversation
            if tool_info:
                self.messages.append({
                    "role": "system",
                    "content": f"Available tools for the Reachy 2 robot:\n\n{tool_info}"
                })
            
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
            
            # Remove the tool information message to keep the conversation clean
            if tool_info:
                self.messages.pop()
            
            # Extract and return the response content
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Failed to generate code: {e}")
    
    def _prepare_tool_info(self) -> str:
        """
        Prepare information about available tools for the code generation.
        
        Returns:
            str: Formatted tool information.
        """
        if not self.tool_schemas:
            return ""
        
        tool_info = []
        for tool in self.tool_schemas:
            if isinstance(tool, dict) and "function" in tool:
                function = tool["function"]
                name = function.get("name", "")
                description = function.get("description", "")
                parameters = function.get("parameters", {})
                
                # Format parameters
                param_info = []
                if "properties" in parameters:
                    for param_name, param_details in parameters["properties"].items():
                        param_type = param_details.get("type", "any")
                        param_desc = param_details.get("description", "")
                        required = "required" if param_name in parameters.get("required", []) else "optional"
                        param_info.append(f"  - {param_name} ({param_type}, {required}): {param_desc}")
                
                # Add tool information
                tool_info.append(f"Tool: {name}\nDescription: {description}\nParameters:\n" + "\n".join(param_info))
        
        return "\n\n".join(tool_info)
    
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
        if "from agent.tools.connection_manager import get_reachy" not in code:
            warnings.append("Missing import for get_reachy from connection_manager")
        
        # Check for connection setup
        if "get_reachy()" not in code:
            warnings.append("Code does not use get_reachy() to establish a connection")
        
        # Check for error handling
        if "try:" not in code:
            warnings.append("No error handling (try/except) found in the code")
        
        # Check for potentially unsafe operations
        unsafe_patterns = [
            "os.system", "subprocess", "eval(", "exec(", "import shutil"
        ]
        for pattern in unsafe_patterns:
            if pattern in code:
                errors.append(f"Potentially unsafe operation detected: {pattern}")
        
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
        if websocket_server and websocket_server.is_running():
            try:
                message = {
                    "type": "code_generation",
                    "data": data
                }
                websocket_server.broadcast(json.dumps(message))
                logger.debug("Sent WebSocket notification")
            except Exception as e:
                logger.error(f"Error sending WebSocket notification: {e}")
                logger.error(traceback.format_exc()) 