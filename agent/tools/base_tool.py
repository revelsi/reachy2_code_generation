#!/usr/bin/env python
"""
Base tool class for Reachy 2 tools.

This module provides a base class for all Reachy 2 tools, with common functionality
such as connection management and error handling.
"""

from typing import Dict, Any, Optional, Callable, List, Type
import logging
import importlib.util
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("base_tool")

# Try to import Reachy SDK (may not be available)
try:
    from reachy2_sdk import ReachySDK
    REACHY_SDK_AVAILABLE = True
except ImportError:
    logger.warning("Reachy SDK not available. Running in demo/simulation mode.")
    REACHY_SDK_AVAILABLE = False

# Import our connection manager if available
try:
    from agent.tools.connection_manager import connect_to_reachy, get_reachy, is_mock
    CONNECTION_MANAGER_AVAILABLE = True
except ImportError:
    logger.warning("Connection manager not available. Using basic connection handling.")
    CONNECTION_MANAGER_AVAILABLE = False
    
    # Global connection instance as fallback
    _reachy_instance = None

# Import transparent executor if available
try:
    from agent.transparent_executor import get_executor, wrap_function
    TRANSPARENT_EXECUTOR_AVAILABLE = True
except ImportError:
    logger.warning("Transparent executor not available. Using direct execution.")
    TRANSPARENT_EXECUTOR_AVAILABLE = False


def get_reachy_connection(host: str = "localhost", use_mock: bool = False) -> Any:
    """
    Get or create a Reachy connection.
    
    Args:
        host: Hostname or IP address of the Reachy robot.
        use_mock: Whether to use a mock implementation.
        
    Returns:
        Any: Reachy instance (real or mock).
    """
    global _reachy_instance
    
    # Use connection manager if available
    if CONNECTION_MANAGER_AVAILABLE:
        return connect_to_reachy(host=host, use_mock=use_mock or not REACHY_SDK_AVAILABLE)
    
    # Fallback to basic connection
    if _reachy_instance is None:
        if use_mock or not REACHY_SDK_AVAILABLE:
            # Try to import and use mock
            try:
                from agent.tools.mock_reachy import get_mock_reachy
                _reachy_instance = get_mock_reachy(host=host)
                logger.info(f"Connected to mock Reachy at {host}")
            except ImportError:
                logger.error("Mock Reachy not available. Cannot connect.")
                raise RuntimeError("Cannot connect to Reachy (no SDK or mock available)")
        else:
            # Use real SDK
            _reachy_instance = ReachySDK(host=host)
            logger.info(f"Connected to real Reachy at {host}")
            
    return _reachy_instance


class BaseTool:
    """Base class for all Reachy 2 tools."""
    
    # Class variables for tool registration
    tools: Dict[str, Callable] = {}
    tool_schemas: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register_tool(cls, name: str, func: Callable, schema: Dict[str, Any]) -> None:
        """
        Register a tool function with its schema.
        
        Args:
            name: Name of the tool.
            func: Tool function.
            schema: Tool schema.
        """
        # Wrap function with transparent executor if available
        if TRANSPARENT_EXECUTOR_AVAILABLE:
            # Check if we have a mock version available
            mock_func = None
            
            # Create docstring-based reasoning
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                # Extract reasoning from function docstring
                doc = func.__doc__ or ""
                reasoning = doc.strip().split("\n")[0] if doc else f"Executing {name}"
                
                # Add reasoning to kwargs
                kwargs["reasoning"] = kwargs.get("reasoning", reasoning)
                
                # Call the function through executor
                return wrap_function(func, mock_func)(*args, **kwargs)
            
            # Register the wrapped function
            cls.tools[name] = wrapped_func
        else:
            # Register the original function
            cls.tools[name] = func
            
        # Register the schema
        cls.tool_schemas[name] = schema
    
    @classmethod
    def get_all_tools(cls) -> Dict[str, Callable]:
        """
        Get all registered tools.
        
        Returns:
            Dict[str, Callable]: Dictionary of tool names to tool functions.
        """
        return cls.tools
    
    @classmethod
    def get_all_schemas(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered tool schemas.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of tool names to tool schemas.
        """
        return cls.tool_schemas
    
    @staticmethod
    def safe_execute(func: Callable, **kwargs) -> Dict[str, Any]:
        """
        Safely execute a tool function with error handling.
        
        Args:
            func: Tool function to execute.
            **kwargs: Arguments to pass to the function.
            
        Returns:
            Dict[str, Any]: Result of the function execution.
        """
        # Remove 'reasoning' from kwargs if using direct execution
        if not TRANSPARENT_EXECUTOR_AVAILABLE and "reasoning" in kwargs:
            if "reasoning" in func.__code__.co_varnames:
                # Only keep reasoning if function explicitly accepts it
                pass
            else:
                # Remove reasoning as it's not used
                kwargs.pop("reasoning")
        
        try:
            result = func(**kwargs)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            logger.error(f"Error executing {func.__name__}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def create_tool_schema(
        name: str,
        description: str,
        parameters: Dict[str, Dict[str, Any]],
        required: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a tool schema for function calling.
        
        Args:
            name: Name of the tool.
            description: Description of the tool.
            parameters: Dictionary of parameter names to parameter schemas.
            required: List of required parameter names.
            
        Returns:
            Dict[str, Any]: Tool schema.
        """
        if required is None:
            required = []
            
        # Add reasoning parameter if using transparent executor
        if TRANSPARENT_EXECUTOR_AVAILABLE and "reasoning" not in parameters:
            parameters["reasoning"] = {
                "type": "string",
                "description": "Reasoning behind this function call."
            }
            
        return {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required
            }
        } 