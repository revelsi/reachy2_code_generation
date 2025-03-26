#!/usr/bin/env python
"""
sensors tools for the Reachy 2 robot.

This module provides tools for interacting with the sensors module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class SensorsTools(BaseTool):
    """Tools for interacting with the sensors module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all sensors tools."""
        cls.register_tool(
            name="sensors_lidar_Lidar___init__",
            func=cls.sensors_lidar_Lidar___init__,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar___init__",
                description="""Initialize the LIDAR class.""",
                parameters={'initial_state': {'type': 'string', 'description': 'Parameter initial_state'}, 'grpc_channel': {'type': 'string', 'description': 'Parameter grpc_channel'}, 'part': {'type': 'string', 'description': 'Parameter part'}},
                required=['initial_state', 'grpc_channel', 'part']
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar___repr__",
            func=cls.sensors_lidar_Lidar___repr__,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar___repr__",
                description="""Clean representation of a Reachy.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar_get_map",
            func=cls.sensors_lidar_Lidar_get_map,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar_get_map",
                description="""Retrieve the current map of the environment using lidar data.

Returns:
    The current map of the environment as an image (NumPy array) if the lidar map is successfully
    retrieved. Returns `None` if no lidar map is retrieved.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar_safety_slowdown_distance",
            func=cls.sensors_lidar_Lidar_safety_slowdown_distance,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar_safety_slowdown_distance",
                description="""Set the safety distance for a Lidar sensor.

Args:
    value: The safety distance to set for the LidarSafety object. This value specifies
        the distance at which a safety slowdown should be initiated.""",
                parameters={'value': {'type': 'number', 'description': 'The safety distance to set for the LidarSafety object. This value specifies'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar_safety_critical_distance",
            func=cls.sensors_lidar_Lidar_safety_critical_distance,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar_safety_critical_distance",
                description="""Set the critical distance for a Lidar safety feature.

Args:
    value: The critical distance in meters for safety. This value specifies the distance
        at which the mobile base should stop if moving in the direction of an obstacle.
        If at least one point is within the critical distance, even movements that move
        away from the obstacles are slowed down to the "safety_zone" speed.""",
                parameters={'value': {'type': 'number', 'description': 'The critical distance in meters for safety. This value specifies the distance'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar_safety_enabled",
            func=cls.sensors_lidar_Lidar_safety_enabled,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar_safety_enabled",
                description="""Set the safety status for the Lidar device.

Args:
    value: A boolean indicating whether the safety features are enabled or disabled. If `True`, the safety feature
        is enabled.""",
                parameters={'value': {'type': 'boolean', 'description': 'A boolean indicating whether the safety features are enabled or disabled. If `True`, the safety feature'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar_obstacle_detection_status",
            func=cls.sensors_lidar_Lidar_obstacle_detection_status,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar_obstacle_detection_status",
                description="""Get the status of the lidar obstacle detection.

Returns:
    The status of the lidar obstacle detection, which can be one of the following values:
    NO_OBJECT_DETECTED, OBJECT_DETECTED_SLOWDOWN, OBJECT_DETECTED_STOP, or DETECTION_ERROR.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="sensors_lidar_Lidar_reset_safety_default_distances",
            func=cls.sensors_lidar_Lidar_reset_safety_default_distances,
            schema=cls.create_tool_schema(
                name="sensors_lidar_Lidar_reset_safety_default_distances",
                description="""Reset default distance values for safety detection.

The reset values include:
- safety_critical_distance
- safety_slowdown_distance.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def sensors_lidar_Lidar___init__(cls, initial_state, grpc_channel, part) -> Dict[str, Any]:
        """Initialize the LIDAR class."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar___init__(initial_state, grpc_channel, part)

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
    def sensors_lidar_Lidar___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a Reachy."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar___repr__()

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
    def sensors_lidar_Lidar_get_map(cls, ) -> Dict[str, Any]:
        """Retrieve the current map of the environment using lidar data.
        
        Returns:
            The current map of the environment as an image (NumPy array) if the lidar map is successfully
            retrieved. Returns `None` if no lidar map is retrieved."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar_get_map()

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
    def sensors_lidar_Lidar_safety_slowdown_distance(cls, value) -> Dict[str, Any]:
        """Set the safety distance for a Lidar sensor.
        
        Args:
            value: The safety distance to set for the LidarSafety object. This value specifies
                the distance at which a safety slowdown should be initiated."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar_safety_slowdown_distance(value)

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
    def sensors_lidar_Lidar_safety_critical_distance(cls, value) -> Dict[str, Any]:
        """Set the critical distance for a Lidar safety feature.
        
        Args:
            value: The critical distance in meters for safety. This value specifies the distance
                at which the mobile base should stop if moving in the direction of an obstacle.
                If at least one point is within the critical distance, even movements that move
                away from the obstacles are slowed down to the "safety_zone" speed."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar_safety_critical_distance(value)

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
    def sensors_lidar_Lidar_safety_enabled(cls, value) -> Dict[str, Any]:
        """Set the safety status for the Lidar device.
        
        Args:
            value: A boolean indicating whether the safety features are enabled or disabled. If `True`, the safety feature
                is enabled."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar_safety_enabled(value)

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
    def sensors_lidar_Lidar_obstacle_detection_status(cls, ) -> Dict[str, Any]:
        """Get the status of the lidar obstacle detection.
        
        Returns:
            The status of the lidar obstacle detection, which can be one of the following values:
            NO_OBJECT_DETECTED, OBJECT_DETECTED_SLOWDOWN, OBJECT_DETECTED_STOP, or DETECTION_ERROR."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar_obstacle_detection_status()

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
    def sensors_lidar_Lidar_reset_safety_default_distances(cls, ) -> Dict[str, Any]:
        """Reset default distance values for safety detection.
        
        The reset values include:
        - safety_critical_distance
        - safety_slowdown_distance."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'lidar')

            # Call the function with parameters
            result = obj.Lidar_reset_safety_default_distances()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
