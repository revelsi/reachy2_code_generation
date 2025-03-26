#!/usr/bin/env python
"""
orbita tools for the Reachy 2 robot.

This module provides tools for interacting with the orbita module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class OrbitaTools(BaseTool):
    """Tools for interacting with the orbita module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all orbita tools."""
        cls.register_tool(
            name="orbita_orbita_axis_OrbitaAxis___init__",
            func=cls.orbita_orbita_axis_OrbitaAxis___init__,
            schema=cls.create_tool_schema(
                name="orbita_orbita_axis_OrbitaAxis___init__",
                description="""Initialize the axis with its initial state.

Args:
    initial_state: A dictionary containing the initial state values for the axis. The keys should include
        "present_speed" and "present_load", with corresponding FloatValue objects as values.""",
                parameters={'initial_state': {'type': 'object', 'description': 'A dictionary containing the initial state values for the axis. The keys should include'}},
                required=['initial_state']
            )
        )
        cls.register_tool(
            name="orbita_orbita_axis_OrbitaAxis_present_speed",
            func=cls.orbita_orbita_axis_OrbitaAxis_present_speed,
            schema=cls.create_tool_schema(
                name="orbita_orbita_axis_OrbitaAxis_present_speed",
                description="""Get the present speed of the axis in radians per second.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_axis_OrbitaAxis_present_load",
            func=cls.orbita_orbita_axis_OrbitaAxis_present_load,
            schema=cls.create_tool_schema(
                name="orbita_orbita_axis_OrbitaAxis_present_load",
                description="""Get the present load of the axis in Newtons.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita___init__",
            func=cls.orbita_orbita_Orbita___init__,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita___init__",
                description="""Initialize the Orbita actuator with its common attributes.

Args:
    uid: The unique identifier for the actuator.
    name: The name of the actuator.
    orbita_type: Specifies the type of Orbita, either "2d" or "3d".
    stub: The gRPC stub used for communicating with the actuator, which can be an
        instance of either `Orbita2dServiceStub` or `Orbita3dServiceStub`.
    part: The parent part to which the Orbita belongs, used for referencing the
        part's attributes.""",
                parameters={'uid': {'type': 'integer', 'description': 'The unique identifier for the actuator.'}, 'name': {'type': 'string', 'description': 'The name of the actuator.'}, 'orbita_type': {'type': 'string', 'description': 'Specifies the type of Orbita, either "2d" or "3d".'}, 'stub': {'type': 'string', 'description': 'The gRPC stub used for communicating with the actuator, which can be an'}, 'part': {'type': 'string', 'description': 'The parent part to which the Orbita belongs, used for referencing the'}},
                required=['uid', 'name', 'orbita_type', 'stub', 'part']
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita___repr__",
            func=cls.orbita_orbita_Orbita___repr__,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita___repr__",
                description="""Clean representation of an Orbita.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_set_speed_limits",
            func=cls.orbita_orbita_Orbita_set_speed_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_set_speed_limits",
                description="""Set the speed limits for the Orbita actuator.

This method defines the maximum speed for the joints, specified as a percentage
of the maximum speed capability.

Args:
    speed_limit: The desired speed limit as a percentage (0-100).

Raises:
    TypeError: If the provided speed_limit is not a float or int.
    ValueError: If the provided speed_limit is outside the range [0, 100].""",
                parameters={'speed_limit': {'type': 'string', 'description': 'The desired speed limit as a percentage (0-100).'}},
                required=['speed_limit']
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_set_torque_limits",
            func=cls.orbita_orbita_Orbita_set_torque_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_set_torque_limits",
                description="""Set the torque limits for the Orbita actuator.

This method defines the maximum torque for the joints, specified as a percentage
of the maximum torque capability.

Args:
    torque_limit: The desired torque limit as a percentage (0-100).

Raises:
    TypeError: If the provided torque_limit is not a float or int.
    ValueError: If the provided torque_limit is outside the range [0, 100].""",
                parameters={'torque_limit': {'type': 'string', 'description': 'The desired torque limit as a percentage (0-100).'}},
                required=['torque_limit']
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_get_speed_limits",
            func=cls.orbita_orbita_Orbita_get_speed_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_get_speed_limits",
                description="""Get the speed limits for all motors of the actuator.

The speed limits are expressed as percentages of the maximum speed for each motor.

Returns:
    A dictionary where each key is the motor name and the value is the speed limit
    percentage (0-100) for that motor. Motor names are of format "motor_{n}".""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_get_torque_limits",
            func=cls.orbita_orbita_Orbita_get_torque_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_get_torque_limits",
                description="""Get the torque limits for all motors of the actuator.

The torque limits are expressed as percentages of the maximum torque for each motor.

Returns:
    A dictionary where each key is the motor name and the value is the torque limit
    percentage (0-100) for that motor. Motor names are of format "motor_{n}".""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_get_pids",
            func=cls.orbita_orbita_Orbita_get_pids,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_get_pids",
                description="""Get the PID values for all motors of the actuator.

Each motor's PID controller parameters (Proportional, Integral, Derivative) are returned.

Returns:
    A dictionary where each key is the motor name and the value is a tuple containing
    the PID values (P, I, D) for that motor. Motor names are of format "motor_{n}".""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_turn_on",
            func=cls.orbita_orbita_Orbita_turn_on,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_turn_on",
                description="""Turn on all motors of the actuator.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_turn_off",
            func=cls.orbita_orbita_Orbita_turn_off,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_turn_off",
                description="""Turn off all motors of the actuator.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_is_on",
            func=cls.orbita_orbita_Orbita_is_on,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_is_on",
                description="""Check if the actuator is currently stiff.

Returns:
    `True` if the actuator is stiff (not compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_is_off",
            func=cls.orbita_orbita_Orbita_is_off,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_is_off",
                description="""Check if the actuator is currently compliant.

Returns:
    `True` if the actuator is compliant (not stiff), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_temperatures",
            func=cls.orbita_orbita_Orbita_temperatures,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_temperatures",
                description="""Get the current temperatures of all the motors in the actuator.

Returns:
    A dictionary where each key is the motor name and the value is the
    current temperature of the motor in degrees Celsius. Motor names are of format "motor_{n}".""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_send_goal_positions",
            func=cls.orbita_orbita_Orbita_send_goal_positions,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_send_goal_positions",
                description="""Send the goal positions to the actuator.

This method is abstract and should be implemented in derived classes to
send the specified goal positions to the actuator's joints.

Args:
    check_positions: A boolean value indicating whether to check the positions of the joints
        after sending the goal positions. If `True`, a background thread is started to monitor
        the joint positions relative to their last goal positions.
        Default is `True`.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean value indicating whether to check the positions of the joints'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="orbita_orbita_Orbita_status",
            func=cls.orbita_orbita_Orbita_status,
            schema=cls.create_tool_schema(
                name="orbita_orbita_Orbita_status",
                description="""Get the current audit status of the actuator.

Returns:
    The audit status as a string, representing the latest error or status
    message, or `None` if there is no error.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_joint_OrbitaJoint___init__",
            func=cls.orbita_orbita_joint_OrbitaJoint___init__,
            schema=cls.create_tool_schema(
                name="orbita_orbita_joint_OrbitaJoint___init__",
                description="""Initialize the OrbitaJoint with its initial state and configuration.

This sets up the joint by assigning its actuator, axis type, and position order within
the part, and updates its state based on the provided initial values.

Args:
    initial_state: A dictionary containing the initial state of the joint, with
        each entry representing a specific parameter of the joint (e.g., present position).
    axis_type: The type of axis for the joint (e.g., roll, pitch, yaw).
    actuator: The actuator to which this joint belongs.
    position_order_in_part: The position order of this joint in the overall part's
        list of joints.""",
                parameters={'initial_state': {'type': 'object', 'description': 'A dictionary containing the initial state of the joint, with'}, 'axis_type': {'type': 'string', 'description': 'The type of axis for the joint (e.g., roll, pitch, yaw).'}, 'actuator': {'type': 'string', 'description': 'The actuator to which this joint belongs.'}, 'position_order_in_part': {'type': 'integer', 'description': "The position order of this joint in the overall part's"}},
                required=['initial_state', 'axis_type', 'actuator', 'position_order_in_part']
            )
        )
        cls.register_tool(
            name="orbita_orbita_joint_OrbitaJoint___repr__",
            func=cls.orbita_orbita_joint_OrbitaJoint___repr__,
            schema=cls.create_tool_schema(
                name="orbita_orbita_joint_OrbitaJoint___repr__",
                description="""Clean representation of the OrbitaJoint.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_joint_OrbitaJoint_present_position",
            func=cls.orbita_orbita_joint_OrbitaJoint_present_position,
            schema=cls.create_tool_schema(
                name="orbita_orbita_joint_OrbitaJoint_present_position",
                description="""Get the present position of the joint in degrees.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_joint_OrbitaJoint_goal_position",
            func=cls.orbita_orbita_joint_OrbitaJoint_goal_position,
            schema=cls.create_tool_schema(
                name="orbita_orbita_joint_OrbitaJoint_goal_position",
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
            name="orbita_orbita_joint_OrbitaJoint_goto",
            func=cls.orbita_orbita_joint_OrbitaJoint_goto,
            schema=cls.create_tool_schema(
                name="orbita_orbita_joint_OrbitaJoint_goto",
                description="""Send the joint to the specified goal position within a given duration.

Acts like a "goto" movement on the part, where "goto" movements for joints are queued on the part they belong to.

Args:
    goal_position: The target position to move the joint to.
    duration: The time in seconds for the joint to reach the goal position. Defaults to 2.
    wait: Whether to wait for the movement to finish before continuing. Defaults to False.
    interpolation_mode: The type of interpolation to use for the movement, either "minimum_jerk" or "linear".
        Defaults to "minimum_jerk".
    degrees: Whether the goal position is specified in degrees. If True, the position is interpreted as degrees.
        Defaults to True.

Returns:
    The GoToId associated with the movement command.""",
                parameters={'goal_position': {'type': 'number', 'description': 'The target position to move the joint to.'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the joint to reach the goal position. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'Whether to wait for the movement to finish before continuing. Defaults to False.'}, 'interpolation_mode': {'type': 'string', 'description': 'The type of interpolation to use for the movement, either "minimum_jerk" or "linear".'}, 'degrees': {'type': 'boolean', 'description': 'Whether the goal position is specified in degrees. If True, the position is interpreted as degrees.'}},
                required=['goal_position', 'duration', 'wait', 'interpolation_mode', 'degrees']
            )
        )
        cls.register_tool(
            name="orbita_orbita2d_Orbita2d___init__",
            func=cls.orbita_orbita2d_Orbita2d___init__,
            schema=cls.create_tool_schema(
                name="orbita_orbita2d_Orbita2d___init__",
                description="""Initialize the Orbita2d actuator with its joints, motors, and axes.

Args:
    uid: The unique identifier for the actuator.
    name: The name of the actuator.
    axis1: The first axis of the actuator, typically representing roll, pitch, or yaw.
    axis2: The second axis of the actuator, typically representing roll, pitch, or yaw.
    initial_state: The initial state of the Orbita2d actuator, containing the states
        of the joints, motors, and axes.
    grpc_channel: The gRPC communication channel used for interfacing with the
        Orbita2d actuator.
    part: The robot part that this actuator belongs to.
    joints_position_order: A list defining the order of the joint positions in the
        containing part, used to map the actuator's joint positions correctly.""",
                parameters={'uid': {'type': 'integer', 'description': 'The unique identifier for the actuator.'}, 'name': {'type': 'string', 'description': 'The name of the actuator.'}, 'axis1': {'type': 'string', 'description': 'The first axis of the actuator, typically representing roll, pitch, or yaw.'}, 'axis2': {'type': 'string', 'description': 'The second axis of the actuator, typically representing roll, pitch, or yaw.'}, 'initial_state': {'type': 'string', 'description': 'The initial state of the Orbita2d actuator, containing the states'}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC communication channel used for interfacing with the'}, 'part': {'type': 'string', 'description': 'The robot part that this actuator belongs to.'}, 'joints_position_order': {'type': 'array', 'description': 'A list defining the order of the joint positions in the'}},
                required=['uid', 'name', 'axis1', 'axis2', 'initial_state', 'grpc_channel', 'part', 'joints_position_order']
            )
        )
        cls.register_tool(
            name="orbita_orbita2d_Orbita2d___setattr__",
            func=cls.orbita_orbita2d_Orbita2d___setattr__,
            schema=cls.create_tool_schema(
                name="orbita_orbita2d_Orbita2d___setattr__",
                description="""Custom attribute setting to prevent modification of specific attributes.

This method overrides the default behavior of setting attributes to ensure that
certain attributes ('roll', 'pitch', 'yaw') cannot be modified after being set initially.
If an attempt is made to set these attributes again, an AttributeError is raised.

Args:
    __name: The name of the attribute.
    __value: The value to assign to the attribute.

Raises:
    AttributeError: If trying to set the value of 'roll', 'pitch', or 'yaw' after they are already set.""",
                parameters={'__name': {'type': 'string', 'description': 'The name of the attribute.'}, '__value': {'type': 'string', 'description': 'The value to assign to the attribute.'}},
                required=['__name', '__value']
            )
        )
        cls.register_tool(
            name="orbita_orbita2d_Orbita2d_send_goal_positions",
            func=cls.orbita_orbita2d_Orbita2d_send_goal_positions,
            schema=cls.create_tool_schema(
                name="orbita_orbita2d_Orbita2d_send_goal_positions",
                description="""Send goal positions to the actuator's joints.

If goal positions have been specified for any joint of this actuator, sends them to the actuator.

Args :
    check_positions: A boolean indicating whether to check the positions after sending the command.
        Defaults to True.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="orbita_orbita2d_Orbita2d_set_speed_limits",
            func=cls.orbita_orbita2d_Orbita2d_set_speed_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita2d_Orbita2d_set_speed_limits",
                description="""Set the speed limit as a percentage of the maximum speed for all motors of the actuator.

Args:
    speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
        specified as a float or int.""",
                parameters={'speed_limit': {'type': 'string', 'description': 'The desired speed limit as a percentage (0-100) of the maximum speed. Can be'}},
                required=['speed_limit']
            )
        )
        cls.register_tool(
            name="orbita_orbita2d_Orbita2d_set_torque_limits",
            func=cls.orbita_orbita2d_Orbita2d_set_torque_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita2d_Orbita2d_set_torque_limits",
                description="""Set the torque limit as a percentage of the maximum torque for all motors of the actuator.

Args:
    torque_limit: The desired torque limit as a percentage (0-100) of the maximum torque. Can be
        specified as a float or int.""",
                parameters={'torque_limit': {'type': 'string', 'description': 'The desired torque limit as a percentage (0-100) of the maximum torque. Can be'}},
                required=['torque_limit']
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d___init__",
            func=cls.orbita_orbita3d_Orbita3d___init__,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d___init__",
                description="""Initialize the Orbita3d actuator with its joints, motors, and axes.

Args:
    uid: The unique identifier for the actuator.
    name: The name of the actuator.
    initial_state: The initial state of the Orbita3d actuator, containing the states
        of the joints, motors, and axes.
    grpc_channel: The gRPC communication channel used for interfacing with the
        Orbita3d actuator.
    part: The robot part that this actuator belongs to.
    joints_position_order: A list defining the order of the joint positions in the
        containing part, used to map the actuator's joint positions correctly.""",
                parameters={'uid': {'type': 'integer', 'description': 'The unique identifier for the actuator.'}, 'name': {'type': 'string', 'description': 'The name of the actuator.'}, 'initial_state': {'type': 'string', 'description': 'The initial state of the Orbita3d actuator, containing the states'}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC communication channel used for interfacing with the'}, 'part': {'type': 'string', 'description': 'The robot part that this actuator belongs to.'}, 'joints_position_order': {'type': 'array', 'description': 'A list defining the order of the joint positions in the'}},
                required=['uid', 'name', 'initial_state', 'grpc_channel', 'part', 'joints_position_order']
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d_roll",
            func=cls.orbita_orbita3d_Orbita3d_roll,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d_roll",
                description="""Get the roll joint of the actuator.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d_pitch",
            func=cls.orbita_orbita3d_Orbita3d_pitch,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d_pitch",
                description="""Get the pitch joint of the actuator.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d_yaw",
            func=cls.orbita_orbita3d_Orbita3d_yaw,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d_yaw",
                description="""Get the yaw joint of the actuator.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d_send_goal_positions",
            func=cls.orbita_orbita3d_Orbita3d_send_goal_positions,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d_send_goal_positions",
                description="""Send goal positions to the actuator's joints.

If goal positions have been specified for any joint of this actuator, sends them to the actuator.

Args:
    check_positions: A boolean indicating whether to check the positions after sending the command.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d_set_speed_limits",
            func=cls.orbita_orbita3d_Orbita3d_set_speed_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d_set_speed_limits",
                description="""Set the speed limit as a percentage of the maximum speed for all motors of the actuator.

Args:
    speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
        specified as a float or int.""",
                parameters={'speed_limit': {'type': 'string', 'description': 'The desired speed limit as a percentage (0-100) of the maximum speed. Can be'}},
                required=['speed_limit']
            )
        )
        cls.register_tool(
            name="orbita_orbita3d_Orbita3d_set_torque_limits",
            func=cls.orbita_orbita3d_Orbita3d_set_torque_limits,
            schema=cls.create_tool_schema(
                name="orbita_orbita3d_Orbita3d_set_torque_limits",
                description="""Set the torque limit as a percentage of the maximum torque for all motors of the actuator.

Args:
    torque_limit: The desired torque limit as a percentage (0-100) of the maximum torque. Can be
        specified as a float or int.""",
                parameters={'torque_limit': {'type': 'string', 'description': 'The desired torque limit as a percentage (0-100) of the maximum torque. Can be'}},
                required=['torque_limit']
            )
        )
        cls.register_tool(
            name="orbita_utils_to_position",
            func=cls.orbita_utils_to_position,
            schema=cls.create_tool_schema(
                name="orbita_utils_to_position",
                description="""Convert an internal angular value in radians to a value in degrees.

Args:
    internal_pos: The internal angular value in radians.

Returns:
    The corresponding angular value in degrees.""",
                parameters={'internal_pos': {'type': 'number', 'description': 'The internal angular value in radians.'}},
                required=['internal_pos']
            )
        )
        cls.register_tool(
            name="orbita_utils_to_internal_position",
            func=cls.orbita_utils_to_internal_position,
            schema=cls.create_tool_schema(
                name="orbita_utils_to_internal_position",
                description="""Convert an angular value in degrees to a value in radians.

The server expects values in radians, so conversion is necessary.

Args:
    pos: The angular value in degrees.

Returns:
    The corresponding value in radians.

Raises:
    TypeError: If the provided value is not of type int or float.""",
                parameters={'pos': {'type': 'number', 'description': 'The angular value in degrees.'}},
                required=['pos']
            )
        )
        cls.register_tool(
            name="orbita_utils_unwrapped_pid_value",
            func=cls.orbita_utils_unwrapped_pid_value,
            schema=cls.create_tool_schema(
                name="orbita_utils_unwrapped_pid_value",
                description="""Unwrap the internal PID value from a gRPC protobuf object to a Python value.

Args:
    value: The gRPC protobuf object containing the PID values.

Returns:
    A tuple representing the unwrapped PID gains (p, i, d).""",
                parameters={'value': {'type': 'string', 'description': 'The gRPC protobuf object containing the PID values.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="orbita_utils_wrapped_proto_value",
            func=cls.orbita_utils_wrapped_proto_value,
            schema=cls.create_tool_schema(
                name="orbita_utils_wrapped_proto_value",
                description="""Wrap a simple Python value to the corresponding gRPC protobuf type.

Args:
    value: The value to be wrapped, which can be a bool, float, or int.

Returns:
    The corresponding gRPC protobuf object (BoolValue, FloatValue, or UInt32Value).

Raises:
    TypeError: If the provided value is not a supported type.""",
                parameters={'value': {'type': 'string', 'description': 'The value to be wrapped, which can be a bool, float, or int.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="orbita_utils_wrapped_pid_value",
            func=cls.orbita_utils_wrapped_pid_value,
            schema=cls.create_tool_schema(
                name="orbita_utils_wrapped_pid_value",
                description="""Wrap a simple Python value to the corresponding gRPC protobuf type.

Args:
    value: The value to be wrapped, which can be a bool, float, or int.

Returns:
    The corresponding gRPC protobuf object (BoolValue, FloatValue, or UInt32Value).

Raises:
    TypeError: If the provided value is not a supported type.""",
                parameters={'value': {'type': 'string', 'description': 'The value to be wrapped, which can be a bool, float, or int.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="orbita_orbita_motor_OrbitaMotor___init__",
            func=cls.orbita_orbita_motor_OrbitaMotor___init__,
            schema=cls.create_tool_schema(
                name="orbita_orbita_motor_OrbitaMotor___init__",
                description="""Initialize the motor with its initial state.

Args:
    initial_state: A dictionary containing the initial state values for the motor. The keys should include
        "temperature", "speed_limit", "torque_limit", "compliant", and "pid", with corresponding
        FloatValue objects as values.
    actuator: The actuator to which the motor belongs.""",
                parameters={'initial_state': {'type': 'object', 'description': 'A dictionary containing the initial state values for the motor. The keys should include'}, 'actuator': {'type': 'string', 'description': 'The actuator to which the motor belongs.'}},
                required=['initial_state', 'actuator']
            )
        )
        cls.register_tool(
            name="orbita_orbita_motor_OrbitaMotor_speed_limit",
            func=cls.orbita_orbita_motor_OrbitaMotor_speed_limit,
            schema=cls.create_tool_schema(
                name="orbita_orbita_motor_OrbitaMotor_speed_limit",
                description="""Get the speed limit of the motor, as a percentage of the max allowed speed, rounded to three decimal places.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_motor_OrbitaMotor_temperature",
            func=cls.orbita_orbita_motor_OrbitaMotor_temperature,
            schema=cls.create_tool_schema(
                name="orbita_orbita_motor_OrbitaMotor_temperature",
                description="""Get the current temperature of the motor in Celsius degrees.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_motor_OrbitaMotor_torque_limit",
            func=cls.orbita_orbita_motor_OrbitaMotor_torque_limit,
            schema=cls.create_tool_schema(
                name="orbita_orbita_motor_OrbitaMotor_torque_limit",
                description="""Get the torque limit of the axis, as a percentage of the max allowed speed, rounded to three decimal places.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_motor_OrbitaMotor_compliant",
            func=cls.orbita_orbita_motor_OrbitaMotor_compliant,
            schema=cls.create_tool_schema(
                name="orbita_orbita_motor_OrbitaMotor_compliant",
                description="""Get the compliance status of the motor.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="orbita_orbita_motor_OrbitaMotor_pid",
            func=cls.orbita_orbita_motor_OrbitaMotor_pid,
            schema=cls.create_tool_schema(
                name="orbita_orbita_motor_OrbitaMotor_pid",
                description="""Get the PID gains of the motor.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def orbita_orbita_axis_OrbitaAxis___init__(cls, initial_state) -> Dict[str, Any]:
        """Initialize the axis with its initial state.
        
        Args:
            initial_state: A dictionary containing the initial state values for the axis. The keys should include
                "present_speed" and "present_load", with corresponding FloatValue objects as values."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.axis_OrbitaAxis___init__(initial_state)

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
    def orbita_orbita_axis_OrbitaAxis_present_speed(cls, ) -> Dict[str, Any]:
        """Get the present speed of the axis in radians per second."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.axis_OrbitaAxis_present_speed()

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
    def orbita_orbita_axis_OrbitaAxis_present_load(cls, ) -> Dict[str, Any]:
        """Get the present load of the axis in Newtons."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.axis_OrbitaAxis_present_load()

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
    def orbita_orbita_Orbita___init__(cls, uid, name, orbita_type, stub, part) -> Dict[str, Any]:
        """Initialize the Orbita actuator with its common attributes.
        
        Args:
            uid: The unique identifier for the actuator.
            name: The name of the actuator.
            orbita_type: Specifies the type of Orbita, either "2d" or "3d".
            stub: The gRPC stub used for communicating with the actuator, which can be an
                instance of either `Orbita2dServiceStub` or `Orbita3dServiceStub`.
            part: The parent part to which the Orbita belongs, used for referencing the
                part's attributes."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita___init__(uid, name, orbita_type, stub, part)

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
    def orbita_orbita_Orbita___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of an Orbita."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita___repr__()

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
    def orbita_orbita_Orbita_set_speed_limits(cls, speed_limit) -> Dict[str, Any]:
        """Set the speed limits for the Orbita actuator.
        
        This method defines the maximum speed for the joints, specified as a percentage
        of the maximum speed capability.
        
        Args:
            speed_limit: The desired speed limit as a percentage (0-100).
        
        Raises:
            TypeError: If the provided speed_limit is not a float or int.
            ValueError: If the provided speed_limit is outside the range [0, 100]."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_set_speed_limits(speed_limit)

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
    def orbita_orbita_Orbita_set_torque_limits(cls, torque_limit) -> Dict[str, Any]:
        """Set the torque limits for the Orbita actuator.
        
        This method defines the maximum torque for the joints, specified as a percentage
        of the maximum torque capability.
        
        Args:
            torque_limit: The desired torque limit as a percentage (0-100).
        
        Raises:
            TypeError: If the provided torque_limit is not a float or int.
            ValueError: If the provided torque_limit is outside the range [0, 100]."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_set_torque_limits(torque_limit)

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
    def orbita_orbita_Orbita_get_speed_limits(cls, ) -> Dict[str, Any]:
        """Get the speed limits for all motors of the actuator.
        
        The speed limits are expressed as percentages of the maximum speed for each motor.
        
        Returns:
            A dictionary where each key is the motor name and the value is the speed limit
            percentage (0-100) for that motor. Motor names are of format "motor_{n}"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_get_speed_limits()

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
    def orbita_orbita_Orbita_get_torque_limits(cls, ) -> Dict[str, Any]:
        """Get the torque limits for all motors of the actuator.
        
        The torque limits are expressed as percentages of the maximum torque for each motor.
        
        Returns:
            A dictionary where each key is the motor name and the value is the torque limit
            percentage (0-100) for that motor. Motor names are of format "motor_{n}"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_get_torque_limits()

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
    def orbita_orbita_Orbita_get_pids(cls, ) -> Dict[str, Any]:
        """Get the PID values for all motors of the actuator.
        
        Each motor's PID controller parameters (Proportional, Integral, Derivative) are returned.
        
        Returns:
            A dictionary where each key is the motor name and the value is a tuple containing
            the PID values (P, I, D) for that motor. Motor names are of format "motor_{n}"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_get_pids()

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
    def orbita_orbita_Orbita_turn_on(cls, ) -> Dict[str, Any]:
        """Turn on all motors of the actuator."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_turn_on()

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
    def orbita_orbita_Orbita_turn_off(cls, ) -> Dict[str, Any]:
        """Turn off all motors of the actuator."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_turn_off()

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
    def orbita_orbita_Orbita_is_on(cls, ) -> Dict[str, Any]:
        """Check if the actuator is currently stiff.
        
        Returns:
            `True` if the actuator is stiff (not compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_is_on()

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
    def orbita_orbita_Orbita_is_off(cls, ) -> Dict[str, Any]:
        """Check if the actuator is currently compliant.
        
        Returns:
            `True` if the actuator is compliant (not stiff), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_is_off()

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
    def orbita_orbita_Orbita_temperatures(cls, ) -> Dict[str, Any]:
        """Get the current temperatures of all the motors in the actuator.
        
        Returns:
            A dictionary where each key is the motor name and the value is the
            current temperature of the motor in degrees Celsius. Motor names are of format "motor_{n}"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_temperatures()

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
    def orbita_orbita_Orbita_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send the goal positions to the actuator.
        
        This method is abstract and should be implemented in derived classes to
        send the specified goal positions to the actuator's joints.
        
        Args:
            check_positions: A boolean value indicating whether to check the positions of the joints
                after sending the goal positions. If `True`, a background thread is started to monitor
                the joint positions relative to their last goal positions.
                Default is `True`."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_send_goal_positions(check_positions)

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
    def orbita_orbita_Orbita_status(cls, ) -> Dict[str, Any]:
        """Get the current audit status of the actuator.
        
        Returns:
            The audit status as a string, representing the latest error or status
            message, or `None` if there is no error."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.Orbita_status()

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
    def orbita_orbita_joint_OrbitaJoint___init__(cls, initial_state, axis_type, actuator, position_order_in_part) -> Dict[str, Any]:
        """Initialize the OrbitaJoint with its initial state and configuration.
        
        This sets up the joint by assigning its actuator, axis type, and position order within
        the part, and updates its state based on the provided initial values.
        
        Args:
            initial_state: A dictionary containing the initial state of the joint, with
                each entry representing a specific parameter of the joint (e.g., present position).
            axis_type: The type of axis for the joint (e.g., roll, pitch, yaw).
            actuator: The actuator to which this joint belongs.
            position_order_in_part: The position order of this joint in the overall part's
                list of joints."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.joint_OrbitaJoint___init__(initial_state, axis_type, actuator, position_order_in_part)

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
    def orbita_orbita_joint_OrbitaJoint___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of the OrbitaJoint."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.joint_OrbitaJoint___repr__()

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
    def orbita_orbita_joint_OrbitaJoint_present_position(cls, ) -> Dict[str, Any]:
        """Get the present position of the joint in degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.joint_OrbitaJoint_present_position()

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
    def orbita_orbita_joint_OrbitaJoint_goal_position(cls, value) -> Dict[str, Any]:
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
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.joint_OrbitaJoint_goal_position(value)

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
    def orbita_orbita_joint_OrbitaJoint_goto(cls, goal_position, duration, wait, interpolation_mode, degrees) -> Dict[str, Any]:
        """Send the joint to the specified goal position within a given duration.
        
        Acts like a "goto" movement on the part, where "goto" movements for joints are queued on the part they belong to.
        
        Args:
            goal_position: The target position to move the joint to.
            duration: The time in seconds for the joint to reach the goal position. Defaults to 2.
            wait: Whether to wait for the movement to finish before continuing. Defaults to False.
            interpolation_mode: The type of interpolation to use for the movement, either "minimum_jerk" or "linear".
                Defaults to "minimum_jerk".
            degrees: Whether the goal position is specified in degrees. If True, the position is interpreted as degrees.
                Defaults to True.
        
        Returns:
            The GoToId associated with the movement command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.joint_OrbitaJoint_goto(goal_position, duration, wait, interpolation_mode, degrees)

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
    def orbita_orbita2d_Orbita2d___init__(cls, uid, name, axis1, axis2, initial_state, grpc_channel, part, joints_position_order) -> Dict[str, Any]:
        """Initialize the Orbita2d actuator with its joints, motors, and axes.
        
        Args:
            uid: The unique identifier for the actuator.
            name: The name of the actuator.
            axis1: The first axis of the actuator, typically representing roll, pitch, or yaw.
            axis2: The second axis of the actuator, typically representing roll, pitch, or yaw.
            initial_state: The initial state of the Orbita2d actuator, containing the states
                of the joints, motors, and axes.
            grpc_channel: The gRPC communication channel used for interfacing with the
                Orbita2d actuator.
            part: The robot part that this actuator belongs to.
            joints_position_order: A list defining the order of the joint positions in the
                containing part, used to map the actuator's joint positions correctly."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita2d')

            # Call the function with parameters
            result = obj.Orbita2d___init__(uid, name, axis1, axis2, initial_state, grpc_channel, part, joints_position_order)

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
    def orbita_orbita2d_Orbita2d___setattr__(cls, __name, __value) -> Dict[str, Any]:
        """Custom attribute setting to prevent modification of specific attributes.
        
        This method overrides the default behavior of setting attributes to ensure that
        certain attributes ('roll', 'pitch', 'yaw') cannot be modified after being set initially.
        If an attempt is made to set these attributes again, an AttributeError is raised.
        
        Args:
            __name: The name of the attribute.
            __value: The value to assign to the attribute.
        
        Raises:
            AttributeError: If trying to set the value of 'roll', 'pitch', or 'yaw' after they are already set."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita2d')

            # Call the function with parameters
            result = obj.Orbita2d___setattr__(__name, __value)

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
    def orbita_orbita2d_Orbita2d_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send goal positions to the actuator's joints.
        
        If goal positions have been specified for any joint of this actuator, sends them to the actuator.
        
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita2d')

            # Call the function with parameters
            result = obj.Orbita2d_send_goal_positions(check_positions)

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
    def orbita_orbita2d_Orbita2d_set_speed_limits(cls, speed_limit) -> Dict[str, Any]:
        """Set the speed limit as a percentage of the maximum speed for all motors of the actuator.
        
        Args:
            speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita2d')

            # Call the function with parameters
            result = obj.Orbita2d_set_speed_limits(speed_limit)

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
    def orbita_orbita2d_Orbita2d_set_torque_limits(cls, torque_limit) -> Dict[str, Any]:
        """Set the torque limit as a percentage of the maximum torque for all motors of the actuator.
        
        Args:
            torque_limit: The desired torque limit as a percentage (0-100) of the maximum torque. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita2d')

            # Call the function with parameters
            result = obj.Orbita2d_set_torque_limits(torque_limit)

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
    def orbita_orbita3d_Orbita3d___init__(cls, uid, name, initial_state, grpc_channel, part, joints_position_order) -> Dict[str, Any]:
        """Initialize the Orbita3d actuator with its joints, motors, and axes.
        
        Args:
            uid: The unique identifier for the actuator.
            name: The name of the actuator.
            initial_state: The initial state of the Orbita3d actuator, containing the states
                of the joints, motors, and axes.
            grpc_channel: The gRPC communication channel used for interfacing with the
                Orbita3d actuator.
            part: The robot part that this actuator belongs to.
            joints_position_order: A list defining the order of the joint positions in the
                containing part, used to map the actuator's joint positions correctly."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d___init__(uid, name, initial_state, grpc_channel, part, joints_position_order)

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
    def orbita_orbita3d_Orbita3d_roll(cls, ) -> Dict[str, Any]:
        """Get the roll joint of the actuator."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d_roll()

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
    def orbita_orbita3d_Orbita3d_pitch(cls, ) -> Dict[str, Any]:
        """Get the pitch joint of the actuator."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d_pitch()

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
    def orbita_orbita3d_Orbita3d_yaw(cls, ) -> Dict[str, Any]:
        """Get the yaw joint of the actuator."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d_yaw()

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
    def orbita_orbita3d_Orbita3d_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send goal positions to the actuator's joints.
        
        If goal positions have been specified for any joint of this actuator, sends them to the actuator.
        
        Args:
            check_positions: A boolean indicating whether to check the positions after sending the command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d_send_goal_positions(check_positions)

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
    def orbita_orbita3d_Orbita3d_set_speed_limits(cls, speed_limit) -> Dict[str, Any]:
        """Set the speed limit as a percentage of the maximum speed for all motors of the actuator.
        
        Args:
            speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d_set_speed_limits(speed_limit)

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
    def orbita_orbita3d_Orbita3d_set_torque_limits(cls, torque_limit) -> Dict[str, Any]:
        """Set the torque limit as a percentage of the maximum torque for all motors of the actuator.
        
        Args:
            torque_limit: The desired torque limit as a percentage (0-100) of the maximum torque. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'orbita3d')

            # Call the function with parameters
            result = obj.Orbita3d_set_torque_limits(torque_limit)

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
    def orbita_utils_to_position(cls, internal_pos) -> Dict[str, Any]:
        """Convert an internal angular value in radians to a value in degrees.
        
        Args:
            internal_pos: The internal angular value in radians.
        
        Returns:
            The corresponding angular value in degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'utils')

            # Call the function with parameters
            result = obj.to_position(internal_pos)

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
    def orbita_utils_to_internal_position(cls, pos) -> Dict[str, Any]:
        """Convert an angular value in degrees to a value in radians.
        
        The server expects values in radians, so conversion is necessary.
        
        Args:
            pos: The angular value in degrees.
        
        Returns:
            The corresponding value in radians.
        
        Raises:
            TypeError: If the provided value is not of type int or float."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'utils')

            # Call the function with parameters
            result = obj.to_internal_position(pos)

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
    def orbita_utils_unwrapped_pid_value(cls, value) -> Dict[str, Any]:
        """Unwrap the internal PID value from a gRPC protobuf object to a Python value.
        
        Args:
            value: The gRPC protobuf object containing the PID values.
        
        Returns:
            A tuple representing the unwrapped PID gains (p, i, d)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'utils')

            # Call the function with parameters
            result = obj.unwrapped_pid_value(value)

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
    def orbita_utils_wrapped_proto_value(cls, value) -> Dict[str, Any]:
        """Wrap a simple Python value to the corresponding gRPC protobuf type.
        
        Args:
            value: The value to be wrapped, which can be a bool, float, or int.
        
        Returns:
            The corresponding gRPC protobuf object (BoolValue, FloatValue, or UInt32Value).
        
        Raises:
            TypeError: If the provided value is not a supported type."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'utils')

            # Call the function with parameters
            result = obj.wrapped_proto_value(value)

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
    def orbita_utils_wrapped_pid_value(cls, value) -> Dict[str, Any]:
        """Wrap a simple Python value to the corresponding gRPC protobuf type.
        
        Args:
            value: The value to be wrapped, which can be a bool, float, or int.
        
        Returns:
            The corresponding gRPC protobuf object (BoolValue, FloatValue, or UInt32Value).
        
        Raises:
            TypeError: If the provided value is not a supported type."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'utils')

            # Call the function with parameters
            result = obj.wrapped_pid_value(value)

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
    def orbita_orbita_motor_OrbitaMotor___init__(cls, initial_state, actuator) -> Dict[str, Any]:
        """Initialize the motor with its initial state.
        
        Args:
            initial_state: A dictionary containing the initial state values for the motor. The keys should include
                "temperature", "speed_limit", "torque_limit", "compliant", and "pid", with corresponding
                FloatValue objects as values.
            actuator: The actuator to which the motor belongs."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.motor_OrbitaMotor___init__(initial_state, actuator)

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
    def orbita_orbita_motor_OrbitaMotor_speed_limit(cls, ) -> Dict[str, Any]:
        """Get the speed limit of the motor, as a percentage of the max allowed speed, rounded to three decimal places."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.motor_OrbitaMotor_speed_limit()

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
    def orbita_orbita_motor_OrbitaMotor_temperature(cls, ) -> Dict[str, Any]:
        """Get the current temperature of the motor in Celsius degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.motor_OrbitaMotor_temperature()

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
    def orbita_orbita_motor_OrbitaMotor_torque_limit(cls, ) -> Dict[str, Any]:
        """Get the torque limit of the axis, as a percentage of the max allowed speed, rounded to three decimal places."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.motor_OrbitaMotor_torque_limit()

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
    def orbita_orbita_motor_OrbitaMotor_compliant(cls, ) -> Dict[str, Any]:
        """Get the compliance status of the motor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.motor_OrbitaMotor_compliant()

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
    def orbita_orbita_motor_OrbitaMotor_pid(cls, ) -> Dict[str, Any]:
        """Get the PID gains of the motor."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.orbita

            # Call the function with parameters
            result = obj.motor_OrbitaMotor_pid()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
