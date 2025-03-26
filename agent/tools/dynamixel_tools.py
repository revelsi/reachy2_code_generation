#!/usr/bin/env python
"""
dynamixel tools for the Reachy 2 robot.

This module provides tools for interacting with the dynamixel module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class DynamixelTools(BaseTool):
    """Tools for interacting with the dynamixel module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all dynamixel tools."""
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor___init__",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor___init__,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor___init__",
                description="""Initialize the DynamixelMotor with its initial state and configuration.

This sets up the motor by assigning its state based on the provided initial values.

Args:
    uid: The unique identifier of the component.
    name: The name of the component.
    initial_state: A dictionary containing the initial state of the joint, with
        each entry representing a specific parameter of the joint (e.g., present position).
    grpc_channel: The gRPC channel used to communicate with the DynamixelMotor service.""",
                parameters={'uid': {'type': 'integer', 'description': 'The unique identifier of the component.'}, 'name': {'type': 'string', 'description': 'The name of the component.'}, 'initial_state': {'type': 'string', 'description': 'A dictionary containing the initial state of the joint, with'}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC channel used to communicate with the DynamixelMotor service.'}},
                required=['uid', 'name', 'initial_state', 'grpc_channel']
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor___repr__",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor___repr__,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor___repr__",
                description="""Clean representation of the DynamixelMotor.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_turn_on",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_turn_on,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_turn_on",
                description="""Turn on the motor.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_turn_off",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_turn_off,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_turn_off",
                description="""Turn off the motor.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_is_on",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_is_on,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_is_on",
                description="""Check if the dynamixel motor is currently stiff.

Returns:
    `True` if the motor is stiff (not compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_present_position",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_present_position,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_present_position",
                description="""Get the present position of the joint in degrees.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_goal_position",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_goal_position,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_goal_position",
                description="""Set the goal position of the joint in degrees.

The goal position is not send to the joint immediately, it is stored locally until the `send_goal_positions` method
is called.

Args:
    value: The goal position to set, specified as a float or int.

Raises:
    TypeError: If the provided value is not a float or int.""",
                parameters={'value': {'type': 'string', 'description': 'The goal position to set, specified as a float or int.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_send_goal_positions",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_send_goal_positions,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_send_goal_positions",
                description="""Send goal positions to the motor.

If goal positions have been specified, sends them to the motor.
Args :
    check_positions: A boolean indicating whether to check the positions after sending the command.
        Defaults to True.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="dynamixel_dynamixel_motor_DynamixelMotor_set_speed_limits",
            func=cls.dynamixel_dynamixel_motor_DynamixelMotor_set_speed_limits,
            schema=cls.create_tool_schema(
                name="dynamixel_dynamixel_motor_DynamixelMotor_set_speed_limits",
                description="""Set the speed limit as a percentage of the maximum speed the motor.

Args:
    speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
        specified as a float or int.""",
                parameters={'speed_limit': {'type': 'string', 'description': 'The desired speed limit as a percentage (0-100) of the maximum speed. Can be'}},
                required=['speed_limit']
            )
        )

    @classmethod
    def dynamixel_dynamixel_motor_DynamixelMotor___init__(cls, uid, name, initial_state, grpc_channel) -> Dict[str, Any]:
        """Initialize the DynamixelMotor with its initial state and configuration.
        
        This sets up the motor by assigning its state based on the provided initial values.
        
        Args:
            uid: The unique identifier of the component.
            name: The name of the component.
            initial_state: A dictionary containing the initial state of the joint, with
                each entry representing a specific parameter of the joint (e.g., present position).
            grpc_channel: The gRPC channel used to communicate with the DynamixelMotor service."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor___init__(uid, name, initial_state, grpc_channel)

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
    def dynamixel_dynamixel_motor_DynamixelMotor___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of the DynamixelMotor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor___repr__()

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
    def dynamixel_dynamixel_motor_DynamixelMotor_turn_on(cls, ) -> Dict[str, Any]:
        """Turn on the motor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_turn_on()

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
    def dynamixel_dynamixel_motor_DynamixelMotor_turn_off(cls, ) -> Dict[str, Any]:
        """Turn off the motor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_turn_off()

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
    def dynamixel_dynamixel_motor_DynamixelMotor_is_on(cls, ) -> Dict[str, Any]:
        """Check if the dynamixel motor is currently stiff.
        
        Returns:
            `True` if the motor is stiff (not compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_is_on()

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
    def dynamixel_dynamixel_motor_DynamixelMotor_present_position(cls, ) -> Dict[str, Any]:
        """Get the present position of the joint in degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_present_position()

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
    def dynamixel_dynamixel_motor_DynamixelMotor_goal_position(cls, value) -> Dict[str, Any]:
        """Set the goal position of the joint in degrees.
        
        The goal position is not send to the joint immediately, it is stored locally until the `send_goal_positions` method
        is called.
        
        Args:
            value: The goal position to set, specified as a float or int.
        
        Raises:
            TypeError: If the provided value is not a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_goal_position(value)

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
    def dynamixel_dynamixel_motor_DynamixelMotor_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send goal positions to the motor.
        
        If goal positions have been specified, sends them to the motor.
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_send_goal_positions(check_positions)

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
    def dynamixel_dynamixel_motor_DynamixelMotor_set_speed_limits(cls, speed_limit) -> Dict[str, Any]:
        """Set the speed limit as a percentage of the maximum speed the motor.
        
        Args:
            speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.dynamixel

            # Call the function with parameters
            result = obj.motor_DynamixelMotor_set_speed_limits(speed_limit)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
