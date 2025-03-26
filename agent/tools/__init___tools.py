#!/usr/bin/env python
"""
__init__ tools for the Reachy 2 robot.

This module provides tools for interacting with the __init__ module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class InitTools(BaseTool):
    """Tools for interacting with the __init__ module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all __init__ tools."""
        cls.register_tool(
            name="__init___get_dependencies_from_setup_cfg",
            func=cls.__init___get_dependencies_from_setup_cfg,
            schema=cls.create_tool_schema(
                name="__init___get_dependencies_from_setup_cfg",
                description="""Get dependencies from setup.cfg file.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="__init___check_reachy2_sdk_api_dependency",
            func=cls.__init___check_reachy2_sdk_api_dependency,
            schema=cls.create_tool_schema(
                name="__init___check_reachy2_sdk_api_dependency",
                description="""Check if the installed version of reachy2-sdk-api is compatible with the required one.

Also check if the used version of reachy2-sdk-api is higher than the minimal required version.""",
                parameters={'requirement': {'type': 'string', 'description': 'Parameter requirement'}},
                required=['requirement']
            )
        )
        cls.register_tool(
            name="__init___check_dependencies",
            func=cls.__init___check_dependencies,
            schema=cls.create_tool_schema(
                name="__init___check_dependencies",
                description="""Check if the installed dependencies are compatible with the required ones.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def __init___get_dependencies_from_setup_cfg(cls, ) -> Dict[str, Any]:
        """Get dependencies from setup.cfg file."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.

            # Call the function with parameters
            result = obj.init___get_dependencies_from_setup_cfg()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def __init___check_reachy2_sdk_api_dependency(cls, requirement) -> Dict[str, Any]:
        """Check if the installed version of reachy2-sdk-api is compatible with the required one.
        
        Also check if the used version of reachy2-sdk-api is higher than the minimal required version."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.

            # Call the function with parameters
            result = obj.init___check_reachy2_sdk_api_dependency(requirement)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def __init___check_dependencies(cls, ) -> Dict[str, Any]:
        """Check if the installed dependencies are compatible with the required ones."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.

            # Call the function with parameters
            result = obj.init___check_dependencies()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
