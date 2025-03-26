#!/usr/bin/env python
"""
components tools for the Reachy 2 robot.

This module provides tools for interacting with the components module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class ComponentsTools(BaseTool):
    """Tools for interacting with the components module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all components tools."""
        cls.register_tool(
            name="components_antenna_Antenna___init__",
            func=cls.components_antenna_Antenna___init__,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna___init__",
                description="""Initialize the Antenna with its initial state and configuration.

Args:
    uid: The unique identifier of the component.
    name: The name of the joint.
    initial_state: A dictionary containing the initial state of the joint, with
        each entry representing a specific parameter of the joint (e.g., present position).
    grpc_channel: The gRPC channel used to communicate with the DynamixelMotor service.
    goto_stub: The gRPC stub for controlling goto movements.
    part: The part to which this joint belongs.""",
                parameters={'uid': {'type': 'integer', 'description': 'The unique identifier of the component.'}, 'name': {'type': 'string', 'description': 'The name of the joint.'}, 'initial_state': {'type': 'string', 'description': 'A dictionary containing the initial state of the joint, with'}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC channel used to communicate with the DynamixelMotor service.'}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub for controlling goto movements.'}, 'part': {'type': 'string', 'description': 'The part to which this joint belongs.'}},
                required=['uid', 'name', 'initial_state', 'grpc_channel', 'goto_stub', 'part']
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_goto_posture",
            func=cls.components_antenna_Antenna_goto_posture,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_goto_posture",
                description="""Send the antenna to standard positions within the specified duration.

The default posture sets the antenna is 0.0.

Args:
    common_posture: The standard positions to which all joints will be sent.
        It can be 'default' or 'elbow_90'. Defaults to 'default'.
    duration: The time duration in seconds for the robot to move to the specified posture.
        Defaults to 2.
    wait: Determines whether the program should wait for the movement to finish before
        returning. If set to `True`, the program waits for the movement to complete before continuing
        execution. Defaults to `False`.
    wait_for_goto_end: Specifies whether commands will be sent to a part immediately or
        only after all previous commands in the queue have been executed. If set to `False`, the program
        will cancel all executing moves and queues. Defaults to `True`.
    interpolation_mode: The type of interpolation used when moving the arm's joints.
        Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.

Returns:
    The unique GoToId associated with the movement command.""",
                parameters={'common_posture': {'type': 'string', 'description': 'The standard positions to which all joints will be sent.'}, 'duration': {'type': 'number', 'description': 'The time duration in seconds for the robot to move to the specified posture.'}, 'wait': {'type': 'boolean', 'description': 'Determines whether the program should wait for the movement to finish before'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Specifies whether commands will be sent to a part immediately or'}, 'interpolation_mode': {'type': 'string', 'description': "The type of interpolation used when moving the arm's joints."}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_goto",
            func=cls.components_antenna_Antenna_goto,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_goto",
                description="""Send the antenna to a specified goal position.

Args:
    target: The desired goal position for the antenna.
    duration: The time in seconds for the movement to be completed. Defaults to 2.
    wait: If True, the function waits until the movement is completed before returning.
            Defaults to False.
    interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk"
            or "linear". Defaults to "minimum_jerk".
    degrees: If True, the joint value in the `target` argument is treated as degrees.
            Defaults to True.

Raises:
    TypeError : If the input type for `target` is invalid
    ValueError: If the `duration` is set to 0.

Returns:
    GoToId: The unique identifier for the movement command.""",
                parameters={'target': {'type': 'number', 'description': 'The desired goal position for the antenna.'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the movement to be completed. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the movement is completed before returning.'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation method to be used. It can be either "minimum_jerk"'}, 'degrees': {'type': 'boolean', 'description': 'If True, the joint value in the `target` argument is treated as degrees.'}},
                required=['target', 'duration', 'wait', 'interpolation_mode', 'degrees']
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna___repr__",
            func=cls.components_antenna_Antenna___repr__,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna___repr__",
                description="""Clean representation of the Antenna only joint (DynamixelMotor).""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_turn_on",
            func=cls.components_antenna_Antenna_turn_on,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_turn_on",
                description="""Turn on the antenna's motor.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_turn_off",
            func=cls.components_antenna_Antenna_turn_off,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_turn_off",
                description="""Turn off the antenna's motor.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_is_on",
            func=cls.components_antenna_Antenna_is_on,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_is_on",
                description="""Check if the antenna is currently stiff.

Returns:
    `True` if the antenna's motor is stiff (not compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_is_off",
            func=cls.components_antenna_Antenna_is_off,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_is_off",
                description="""Check if the antenna is currently stiff.

Returns:
    `True` if the antenna's motor is stiff (not compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_present_position",
            func=cls.components_antenna_Antenna_present_position,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_present_position",
                description="""Get the present position of the joint in degrees.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_goal_position",
            func=cls.components_antenna_Antenna_goal_position,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_goal_position",
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
            name="components_antenna_Antenna_send_goal_positions",
            func=cls.components_antenna_Antenna_send_goal_positions,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_send_goal_positions",
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
            name="components_antenna_Antenna_set_speed_limits",
            func=cls.components_antenna_Antenna_set_speed_limits,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_set_speed_limits",
                description="""Set the speed limit as a percentage of the maximum speed the motor.

Args:
    speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
        specified as a float or int.""",
                parameters={'speed_limit': {'type': 'string', 'description': 'The desired speed limit as a percentage (0-100) of the maximum speed. Can be'}},
                required=['speed_limit']
            )
        )
        cls.register_tool(
            name="components_antenna_Antenna_status",
            func=cls.components_antenna_Antenna_status,
            schema=cls.create_tool_schema(
                name="components_antenna_Antenna_status",
                description="""Get the current audit status of the actuator.

Returns:
    The audit status as a string, representing the latest error or status
    message, or `None` if there is no error.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_goto_based_component_IGoToBasedComponent___init__",
            func=cls.components_goto_based_component_IGoToBasedComponent___init__,
            schema=cls.create_tool_schema(
                name="components_goto_based_component_IGoToBasedComponent___init__",
                description="""Initialize the IGoToBasedComponent interface.

Sets up the common attributes needed for handling goto-based movements. This includes
associating the component with the interface and setting up the gRPC stub for performing
goto commands.

Args:
    component_id: The robot component that uses this interface.
    goto_stub: The gRPC stub used to send goto commands to the robot component.""",
                parameters={'component_id': {'type': 'string', 'description': 'The robot component that uses this interface.'}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub used to send goto commands to the robot component.'}},
                required=['component_id', 'goto_stub']
            )
        )
        cls.register_tool(
            name="components_goto_based_component_IGoToBasedComponent_get_goto_playing",
            func=cls.components_goto_based_component_IGoToBasedComponent_get_goto_playing,
            schema=cls.create_tool_schema(
                name="components_goto_based_component_IGoToBasedComponent_get_goto_playing",
                description="""Return the GoToId of the currently playing goto movement on a specific component.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_goto_based_component_IGoToBasedComponent_get_goto_queue",
            func=cls.components_goto_based_component_IGoToBasedComponent_get_goto_queue,
            schema=cls.create_tool_schema(
                name="components_goto_based_component_IGoToBasedComponent_get_goto_queue",
                description="""Return a list of all GoToIds waiting to be played on a specific component.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="components_goto_based_component_IGoToBasedComponent_cancel_all_goto",
            func=cls.components_goto_based_component_IGoToBasedComponent_cancel_all_goto,
            schema=cls.create_tool_schema(
                name="components_goto_based_component_IGoToBasedComponent_cancel_all_goto",
                description="""Request the cancellation of all playing and waiting goto commands for a specific component.

Returns:
    A GoToAck acknowledging the cancellation of all goto commands.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def components_antenna_Antenna___init__(cls, uid, name, initial_state, grpc_channel, goto_stub, part) -> Dict[str, Any]:
        """Initialize the Antenna with its initial state and configuration.
        
        Args:
            uid: The unique identifier of the component.
            name: The name of the joint.
            initial_state: A dictionary containing the initial state of the joint, with
                each entry representing a specific parameter of the joint (e.g., present position).
            grpc_channel: The gRPC channel used to communicate with the DynamixelMotor service.
            goto_stub: The gRPC stub for controlling goto movements.
            part: The part to which this joint belongs."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna___init__(uid, name, initial_state, grpc_channel, goto_stub, part)

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
    def components_antenna_Antenna_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode) -> Dict[str, Any]:
        """Send the antenna to standard positions within the specified duration.
        
        The default posture sets the antenna is 0.0.
        
        Args:
            common_posture: The standard positions to which all joints will be sent.
                It can be 'default' or 'elbow_90'. Defaults to 'default'.
            duration: The time duration in seconds for the robot to move to the specified posture.
                Defaults to 2.
            wait: Determines whether the program should wait for the movement to finish before
                returning. If set to `True`, the program waits for the movement to complete before continuing
                execution. Defaults to `False`.
            wait_for_goto_end: Specifies whether commands will be sent to a part immediately or
                only after all previous commands in the queue have been executed. If set to `False`, the program
                will cancel all executing moves and queues. Defaults to `True`.
            interpolation_mode: The type of interpolation used when moving the arm's joints.
                Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.
        
        Returns:
            The unique GoToId associated with the movement command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode)

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
    def components_antenna_Antenna_goto(cls, target, duration, wait, interpolation_mode, degrees) -> Dict[str, Any]:
        """Send the antenna to a specified goal position.
        
        Args:
            target: The desired goal position for the antenna.
            duration: The time in seconds for the movement to be completed. Defaults to 2.
            wait: If True, the function waits until the movement is completed before returning.
                    Defaults to False.
            interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk"
                    or "linear". Defaults to "minimum_jerk".
            degrees: If True, the joint value in the `target` argument is treated as degrees.
                    Defaults to True.
        
        Raises:
            TypeError : If the input type for `target` is invalid
            ValueError: If the `duration` is set to 0.
        
        Returns:
            GoToId: The unique identifier for the movement command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_goto(target, duration, wait, interpolation_mode, degrees)

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
    def components_antenna_Antenna___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of the Antenna only joint (DynamixelMotor)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna___repr__()

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
    def components_antenna_Antenna_turn_on(cls, ) -> Dict[str, Any]:
        """Turn on the antenna's motor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_turn_on()

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
    def components_antenna_Antenna_turn_off(cls, ) -> Dict[str, Any]:
        """Turn off the antenna's motor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_turn_off()

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
    def components_antenna_Antenna_is_on(cls, ) -> Dict[str, Any]:
        """Check if the antenna is currently stiff.
        
        Returns:
            `True` if the antenna's motor is stiff (not compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_is_on()

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
    def components_antenna_Antenna_is_off(cls, ) -> Dict[str, Any]:
        """Check if the antenna is currently stiff.
        
        Returns:
            `True` if the antenna's motor is stiff (not compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_is_off()

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
    def components_antenna_Antenna_present_position(cls, ) -> Dict[str, Any]:
        """Get the present position of the joint in degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_present_position()

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
    def components_antenna_Antenna_goal_position(cls, value) -> Dict[str, Any]:
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
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_goal_position(value)

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
    def components_antenna_Antenna_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send goal positions to the motor.
        
        If goal positions have been specified, sends them to the motor.
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_send_goal_positions(check_positions)

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
    def components_antenna_Antenna_set_speed_limits(cls, speed_limit) -> Dict[str, Any]:
        """Set the speed limit as a percentage of the maximum speed the motor.
        
        Args:
            speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_set_speed_limits(speed_limit)

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
    def components_antenna_Antenna_status(cls, ) -> Dict[str, Any]:
        """Get the current audit status of the actuator.
        
        Returns:
            The audit status as a string, representing the latest error or status
            message, or `None` if there is no error."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'antenna')

            # Call the function with parameters
            result = obj.Antenna_status()

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
    def components_goto_based_component_IGoToBasedComponent___init__(cls, component_id, goto_stub) -> Dict[str, Any]:
        """Initialize the IGoToBasedComponent interface.
        
        Sets up the common attributes needed for handling goto-based movements. This includes
        associating the component with the interface and setting up the gRPC stub for performing
        goto commands.
        
        Args:
            component_id: The robot component that uses this interface.
            goto_stub: The gRPC stub used to send goto commands to the robot component."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_component_IGoToBasedComponent___init__(component_id, goto_stub)

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
    def components_goto_based_component_IGoToBasedComponent_get_goto_playing(cls, ) -> Dict[str, Any]:
        """Return the GoToId of the currently playing goto movement on a specific component."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_component_IGoToBasedComponent_get_goto_playing()

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
    def components_goto_based_component_IGoToBasedComponent_get_goto_queue(cls, ) -> Dict[str, Any]:
        """Return a list of all GoToIds waiting to be played on a specific component."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_component_IGoToBasedComponent_get_goto_queue()

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
    def components_goto_based_component_IGoToBasedComponent_cancel_all_goto(cls, ) -> Dict[str, Any]:
        """Request the cancellation of all playing and waiting goto commands for a specific component.
        
        Returns:
            A GoToAck acknowledging the cancellation of all goto commands."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_component_IGoToBasedComponent_cancel_all_goto()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
