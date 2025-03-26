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


def get_reachy_instance(host: str = None) -> Any:
    """Get a Reachy instance, connecting if necessary."""
    from agent.tools.connection_manager import connect_to_reachy
    return connect_to_reachy(host=host)


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
        # Register the function
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
        # Remove 'reasoning' from kwargs if present but not accepted by function
        if "reasoning" in kwargs:
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
        Create a tool schema for code generation.
        
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
            
        # Create schema
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required
                }
            }
        } 