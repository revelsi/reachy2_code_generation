#!/usr/bin/env python
"""
config tools for the Reachy 2 robot.

This module provides tools for interacting with the config module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class ConfigTools(BaseTool):
    """Tools for interacting with the config module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all config tools."""
        cls.register_tool(
            name="config_reachy_info_ReachyInfo___init__",
            func=cls.config_reachy_info_ReachyInfo___init__,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo___init__",
                description="""Initialize the ReachyInfo instance with robot details.

Args:
    reachy: The Reachy robot object, which provides the robot's info and configuration details.""",
                parameters={'reachy': {'type': 'string', 'description': "The Reachy robot object, which provides the robot's info and configuration details."}},
                required=['reachy']
            )
        )
        cls.register_tool(
            name="config_reachy_info_ReachyInfo___repr__",
            func=cls.config_reachy_info_ReachyInfo___repr__,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo___repr__",
                description="""Clean representation of a ReachyInfo.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="config_reachy_info_ReachyInfo_battery_voltage",
            func=cls.config_reachy_info_ReachyInfo_battery_voltage,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo_battery_voltage",
                description="""Get the battery voltage of the mobile base.

If the mobile base is present, returns its battery voltage. Otherwise, returns a default full
battery value.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="config_reachy_info_ReachyInfo_robot_serial_number",
            func=cls.config_reachy_info_ReachyInfo_robot_serial_number,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo_robot_serial_number",
                description="""Returns the robot's serial number.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="config_reachy_info_ReachyInfo_hardware_version",
            func=cls.config_reachy_info_ReachyInfo_hardware_version,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo_hardware_version",
                description="""Returns the robot's hardware version.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="config_reachy_info_ReachyInfo_core_software_version",
            func=cls.config_reachy_info_ReachyInfo_core_software_version,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo_core_software_version",
                description="""Returns the robot's core software version.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="config_reachy_info_ReachyInfo_mode",
            func=cls.config_reachy_info_ReachyInfo_mode,
            schema=cls.create_tool_schema(
                name="config_reachy_info_ReachyInfo_mode",
                description="""Returns the robot's core mode.

Can be either "FAKE", "REAL" or "GAZEBO".""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def config_reachy_info_ReachyInfo___init__(cls, reachy) -> Dict[str, Any]:
        """Initialize the ReachyInfo instance with robot details.
        
        Args:
            reachy: The Reachy robot object, which provides the robot's info and configuration details."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo___init__(reachy)

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
    def config_reachy_info_ReachyInfo___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a ReachyInfo."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo___repr__()

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
    def config_reachy_info_ReachyInfo_battery_voltage(cls, ) -> Dict[str, Any]:
        """Get the battery voltage of the mobile base.
        
        If the mobile base is present, returns its battery voltage. Otherwise, returns a default full
        battery value."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo_battery_voltage()

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
    def config_reachy_info_ReachyInfo_robot_serial_number(cls, ) -> Dict[str, Any]:
        """Returns the robot's serial number."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo_robot_serial_number()

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
    def config_reachy_info_ReachyInfo_hardware_version(cls, ) -> Dict[str, Any]:
        """Returns the robot's hardware version."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo_hardware_version()

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
    def config_reachy_info_ReachyInfo_core_software_version(cls, ) -> Dict[str, Any]:
        """Returns the robot's core software version."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo_core_software_version()

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
    def config_reachy_info_ReachyInfo_mode(cls, ) -> Dict[str, Any]:
        """Returns the robot's core mode.
        
        Can be either "FAKE", "REAL" or "GAZEBO"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'reachy')

            # Call the function with parameters
            result = obj.info_ReachyInfo_mode()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
