#!/usr/bin/env python
"""
parts tools for the Reachy 2 robot.

This module provides tools for interacting with the parts module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class PartsTools(BaseTool):
    """Tools for interacting with the parts module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all parts tools."""
        cls.register_tool(
            name="parts_arm_Arm___init__",
            func=cls.parts_arm_Arm___init__,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm___init__",
                description="""Initialize an Arm instance.

This constructor sets up the arm's gRPC communication and initializes its actuators
(shoulder, elbow, and wrist). Optionally, a gripper can also be configured.

Args:
    arm_msg: The protobuf message containing the arm's configuration details.
    initial_state: The initial state of the arm's actuators.
    grpc_channel: The gRPC channel used for communication with the arm's server.
    goto_stub: The gRPC stub for controlling goto movements.""",
                parameters={'arm_msg': {'type': 'string', 'description': "The protobuf message containing the arm's configuration details."}, 'initial_state': {'type': 'string', 'description': "The initial state of the arm's actuators."}, 'grpc_channel': {'type': 'string', 'description': "The gRPC channel used for communication with the arm's server."}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub for controlling goto movements.'}},
                required=['arm_msg', 'initial_state', 'grpc_channel', 'goto_stub']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_shoulder",
            func=cls.parts_arm_Arm_shoulder,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_shoulder",
                description="""Get the shoulder actuator of the arm.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_elbow",
            func=cls.parts_arm_Arm_elbow,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_elbow",
                description="""Get the elbow actuator of the arm.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_wrist",
            func=cls.parts_arm_Arm_wrist,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_wrist",
                description="""Get the wrist actuator of the arm.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_gripper",
            func=cls.parts_arm_Arm_gripper,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_gripper",
                description="""Get the gripper of the arm, or None if not set.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm___repr__",
            func=cls.parts_arm_Arm___repr__,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm___repr__",
                description="""Clean representation of an Arm.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_turn_on",
            func=cls.parts_arm_Arm_turn_on,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_turn_on",
                description="""Turn on all motors of the part, making all arm motors stiff.

If a gripper is present, it will also be turned on.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_turn_off",
            func=cls.parts_arm_Arm_turn_off,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_turn_off",
                description="""Turn off all motors of the part, making all arm motors compliant.

If a gripper is present, it will also be turned off.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_turn_off_smoothly",
            func=cls.parts_arm_Arm_turn_off_smoothly,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_turn_off_smoothly",
                description="""Gradually reduce the torque limit of all motors over 3 seconds before turning them off.

This function decreases the torque limit in steps until the motors are turned off.
It then restores the torque limit to its original value.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_is_on",
            func=cls.parts_arm_Arm_is_on,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_is_on",
                description="""Check if all actuators of the arm are stiff.

Returns:
    `True` if all actuators of the arm are stiff, `False` otherwise.""",
                parameters={'check_gripper': {'type': 'boolean', 'description': 'Parameter check_gripper'}},
                required=['check_gripper']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_is_off",
            func=cls.parts_arm_Arm_is_off,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_is_off",
                description="""Check if all actuators of the arm are compliant.

Returns:
    `True` if all actuators of the arm are compliant, `False` otherwise.""",
                parameters={'check_gripper': {'type': 'boolean', 'description': 'Parameter check_gripper'}},
                required=['check_gripper']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_get_current_positions",
            func=cls.parts_arm_Arm_get_current_positions,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_get_current_positions",
                description="""Return the current joint positions of the arm, either in degrees or radians.

Args:
    degrees: Specifies whether the joint positions should be returned in degrees.
        If set to `True`, the positions are returned in degrees; otherwise, they are returned in radians.
        Defaults to `True`.

Returns:
    A list of float values representing the current joint positions of the arm in the
    following order: [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch,
    wrist_yaw].""",
                parameters={'degrees': {'type': 'boolean', 'description': 'Specifies whether the joint positions should be returned in degrees.'}},
                required=['degrees']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_forward_kinematics",
            func=cls.parts_arm_Arm_forward_kinematics,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_forward_kinematics",
                description="""Compute the forward kinematics of the arm and return a 4x4 pose matrix.

The pose matrix is expressed in Reachy coordinate system.

Args:
    joints_positions: A list of float values representing the positions of the joints
        in the arm. If not provided, the current robot joints positions are used. Defaults to None.
    degrees: Indicates whether the joint positions are in degrees or radians.
        If `True`, the positions are in degrees; if `False`, in radians. Defaults to True.

Returns:
    A 4x4 pose matrix as a NumPy array, expressed in Reachy coordinate system.

Raises:
    ValueError: If `joints_positions` is provided and its length is not 7.
    ValueError: If no solution is found for the given joint positions.""",
                parameters={'joints_positions': {'type': 'array', 'description': 'A list of float values representing the positions of the joints'}, 'degrees': {'type': 'boolean', 'description': 'Indicates whether the joint positions are in degrees or radians.'}},
                required=['joints_positions', 'degrees']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_inverse_kinematics",
            func=cls.parts_arm_Arm_inverse_kinematics,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_inverse_kinematics",
                description="""Compute a joint configuration to reach a specified target pose for the arm end-effector.

Args:
    target: A 4x4 homogeneous pose matrix representing the target pose in
        Reachy coordinate system, provided as a NumPy array.
    q0: An optional initial joint configuration for the arm. If provided, the
        algorithm will use it as a starting point for finding a solution. Defaults to None.
    degrees: Indicates whether the returned joint angles should be in degrees or radians.
        If `True`, angles are in degrees; if `False`, in radians. Defaults to True.
    round: Number of decimal places to round the computed joint angles to before
        returning. If None, no rounding is performed. Defaults to None.

Returns:
    A list of joint angles representing the solution to reach the target pose, in the following order:
        [shoulder_pitch, shoulder_roll, elbo_yaw, elbow_pitch, wrist.roll, wrist.pitch, wrist.yaw].

Raises:
    ValueError: If the target shape is not (4, 4).
    ValueError: If the length of `q0` is not 7.
    ValueError: If vectorized kinematics is attempted (unsupported).
    ValueError: If no solution is found for the given target.""",
                parameters={'target': {'type': 'string', 'description': 'A 4x4 homogeneous pose matrix representing the target pose in'}, 'q0': {'type': 'array', 'description': 'An optional initial joint configuration for the arm. If provided, the'}, 'degrees': {'type': 'boolean', 'description': 'Indicates whether the returned joint angles should be in degrees or radians.'}},
                required=['target', 'q0', 'degrees']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_goto",
            func=cls.parts_arm_Arm_goto,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_goto",
                description="""Move the arm to a specified target position, either in joint space or Cartesian space.

This function allows the arm to move to a specified target using either:
- A list of 7 joint positions, or
- A 4x4 pose matrix representing the desired end-effector position.

The function also supports an optional initial configuration `q0` for
computing the inverse kinematics solution when the target is in Cartesian space.

Args:
    target: The target position. It can either be a list of 7 joint values (for joint space)
            or a 4x4 NumPy array (for Cartesian space).
    duration: The time in seconds for the movement to be completed. Defaults to 2.
    wait: If True, the function waits until the movement is completed before returning.
            Defaults to False.
    interpolation_space: The space in which the interpolation should be performed. It can
            be either "joint_space" or "cartesian_space". Defaults to "joint_space".
    interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk",
            "linear" or "elliptical". Defaults to "minimum_jerk".
    degrees: If True, the joint values in the `target` argument are treated as degrees.
            Defaults to True.
    q0: An optional list of 7 joint values representing the initial configuration
            for inverse kinematics. Defaults to None.
    arc_direction: The direction of the arc to be followed during elliptical interpolation.
            Can be "above", "below", "front", "back", "left" or "right" . Defaults to "above".
    secondary_radius: The secondary radius of the ellipse for elliptical interpolation, in meters.

Returns:
    GoToId: The unique GoToId identifier for the movement command.

Raises:
    TypeError: If the `target` is neither a list nor a pose matrix.
    TypeError: If the `q0` is not a list.
    ValueError: If the `target` list has a length other than 7, or the pose matrix is not
        of shape (4, 4).
    ValueError: If the `q0` list has a length other than 7.
    ValueError: If the `duration` is set to 0.""",
                parameters={'target': {'type': 'string', 'description': 'The target position. It can either be a list of 7 joint values (for joint space)'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the movement to be completed. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the movement is completed before returning.'}, 'interpolation_space': {'type': 'string', 'description': 'The space in which the interpolation should be performed. It can'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation method to be used. It can be either "minimum_jerk",'}, 'degrees': {'type': 'boolean', 'description': 'If True, the joint values in the `target` argument are treated as degrees.'}, 'q0': {'type': 'array', 'description': 'An optional list of 7 joint values representing the initial configuration'}, 'arc_direction': {'type': 'string', 'description': 'The direction of the arc to be followed during elliptical interpolation.'}, 'secondary_radius': {'type': 'number', 'description': 'The secondary radius of the ellipse for elliptical interpolation, in meters.'}},
                required=['target', 'duration', 'wait', 'interpolation_space', 'interpolation_mode', 'degrees', 'q0', 'arc_direction', 'secondary_radius']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_goto_posture",
            func=cls.parts_arm_Arm_goto_posture,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_goto_posture",
                description="""Send all joints to standard positions with optional parameters for duration, waiting, and interpolation mode.

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
    open_gripper: If `True`, the gripper will open, if `False`, it stays in its current position.
        Defaults to `False`.

Returns:
    A unique GoToId identifier for this specific movement.""",
                parameters={'common_posture': {'type': 'string', 'description': 'The standard positions to which all joints will be sent.'}, 'duration': {'type': 'number', 'description': 'The time duration in seconds for the robot to move to the specified posture.'}, 'wait': {'type': 'boolean', 'description': 'Determines whether the program should wait for the movement to finish before'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Specifies whether commands will be sent to a part immediately or'}, 'interpolation_mode': {'type': 'string', 'description': "The type of interpolation used when moving the arm's joints."}, 'open_gripper': {'type': 'boolean', 'description': 'If `True`, the gripper will open, if `False`, it stays in its current position.'}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode', 'open_gripper']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_get_default_posture_joints",
            func=cls.parts_arm_Arm_get_default_posture_joints,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_get_default_posture_joints",
                description="""Get the list of joint positions for default or elbow_90 poses.

Args:
    common_posture: The name of the posture to retrieve. Can be "default" or "elbow_90".
        Defaults to "default".

Returns:
    A list of joint positions in degrees for the specified posture.

Raises:
    ValueError: If `common_posture` is not "default" or "elbow_90".""",
                parameters={'common_posture': {'type': 'string', 'description': 'The name of the posture to retrieve. Can be "default" or "elbow_90".'}},
                required=['common_posture']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_get_default_posture_matrix",
            func=cls.parts_arm_Arm_get_default_posture_matrix,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_get_default_posture_matrix",
                description="""Get the 4x4 pose matrix in Reachy coordinate system for a default robot posture.

Args:
    common_posture: The posture to retrieve. Can be "default" or "elbow_90".
        Defaults to "default".

Returns:
    The 4x4 homogeneous pose matrix for the specified posture in Reachy coordinate system.""",
                parameters={'common_posture': {'type': 'string', 'description': 'The posture to retrieve. Can be "default" or "elbow_90".'}},
                required=['common_posture']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_get_translation_by",
            func=cls.parts_arm_Arm_get_translation_by,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_get_translation_by",
                description="""Return a 4x4 matrix representing a pose translated by specified x, y, z values.

The translation is performed in either the robot or gripper coordinate system.

Args:
    x: Translation along the x-axis in meters (forwards direction) to apply
        to the pose matrix.
    y: Translation along the y-axis in meters (left direction) to apply
        to the pose matrix.
    z: Translation along the z-axis in meters (upwards direction) to apply
        to the pose matrix.
    initial_pose: A 4x4 matrix representing the initial pose of the end-effector in Reachy coordinate system,
        expressed as a NumPy array of type `np.float64`.
        If not provided, the current pose of the arm is used. Defaults to `None`.
    frame: The coordinate system in which the translation should be performed.
        Can be either "robot" or "gripper". Defaults to "robot".

Returns:
    A 4x4 pose matrix, expressed in Reachy coordinate system,
    translated by the specified x, y, z values from the initial pose.

Raises:
    ValueError: If the `frame` is not "robot" or "gripper".""",
                parameters={'x': {'type': 'number', 'description': 'Translation along the x-axis in meters (forwards direction) to apply'}, 'y': {'type': 'number', 'description': 'Translation along the y-axis in meters (left direction) to apply'}, 'z': {'type': 'number', 'description': 'Translation along the z-axis in meters (upwards direction) to apply'}, 'initial_pose': {'type': 'string', 'description': 'A 4x4 matrix representing the initial pose of the end-effector in Reachy coordinate system,'}, 'frame': {'type': 'string', 'description': 'The coordinate system in which the translation should be performed.'}},
                required=['x', 'y', 'z', 'initial_pose', 'frame']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_translate_by",
            func=cls.parts_arm_Arm_translate_by,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_translate_by",
                description="""Create a translation movement for the arm's end effector.

The movement is based on the last sent position or the current position.

Args:
    x: Translation along the x-axis in meters (forwards direction) to apply
        to the pose matrix.
    y: Translation along the y-axis in meters (left direction) to apply
        to the pose matrix.
    z: Translation along the z-axis in meters (vertical direction) to apply
        to the pose matrix.
    duration: Time duration in seconds for the translation movement to be completed.
        Defaults to 2.
    wait: Determines whether the program should wait for the movement to finish before
        returning. If set to `True`, the program waits for the movement to complete before continuing
        execution. Defaults to `False`.
    frame: The coordinate system in which the translation should be performed.
        Can be "robot" or "gripper". Defaults to "robot".
    interpolation_mode: The type of interpolation to be used when moving the arm's
        joints. Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.

Returns:
    The GoToId of the movement command, created using the `goto_from_matrix` method with the
    translated pose computed in the specified frame.

Raises:
    ValueError: If the `frame` is not "robot" or "gripper".""",
                parameters={'x': {'type': 'number', 'description': 'Translation along the x-axis in meters (forwards direction) to apply'}, 'y': {'type': 'number', 'description': 'Translation along the y-axis in meters (left direction) to apply'}, 'z': {'type': 'number', 'description': 'Translation along the z-axis in meters (vertical direction) to apply'}, 'duration': {'type': 'number', 'description': 'Time duration in seconds for the translation movement to be completed.'}, 'wait': {'type': 'boolean', 'description': 'Determines whether the program should wait for the movement to finish before'}, 'frame': {'type': 'string', 'description': 'The coordinate system in which the translation should be performed.'}, 'interpolation_space': {'type': 'string', 'description': 'Parameter interpolation_space'}, 'interpolation_mode': {'type': 'string', 'description': "The type of interpolation to be used when moving the arm's"}, 'arc_direction': {'type': 'string', 'description': 'Parameter arc_direction'}, 'secondary_radius': {'type': 'number', 'description': 'Parameter secondary_radius'}},
                required=['x', 'y', 'z', 'duration', 'wait', 'frame', 'interpolation_space', 'interpolation_mode', 'arc_direction', 'secondary_radius']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_get_rotation_by",
            func=cls.parts_arm_Arm_get_rotation_by,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_get_rotation_by",
                description="""Calculate a new pose matrix by rotating an initial pose matrix by specified roll, pitch, and yaw angles.

The rotation is performed in either the robot or gripper coordinate system.

Args:
    roll: Rotation around the x-axis in the Euler angles representation, specified
        in radians or degrees (based on the `degrees` parameter).
    pitch: Rotation around the y-axis in the Euler angles representation, specified
        in radians or degrees (based on the `degrees` parameter).
    yaw: Rotation around the z-axis in the Euler angles representation, specified
        in radians or degrees (based on the `degrees` parameter).
    initial_pose: A 4x4 matrix representing the initial
        pose of the end-effector, expressed as a NumPy array of type `np.float64`. If not provided,
        the current pose of the arm is used. Defaults to `None`.
    degrees: Specifies whether the rotation angles are provided in degrees. If set to
        `True`, the angles are interpreted as degrees. Defaults to `True`.
    frame: The coordinate system in which the rotation should be performed. Can be
        "robot" or "gripper". Defaults to "robot".

Returns:
    A 4x4 pose matrix, expressed in the Reachy coordinate system, rotated
    by the specified roll, pitch, and yaw angles from the initial pose, in the specified frame.

Raises:
    ValueError: If the `frame` is not "robot" or "gripper".""",
                parameters={'roll': {'type': 'number', 'description': 'Rotation around the x-axis in the Euler angles representation, specified'}, 'pitch': {'type': 'number', 'description': 'Rotation around the y-axis in the Euler angles representation, specified'}, 'yaw': {'type': 'number', 'description': 'Rotation around the z-axis in the Euler angles representation, specified'}, 'initial_pose': {'type': 'string', 'description': 'A 4x4 matrix representing the initial'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the rotation angles are provided in degrees. If set to'}, 'frame': {'type': 'string', 'description': 'The coordinate system in which the rotation should be performed. Can be'}},
                required=['roll', 'pitch', 'yaw', 'initial_pose', 'degrees', 'frame']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_rotate_by",
            func=cls.parts_arm_Arm_rotate_by,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_rotate_by",
                description="""Create a rotation movement for the arm's end effector based on the specified roll, pitch, and yaw angles.

The rotation is performed in either the robot or gripper frame.

Args:
    roll: Rotation around the x-axis in the Euler angles representation, specified
        in radians or degrees (based on the `degrees` parameter).
    pitch: Rotation around the y-axis in the Euler angles representation, specified
        in radians or degrees (based on the `degrees` parameter).
    yaw: Rotation around the z-axis in the Euler angles representation, specified
        in radians or degrees (based on the `degrees` parameter).
    duration: Time duration in seconds for the rotation movement to be completed.
        Defaults to 2.
    wait: Determines whether the program should wait for the movement to finish before
        returning. If set to `True`, the program waits for the movement to complete before continuing
        execution. Defaults to `False`.
    degrees: Specifies whether the rotation angles are provided in degrees. If set to
        `True`, the angles are interpreted as degrees. Defaults to `True`.
    frame: The coordinate system in which the rotation should be performed. Can be
        "robot" or "gripper". Defaults to "robot".
    interpolation_mode: The type of interpolation to be used when moving the arm's
        joints. Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.

Returns:
    The GoToId of the movement command, created by calling the `goto_from_matrix` method with
    the rotated pose computed in the specified frame.

Raises:
    ValueError: If the `frame` is not "robot" or "gripper".""",
                parameters={'roll': {'type': 'number', 'description': 'Rotation around the x-axis in the Euler angles representation, specified'}, 'pitch': {'type': 'number', 'description': 'Rotation around the y-axis in the Euler angles representation, specified'}, 'yaw': {'type': 'number', 'description': 'Rotation around the z-axis in the Euler angles representation, specified'}, 'duration': {'type': 'number', 'description': 'Time duration in seconds for the rotation movement to be completed.'}, 'wait': {'type': 'boolean', 'description': 'Determines whether the program should wait for the movement to finish before'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the rotation angles are provided in degrees. If set to'}, 'frame': {'type': 'string', 'description': 'The coordinate system in which the rotation should be performed. Can be'}, 'interpolation_mode': {'type': 'string', 'description': "The type of interpolation to be used when moving the arm's"}},
                required=['roll', 'pitch', 'yaw', 'duration', 'wait', 'degrees', 'frame', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="parts_arm_Arm_send_goal_positions",
            func=cls.parts_arm_Arm_send_goal_positions,
            schema=cls.create_tool_schema(
                name="parts_arm_Arm_send_goal_positions",
                description="""Send goal positions to the arm's joints, including the gripper.

If goal positions have been specified for any joint of the part, sends them to the robot.

Args :
    check_positions: A boolean indicating whether to check the positions after sending the command.
        Defaults to True.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="parts_goto_based_part_IGoToBasedPart___init__",
            func=cls.parts_goto_based_part_IGoToBasedPart___init__,
            schema=cls.create_tool_schema(
                name="parts_goto_based_part_IGoToBasedPart___init__",
                description="""Initialize the IGoToBasedPart interface.

Sets up the common attributes needed for handling goto-based movements. This includes
associating the part with the interface and setting up the gRPC stub for performing
goto commands.

Args:
    part: The robot part that uses this interface, such as an Arm or Head.
    goto_stub: The gRPC stub used to send goto commands to the robot part.""",
                parameters={'part': {'type': 'string', 'description': 'The robot part that uses this interface, such as an Arm or Head.'}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub used to send goto commands to the robot part.'}},
                required=['part', 'goto_stub']
            )
        )
        cls.register_tool(
            name="parts_goto_based_part_IGoToBasedPart_get_goto_playing",
            func=cls.parts_goto_based_part_IGoToBasedPart_get_goto_playing,
            schema=cls.create_tool_schema(
                name="parts_goto_based_part_IGoToBasedPart_get_goto_playing",
                description="""Return the GoToId of the currently playing goto movement on a specific part.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_goto_based_part_IGoToBasedPart_get_goto_queue",
            func=cls.parts_goto_based_part_IGoToBasedPart_get_goto_queue,
            schema=cls.create_tool_schema(
                name="parts_goto_based_part_IGoToBasedPart_get_goto_queue",
                description="""Return a list of all GoToIds waiting to be played on a specific part.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_goto_based_part_IGoToBasedPart_cancel_all_goto",
            func=cls.parts_goto_based_part_IGoToBasedPart_cancel_all_goto,
            schema=cls.create_tool_schema(
                name="parts_goto_based_part_IGoToBasedPart_cancel_all_goto",
                description="""Request the cancellation of all playing and waiting goto commands for a specific part.

Returns:
    A GoToAck acknowledging the cancellation of all goto commands.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_hand_Hand___init__",
            func=cls.parts_hand_Hand___init__,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand___init__",
                description="""Initialize the Hand component.

Sets up the necessary attributes and configuration for the hand, including the gRPC
stub and initial state.

Args:
    hand_msg: The Hand_proto object containing the configuration details for the hand.
    grpc_channel: The gRPC channel used to communicate with the hand's gRPC service.
    goto_stub: The gRPC stub for controlling goto movements.""",
                parameters={'hand_msg': {'type': 'string', 'description': 'The Hand_proto object containing the configuration details for the hand.'}, 'grpc_channel': {'type': 'string', 'description': "The gRPC channel used to communicate with the hand's gRPC service."}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub for controlling goto movements.'}},
                required=['hand_msg', 'grpc_channel', 'goto_stub']
            )
        )
        cls.register_tool(
            name="parts_hand_Hand_is_on",
            func=cls.parts_hand_Hand_is_on,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand_is_on",
                description="""Check if the hand is stiff.

Returns:
    `True` if the hand is on (not compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_hand_Hand_is_off",
            func=cls.parts_hand_Hand_is_off,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand_is_off",
                description="""Check if the hand is compliant.

Returns:
    `True` if the hand is off (compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_hand_Hand_is_moving",
            func=cls.parts_hand_Hand_is_moving,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand_is_moving",
                description="""Check if the hand is currently moving.

Returns:
    `True` if any joint of the hand is moving, `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_hand_Hand_open",
            func=cls.parts_hand_Hand_open,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand_open",
                description="""Open the hand.

Raises:
    RuntimeError: If the gripper is off and the open request cannot be sent.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_hand_Hand_close",
            func=cls.parts_hand_Hand_close,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand_close",
                description="""Close the hand.

Raises:
    RuntimeError: If the gripper is off and the close request cannot be sent.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_hand_Hand_send_goal_positions",
            func=cls.parts_hand_Hand_send_goal_positions,
            schema=cls.create_tool_schema(
                name="parts_hand_Hand_send_goal_positions",
                description="""Send the goal positions to the hand's joints.

If any goal position has been specified for any of the gripper's joints, sends them to the robot.
If the hand is off, the command is not sent.

Args :
    check_positions: A boolean indicating whether to check the positions after sending the command.
        Defaults to True.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="parts_head_Head___init__",
            func=cls.parts_head_Head___init__,
            schema=cls.create_tool_schema(
                name="parts_head_Head___init__",
                description="""Initialize the Head component with its actuators.

Sets up the necessary attributes and configuration for the head, including the gRPC
stubs and initial state.

Args:
    head_msg: The Head_proto object containing the configuration details for the head.
    initial_state: The initial state of the head, represented as a HeadState object.
    grpc_channel: The gRPC channel used to communicate with the head's gRPC service.
    goto_stub: The GoToServiceStub used to handle goto-based movements for the head.""",
                parameters={'head_msg': {'type': 'string', 'description': 'The Head_proto object containing the configuration details for the head.'}, 'initial_state': {'type': 'string', 'description': 'The initial state of the head, represented as a HeadState object.'}, 'grpc_channel': {'type': 'string', 'description': "The gRPC channel used to communicate with the head's gRPC service."}, 'goto_stub': {'type': 'string', 'description': 'The GoToServiceStub used to handle goto-based movements for the head.'}},
                required=['head_msg', 'initial_state', 'grpc_channel', 'goto_stub']
            )
        )
        cls.register_tool(
            name="parts_head_Head___repr__",
            func=cls.parts_head_Head___repr__,
            schema=cls.create_tool_schema(
                name="parts_head_Head___repr__",
                description="""Clean representation of an Head.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_head_Head_neck",
            func=cls.parts_head_Head_neck,
            schema=cls.create_tool_schema(
                name="parts_head_Head_neck",
                description="""Get the neck actuator of the head.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_head_Head_l_antenna",
            func=cls.parts_head_Head_l_antenna,
            schema=cls.create_tool_schema(
                name="parts_head_Head_l_antenna",
                description="""Get the left antenna actuator of the head.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_head_Head_r_antenna",
            func=cls.parts_head_Head_r_antenna,
            schema=cls.create_tool_schema(
                name="parts_head_Head_r_antenna",
                description="""Get the right antenna actuator of the head.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_head_Head_get_current_orientation",
            func=cls.parts_head_Head_get_current_orientation,
            schema=cls.create_tool_schema(
                name="parts_head_Head_get_current_orientation",
                description="""Get the current orientation of the head.

Returns:
    The orientation of the head as a quaternion (w, x, y, z).""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_head_Head_get_current_positions",
            func=cls.parts_head_Head_get_current_positions,
            schema=cls.create_tool_schema(
                name="parts_head_Head_get_current_positions",
                description="""Return the current joint positions of the neck.

Returns:
    A list of the current neck joint positions in the order [roll, pitch, yaw].""",
                parameters={'degrees': {'type': 'boolean', 'description': 'Parameter degrees'}},
                required=['degrees']
            )
        )
        cls.register_tool(
            name="parts_head_Head_goto",
            func=cls.parts_head_Head_goto,
            schema=cls.create_tool_schema(
                name="parts_head_Head_goto",
                description="""Send the neck to a specified orientation.

This method moves the neck either to a given roll-pitch-yaw (RPY) position or to a quaternion orientation.

Args:
    target: The desired orientation for the neck. Can either be:
        - A list of three floats [roll, pitch, yaw] representing the RPY orientation (in degrees if `degrees=True`).
        - A pyQuat object representing a quaternion.
    duration: The time in seconds for the movement to be completed. Defaults to 2.
    wait: If True, the function waits until the movement is completed before returning.
            Defaults to False.
    interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk"
            or "linear". Defaults to "minimum_jerk".
    degrees: If True, the RPY values in the `target` argument are treated as degrees.
            Defaults to True.

Raises:
    TypeError : If the input type for `target` is invalid
    ValueError: If the `duration` is set to 0.

Returns:
    GoToId: The unique identifier for the movement command.""",
                parameters={'target': {'type': 'string', 'description': 'The desired orientation for the neck. Can either be:'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the movement to be completed. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the movement is completed before returning.'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation method to be used. It can be either "minimum_jerk"'}, 'degrees': {'type': 'boolean', 'description': 'If True, the RPY values in the `target` argument are treated as degrees.'}},
                required=['target', 'duration', 'wait', 'interpolation_mode', 'degrees']
            )
        )
        cls.register_tool(
            name="parts_head_Head_look_at",
            func=cls.parts_head_Head_look_at,
            schema=cls.create_tool_schema(
                name="parts_head_Head_look_at",
                description="""Compute and send a neck position to look at a specified point in Reachy's Cartesian space (torso frame).

The (x, y, z) coordinates are expressed in meters, where x is forward, y is left, and z is upward.

Args:
    x: The x-coordinate of the target point.
    y: The y-coordinate of the target point.
    z: The z-coordinate of the target point.
    duration: The time in seconds for the head to look at the point. Defaults to 2.0.
    wait: Whether to wait for the movement to complete before returning. Defaults to False.
    interpolation_mode: The interpolation mode for the movement, either "minimum_jerk" or "linear".
        Defaults to "minimum_jerk".

Returns:
    The unique GoToId associated with the movement command.

Raises:
    ValueError: If the duration is set to 0.""",
                parameters={'x': {'type': 'number', 'description': 'The x-coordinate of the target point.'}, 'y': {'type': 'number', 'description': 'The y-coordinate of the target point.'}, 'z': {'type': 'number', 'description': 'The z-coordinate of the target point.'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the head to look at the point. Defaults to 2.0.'}, 'wait': {'type': 'boolean', 'description': 'Whether to wait for the movement to complete before returning. Defaults to False.'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation mode for the movement, either "minimum_jerk" or "linear".'}},
                required=['x', 'y', 'z', 'duration', 'wait', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="parts_head_Head_rotate_by",
            func=cls.parts_head_Head_rotate_by,
            schema=cls.create_tool_schema(
                name="parts_head_Head_rotate_by",
                description="""Rotate the neck by the specified angles.

Args:
    roll: The angle in degrees to rotate around the x-axis (roll). Defaults to 0.
    pitch: The angle in degrees to rotate around the y-axis (pitch). Defaults to 0.
    yaw: The angle in degrees to rotate around the z-axis (yaw). Defaults to 0.
    duration: The time in seconds for the neck to reach the target posture. Defaults to 2.
    wait: Whether to wait for the movement to complete before returning. Defaults to False.
    degrees: Whether the angles are provided in degrees. If True, the angles will be converted to radians.
        Defaults to True.
    frame: The frame of reference for the rotation. Can be either "robot" or "head". Defaults to "robot".
    interpolation_mode: The interpolation mode for the movement, either "minimum_jerk" or "linear".
        Defaults to "minimum_jerk".


Raises:
    ValueError: If the frame is not "robot" or "head".
    ValueError: If the duration is set to 0.
    ValueError: If the interpolation mode is not "minimum_jerk" or "linear".""",
                parameters={'roll': {'type': 'number', 'description': 'The angle in degrees to rotate around the x-axis (roll). Defaults to 0.'}, 'pitch': {'type': 'number', 'description': 'The angle in degrees to rotate around the y-axis (pitch). Defaults to 0.'}, 'yaw': {'type': 'number', 'description': 'The angle in degrees to rotate around the z-axis (yaw). Defaults to 0.'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the neck to reach the target posture. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'Whether to wait for the movement to complete before returning. Defaults to False.'}, 'degrees': {'type': 'boolean', 'description': 'Whether the angles are provided in degrees. If True, the angles will be converted to radians.'}, 'frame': {'type': 'string', 'description': 'The frame of reference for the rotation. Can be either "robot" or "head". Defaults to "robot".'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation mode for the movement, either "minimum_jerk" or "linear".'}},
                required=['roll', 'pitch', 'yaw', 'duration', 'wait', 'degrees', 'frame', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="parts_head_Head_goto_posture",
            func=cls.parts_head_Head_goto_posture,
            schema=cls.create_tool_schema(
                name="parts_head_Head_goto_posture",
                description="""Send all neck joints to standard positions within the specified duration.

The default posture sets the neck joints to [0, -10, 0] (roll, pitch, yaw).

Args:
    common_posture: The standard positions to which all joints will be sent.
        It can be 'default' or 'elbow_90'. Defaults to 'default'.
    duration: The time in seconds for the neck to reach the target posture. Defaults to 2.
    wait: Whether to wait for the movement to complete before returning. Defaults to False.
    wait_for_goto_end: Whether to wait for all previous goto commands to finish before executing
        the current command. If False, it cancels all ongoing commands. Defaults to True.
    interpolation_mode: The interpolation mode for the movement, either "minimum_jerk" or "linear".
        Defaults to "minimum_jerk".

Returns:
    The unique GoToId associated with the movement command.""",
                parameters={'common_posture': {'type': 'string', 'description': 'The standard positions to which all joints will be sent.'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the neck to reach the target posture. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'Whether to wait for the movement to complete before returning. Defaults to False.'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Whether to wait for all previous goto commands to finish before executing'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation mode for the movement, either "minimum_jerk" or "linear".'}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="parts_joints_based_part_JointsBasedPart___init__",
            func=cls.parts_joints_based_part_JointsBasedPart___init__,
            schema=cls.create_tool_schema(
                name="parts_joints_based_part_JointsBasedPart___init__",
                description="""Initialize the JointsBasedPart with its common attributes.

Sets up the gRPC communication channel and service stub for controlling the joint-based
part of the robot, such as an arm or head.

Args:
    proto_msg: A protocol message representing the part's configuration. It can be an
        Arm_proto or Head_proto object.
    grpc_channel: The gRPC channel used to communicate with the corresponding service.
    stub: The service stub for the gRPC communication, which can be an ArmServiceStub or
        HeadServiceStub, depending on the part type.""",
                parameters={'proto_msg': {'type': 'string', 'description': "A protocol message representing the part's configuration. It can be an"}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC channel used to communicate with the corresponding service.'}, 'stub': {'type': 'string', 'description': 'The service stub for the gRPC communication, which can be an ArmServiceStub or'}},
                required=['proto_msg', 'grpc_channel', 'stub']
            )
        )
        cls.register_tool(
            name="parts_joints_based_part_JointsBasedPart_joints",
            func=cls.parts_joints_based_part_JointsBasedPart_joints,
            schema=cls.create_tool_schema(
                name="parts_joints_based_part_JointsBasedPart_joints",
                description="""Get all the arm's joints.

Returns:
    A dictionary of all the arm's joints, with joint names as keys and joint objects as values.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_joints_based_part_JointsBasedPart_get_current_positions",
            func=cls.parts_joints_based_part_JointsBasedPart_get_current_positions,
            schema=cls.create_tool_schema(
                name="parts_joints_based_part_JointsBasedPart_get_current_positions",
                description="""Get the current positions of all joints.

Returns:
    A list of float values representing the present positions in degrees of the arm's joints.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_joints_based_part_JointsBasedPart_send_goal_positions",
            func=cls.parts_joints_based_part_JointsBasedPart_send_goal_positions,
            schema=cls.create_tool_schema(
                name="parts_joints_based_part_JointsBasedPart_send_goal_positions",
                description="""Send goal positions to the part's joints.

If goal positions have been specified for any joint of the part, sends them to the robot.

Args :
    check_positions: A boolean indicating whether to check the positions after sending the command.
        Defaults to True.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )
        cls.register_tool(
            name="parts_joints_based_part_JointsBasedPart_set_torque_limits",
            func=cls.parts_joints_based_part_JointsBasedPart_set_torque_limits,
            schema=cls.create_tool_schema(
                name="parts_joints_based_part_JointsBasedPart_set_torque_limits",
                description="""Set the torque limit as a percentage of the maximum torque for all motors of the part.

Args:
    torque_limit: The desired torque limit as a percentage (0-100) of the maximum torque. Can be
        specified as a float or int.""",
                parameters={'torque_limit': {'type': 'integer', 'description': 'The desired torque limit as a percentage (0-100) of the maximum torque. Can be'}},
                required=['torque_limit']
            )
        )
        cls.register_tool(
            name="parts_joints_based_part_JointsBasedPart_set_speed_limits",
            func=cls.parts_joints_based_part_JointsBasedPart_set_speed_limits,
            schema=cls.create_tool_schema(
                name="parts_joints_based_part_JointsBasedPart_set_speed_limits",
                description="""Set the speed limit as a percentage of the maximum speed for all motors of the part.

Args:
    speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
        specified as a float or int.""",
                parameters={'speed_limit': {'type': 'integer', 'description': 'The desired speed limit as a percentage (0-100) of the maximum speed. Can be'}},
                required=['speed_limit']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase___init__",
            func=cls.parts_mobile_base_MobileBase___init__,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase___init__",
                description="""Initialize the MobileBase with its gRPC communication and configuration.

This sets up the gRPC communication channel and service stubs for controlling the
mobile base, initializes the drive and control modes.
It also sets up the LIDAR safety monitoring.

Args:
    mb_msg: A MobileBase_proto message containing the configuration details for the mobile base.
    initial_state: The initial state of the mobile base, as a MobileBaseState object.
    grpc_channel: The gRPC channel used to communicate with the mobile base service.
    goto_stub: The gRPC service stub for the GoTo service.""",
                parameters={'mb_msg': {'type': 'string', 'description': 'A MobileBase_proto message containing the configuration details for the mobile base.'}, 'initial_state': {'type': 'string', 'description': 'The initial state of the mobile base, as a MobileBaseState object.'}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC channel used to communicate with the mobile base service.'}, 'goto_stub': {'type': 'string', 'description': 'The gRPC service stub for the GoTo service.'}},
                required=['mb_msg', 'initial_state', 'grpc_channel', 'goto_stub']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase___repr__",
            func=cls.parts_mobile_base_MobileBase___repr__,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase___repr__",
                description="""Clean representation of a mobile base.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_battery_voltage",
            func=cls.parts_mobile_base_MobileBase_battery_voltage,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_battery_voltage",
                description="""Return the battery voltage.

The battery should be recharged if the voltage reaches 24.5V or below. If the battery level is low,
a warning message is logged.

Returns:
    The current battery voltage as a float, rounded to one decimal place.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_odometry",
            func=cls.parts_mobile_base_MobileBase_odometry,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_odometry",
                description="""Return the odometry of the base.

The odometry includes the x and y positions in meters and theta in degrees, along with the
velocities in the x, y directions in meters per degrees and the angular velocity in degrees per second.

Returns:
    A dictionary containing the current odometry with keys 'x', 'y', 'theta', 'vx', 'vy', and 'vtheta',
    each rounded to three decimal places.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_last_cmd_vel",
            func=cls.parts_mobile_base_MobileBase_last_cmd_vel,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_last_cmd_vel",
                description="""Return the last command velocity sent to the base.

The velocity includes the x and y components in meters per second and the theta component in degrees per second.

Returns:
    A dictionary containing the last command velocity with keys 'x', 'y', and 'theta',
    each rounded to three decimal places.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_is_on",
            func=cls.parts_mobile_base_MobileBase_is_on,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_is_on",
                description="""Check if the mobile base is currently stiff (not in free-wheel mode).

Returns:
    `True` if the mobile base is not compliant (stiff), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_is_off",
            func=cls.parts_mobile_base_MobileBase_is_off,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_is_off",
                description="""Check if the mobile base is currently compliant (in free-wheel mode).

Returns:
    True if the mobile base is compliant (in free-wheel mode), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_get_current_odometry",
            func=cls.parts_mobile_base_MobileBase_get_current_odometry,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_get_current_odometry",
                description="""Get the current odometry of the mobile base in its reference frame.

Args:
    degrees (bool, optional): Whether to return the orientation (`theta` and `vtheta`) in degrees.
                            Defaults to True.

Returns:
    Dict[str, float]: A dictionary containing the current odometry of the mobile base with:
    - 'x': Position along the x-axis (in meters).
    - 'y': Position along the y-axis (in meters).
    - 'theta': Orientation (in degrees by default, radians if `degrees=False`).
    - 'vx': Linear velocity along the x-axis (in meters per second).
    - 'vy': Linear velocity along the y-axis (in meters per second).
    - 'vtheta': Angular velocity (in degrees per second by default, radians if `degrees=False`).""",
                parameters={'degrees': {'type': 'boolean', 'description': 'Parameter degrees'}},
                required=['degrees']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_goto",
            func=cls.parts_mobile_base_MobileBase_goto,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_goto",
                description="""Send the mobile base to a specified target position.

The (x, y) coordinates define the position in Cartesian space, and theta specifies the orientation in degrees.
The zero position is set when the mobile base is started or when the `reset_odometry` method is called. A timeout
can be provided to avoid the mobile base getting stuck. The tolerance values define the acceptable margins for
reaching the target position.

Args:
    x: The target x-coordinate in meters.
    y: The target y-coordinate in meters.
    theta: The target orientation in degrees.
    wait: If True, the function waits until the movement is completed before returning.
            Defaults to False.
    degrees: If True, the theta value and angle_tolerance are treated as degrees.
            Defaults to True.
    distance_tolerance: Optional; the tolerance to the target position to consider the goto finished, in meters.
    angle_tolerance: Optional; the angle tolerance to the target to consider the goto finished, in meters.
    timeout: Optional; the maximum time allowed to reach the target, in seconds.

Returns:
    GoToId: The unique GoToId identifier for the movement command.

Raises:
    TypeError: If the target is not reached and the mobile base is stopped due to an obstacle.""",
                parameters={'x': {'type': 'number', 'description': 'The target x-coordinate in meters.'}, 'y': {'type': 'number', 'description': 'The target y-coordinate in meters.'}, 'theta': {'type': 'number', 'description': 'The target orientation in degrees.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the movement is completed before returning.'}, 'degrees': {'type': 'boolean', 'description': 'If True, the theta value and angle_tolerance are treated as degrees.'}, 'distance_tolerance': {'type': 'number', 'description': 'Optional; the tolerance to the target position to consider the goto finished, in meters.'}, 'angle_tolerance': {'type': 'number', 'description': 'Optional; the angle tolerance to the target to consider the goto finished, in meters.'}, 'timeout': {'type': 'number', 'description': 'Optional; the maximum time allowed to reach the target, in seconds.'}},
                required=['x', 'y', 'theta', 'wait', 'degrees', 'distance_tolerance', 'angle_tolerance', 'timeout']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_translate_by",
            func=cls.parts_mobile_base_MobileBase_translate_by,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_translate_by",
                description="""Send a target position relative to the current position of the mobile base.

The (x, y) coordinates specify the desired translation in the mobile base's Cartesian space.

Args:
    x: The desired translation along the x-axis in meters.
    y: The desired translation along the y-axis in meters.
    wait:  If True, the function waits until the movement is completed before returning.
    distance_tolerance: Optional; The distance tolerance to the target to consider the goto finished, in meters.
    timeout: An optional timeout for reaching the target position, in seconds.

Returns:
    The GoToId of the movement command, created using the `goto` method.""",
                parameters={'x': {'type': 'number', 'description': 'The desired translation along the x-axis in meters.'}, 'y': {'type': 'number', 'description': 'The desired translation along the y-axis in meters.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the movement is completed before returning.'}, 'distance_tolerance': {'type': 'number', 'description': 'Optional; The distance tolerance to the target to consider the goto finished, in meters.'}, 'timeout': {'type': 'number', 'description': 'An optional timeout for reaching the target position, in seconds.'}},
                required=['x', 'y', 'wait', 'distance_tolerance', 'timeout']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_rotate_by",
            func=cls.parts_mobile_base_MobileBase_rotate_by,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_rotate_by",
                description="""Send a target rotation relative to the current rotation of the mobile base.

The theta parameter defines the desired rotation in degrees.

Args:
    theta: The desired rotation in degrees, relative to the current orientation.
    wait: If True, the function waits until the rotation is completed before returning.
    degrees: If True, the theta value and angle_tolerance are treated as degrees, otherwise as radians.
    angle_tolerance: Optional; The angle tolerance to the target to consider the goto finished.
    timeout: An optional timeout for completing the rotation, in seconds.""",
                parameters={'theta': {'type': 'number', 'description': 'The desired rotation in degrees, relative to the current orientation.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the rotation is completed before returning.'}, 'degrees': {'type': 'boolean', 'description': 'If True, the theta value and angle_tolerance are treated as degrees, otherwise as radians.'}, 'angle_tolerance': {'type': 'number', 'description': 'Optional; The angle tolerance to the target to consider the goto finished.'}, 'timeout': {'type': 'number', 'description': 'An optional timeout for completing the rotation, in seconds.'}},
                required=['theta', 'wait', 'degrees', 'angle_tolerance', 'timeout']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_reset_odometry",
            func=cls.parts_mobile_base_MobileBase_reset_odometry,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_reset_odometry",
                description="""Reset the odometry.

This method resets the mobile base's odometry, so that the current position is now (x, y, theta) = (0, 0, 0).
If any goto is being played, stop the goto and the queued ones.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_set_goal_speed",
            func=cls.parts_mobile_base_MobileBase_set_goal_speed,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_set_goal_speed",
                description="""Set the goal speed for the mobile base.

This method sets the target velocities for the mobile base's movement along the x and y axes, as well as
its rotational speed. The actual movement is executed after calling `send_speed_command`.

Args:
    vx (float | int, optional): Linear velocity along the x-axis in meters per second. Defaults to 0.
    vy (float | int, optional): Linear velocity along the y-axis in meters per second. Defaults to 0.
    vtheta (float | int, optional): Rotational velocity (around the z-axis) in degrees per second. Defaults to 0.

Raises:
    TypeError: If any of the velocity values (`vx`, `vy`, `vtheta`) are not of type `float` or `int`.

Notes:
    - Use `send_speed_command` after this method to execute the movement.
    - The velocities will be used to command the mobile base for a short duration (0.2 seconds).""",
                parameters={'vx': {'type': 'string', 'description': 'Parameter vx'}, 'vy': {'type': 'string', 'description': 'Parameter vy'}, 'vtheta': {'type': 'string', 'description': 'Parameter vtheta'}},
                required=['vx', 'vy', 'vtheta']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_send_speed_command",
            func=cls.parts_mobile_base_MobileBase_send_speed_command,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_send_speed_command",
                description="""Send the speed command to the mobile base, based on previously set goal speeds.

This method sends the velocity commands for the mobile base that were set with `set_goal_speed`.
The command will be executed for a duration of 200ms, which is predefined at the ROS level of the mobile base code.

Raises:
    ValueError: If the absolute value of `x_vel`, `y_vel`, or `rot_vel` exceeds the configured maximum values.
    Warning: If the mobile base is off, no command is sent, and a warning is logged.

Notes:
    - This method is optimal for sending frequent speed instructions to the mobile base.
    - The goal velocities must be set with `set_goal_speed` before calling this function.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_set_max_xy_goto",
            func=cls.parts_mobile_base_MobileBase_set_max_xy_goto,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_set_max_xy_goto",
                description="""Set the maximum displacement in the x and y directions for the mobile base.

Args:
    value: The maximum displacement value to be set, in meters.""",
                parameters={'value': {'type': 'number', 'description': 'The maximum displacement value to be set, in meters.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="parts_mobile_base_MobileBase_goto_posture",
            func=cls.parts_mobile_base_MobileBase_goto_posture,
            schema=cls.create_tool_schema(
                name="parts_mobile_base_MobileBase_goto_posture",
                description="""Mobile base is not affected by goto_posture. No command is sent.""",
                parameters={'common_posture': {'type': 'string', 'description': 'Parameter common_posture'}, 'duration': {'type': 'number', 'description': 'Parameter duration'}, 'wait': {'type': 'boolean', 'description': 'Parameter wait'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Parameter wait_for_goto_end'}, 'interpolation_mode': {'type': 'string', 'description': 'Parameter interpolation_mode'}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="parts_part_Part___init__",
            func=cls.parts_part_Part___init__,
            schema=cls.create_tool_schema(
                name="parts_part_Part___init__",
                description="""Initialize the Part with common attributes for gRPC communication.

This sets up the communication channel and service stubs for the specified part,
configures the part's unique identifier. It provides the foundation for specific parts of the robot
(Arm, Head, Hand, MobileBase) to be derived from this class.

Args:
    proto_msg: The protobuf message containing configuration details for the part
        (Arm, Head, Hand, or MobileBase).
    grpc_channel: The gRPC channel used to communicate with the service.
    stub: The service stub for the gRPC communication, which could be for Arm, Head,
        Hand, or MobileBase.""",
                parameters={'proto_msg': {'type': 'string', 'description': 'The protobuf message containing configuration details for the part'}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC channel used to communicate with the service.'}, 'stub': {'type': 'string', 'description': 'The service stub for the gRPC communication, which could be for Arm, Head,'}},
                required=['proto_msg', 'grpc_channel', 'stub']
            )
        )
        cls.register_tool(
            name="parts_part_Part_turn_on",
            func=cls.parts_part_Part_turn_on,
            schema=cls.create_tool_schema(
                name="parts_part_Part_turn_on",
                description="""Turn on the part.

This method sets the speed limits to a low value, turns on all motors of the part, and then restores the speed limits
to maximum. It waits for a brief period to ensure the operation is complete.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_part_Part_turn_off",
            func=cls.parts_part_Part_turn_off,
            schema=cls.create_tool_schema(
                name="parts_part_Part_turn_off",
                description="""Turn off the part.

This method turns off all motors of the part and waits for a brief period to ensure the operation is complete.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_part_Part_is_on",
            func=cls.parts_part_Part_is_on,
            schema=cls.create_tool_schema(
                name="parts_part_Part_is_on",
                description="""Check if all actuators of the part are currently on.

Returns:
    True if all actuators are on, otherwise False.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_part_Part_is_off",
            func=cls.parts_part_Part_is_off,
            schema=cls.create_tool_schema(
                name="parts_part_Part_is_off",
                description="""Check if all actuators of the part are currently off.

Returns:
    True if all actuators are off, otherwise False.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_part_Part_audit",
            func=cls.parts_part_Part_audit,
            schema=cls.create_tool_schema(
                name="parts_part_Part_audit",
                description="""Get the audit status of all actuators of the part.

Returns:
    A dictionary where each key is the name of an actuator and the value is its audit status.
    If an error is detected in any actuator, a warning is logged. Otherwise, an informational
    message indicating no errors is logged.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_tripod_Tripod___init__",
            func=cls.parts_tripod_Tripod___init__,
            schema=cls.create_tool_schema(
                name="parts_tripod_Tripod___init__",
                description="""Initialize the Tripod with its initial state and configuration.

This sets up the tripod by assigning its state based on the provided initial values.

Args:
    proto_msg: The protobuf message containing configuration details for the part.
    initial_state: The initial state of the tripod's joints.
    grpc_channel: The gRPC channel used to communicate with the DynamixelMotor service.""",
                parameters={'proto_msg': {'type': 'string', 'description': 'The protobuf message containing configuration details for the part.'}, 'initial_state': {'type': 'string', 'description': "The initial state of the tripod's joints."}, 'grpc_channel': {'type': 'string', 'description': 'The gRPC channel used to communicate with the DynamixelMotor service.'}},
                required=['proto_msg', 'initial_state', 'grpc_channel']
            )
        )
        cls.register_tool(
            name="parts_tripod_Tripod___repr__",
            func=cls.parts_tripod_Tripod___repr__,
            schema=cls.create_tool_schema(
                name="parts_tripod_Tripod___repr__",
                description="""Clean representation of the Tripod.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_tripod_Tripod_height",
            func=cls.parts_tripod_Tripod_height,
            schema=cls.create_tool_schema(
                name="parts_tripod_Tripod_height",
                description="""Get the current height of the robot torso in meters.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_tripod_Tripod_set_height",
            func=cls.parts_tripod_Tripod_set_height,
            schema=cls.create_tool_schema(
                name="parts_tripod_Tripod_set_height",
                description="""Set the height of the tripod.

Args:
    height: The height of the tripod in meters.

Raises:
    TypeError: If the height is not a float or int.""",
                parameters={'height': {'type': 'number', 'description': 'The height of the tripod in meters.'}},
                required=['height']
            )
        )
        cls.register_tool(
            name="parts_tripod_Tripod_reset_height",
            func=cls.parts_tripod_Tripod_reset_height,
            schema=cls.create_tool_schema(
                name="parts_tripod_Tripod_reset_height",
                description="""Reset the height of the tripod to its default position.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="parts_tripod_Tripod_get_limits",
            func=cls.parts_tripod_Tripod_get_limits,
            schema=cls.create_tool_schema(
                name="parts_tripod_Tripod_get_limits",
                description="""Get the limits of the tripod's height.

Returns:
    A tuple containing the minimum and maximum height values.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def parts_arm_Arm___init__(cls, arm_msg, initial_state, grpc_channel, goto_stub) -> Dict[str, Any]:
        """Initialize an Arm instance.
        
        This constructor sets up the arm's gRPC communication and initializes its actuators
        (shoulder, elbow, and wrist). Optionally, a gripper can also be configured.
        
        Args:
            arm_msg: The protobuf message containing the arm's configuration details.
            initial_state: The initial state of the arm's actuators.
            grpc_channel: The gRPC channel used for communication with the arm's server.
            goto_stub: The gRPC stub for controlling goto movements."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm___init__(arm_msg, initial_state, grpc_channel, goto_stub)

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
    def parts_arm_Arm_shoulder(cls, ) -> Dict[str, Any]:
        """Get the shoulder actuator of the arm."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_shoulder()

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
    def parts_arm_Arm_elbow(cls, ) -> Dict[str, Any]:
        """Get the elbow actuator of the arm."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_elbow()

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
    def parts_arm_Arm_wrist(cls, ) -> Dict[str, Any]:
        """Get the wrist actuator of the arm."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_wrist()

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
    def parts_arm_Arm_gripper(cls, ) -> Dict[str, Any]:
        """Get the gripper of the arm, or None if not set."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_gripper()

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
    def parts_arm_Arm___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of an Arm."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm___repr__()

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
    def parts_arm_Arm_turn_on(cls, ) -> Dict[str, Any]:
        """Turn on all motors of the part, making all arm motors stiff.
        
        If a gripper is present, it will also be turned on."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_turn_on()

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
    def parts_arm_Arm_turn_off(cls, ) -> Dict[str, Any]:
        """Turn off all motors of the part, making all arm motors compliant.
        
        If a gripper is present, it will also be turned off."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_turn_off()

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
    def parts_arm_Arm_turn_off_smoothly(cls, ) -> Dict[str, Any]:
        """Gradually reduce the torque limit of all motors over 3 seconds before turning them off.
        
        This function decreases the torque limit in steps until the motors are turned off.
        It then restores the torque limit to its original value."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_turn_off_smoothly()

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
    def parts_arm_Arm_is_on(cls, check_gripper) -> Dict[str, Any]:
        """Check if all actuators of the arm are stiff.
        
        Returns:
            `True` if all actuators of the arm are stiff, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_is_on(check_gripper)

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
    def parts_arm_Arm_is_off(cls, check_gripper) -> Dict[str, Any]:
        """Check if all actuators of the arm are compliant.
        
        Returns:
            `True` if all actuators of the arm are compliant, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_is_off(check_gripper)

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
    def parts_arm_Arm_get_current_positions(cls, degrees) -> Dict[str, Any]:
        """Return the current joint positions of the arm, either in degrees or radians.
        
        Args:
            degrees: Specifies whether the joint positions should be returned in degrees.
                If set to `True`, the positions are returned in degrees; otherwise, they are returned in radians.
                Defaults to `True`.
        
        Returns:
            A list of float values representing the current joint positions of the arm in the
            following order: [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch,
            wrist_yaw]."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_get_current_positions(degrees)

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
    def parts_arm_Arm_forward_kinematics(cls, joints_positions, degrees) -> Dict[str, Any]:
        """Compute the forward kinematics of the arm and return a 4x4 pose matrix.
        
        The pose matrix is expressed in Reachy coordinate system.
        
        Args:
            joints_positions: A list of float values representing the positions of the joints
                in the arm. If not provided, the current robot joints positions are used. Defaults to None.
            degrees: Indicates whether the joint positions are in degrees or radians.
                If `True`, the positions are in degrees; if `False`, in radians. Defaults to True.
        
        Returns:
            A 4x4 pose matrix as a NumPy array, expressed in Reachy coordinate system.
        
        Raises:
            ValueError: If `joints_positions` is provided and its length is not 7.
            ValueError: If no solution is found for the given joint positions."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_forward_kinematics(joints_positions, degrees)

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
    def parts_arm_Arm_inverse_kinematics(cls, target, q0, degrees) -> Dict[str, Any]:
        """Compute a joint configuration to reach a specified target pose for the arm end-effector.
        
        Args:
            target: A 4x4 homogeneous pose matrix representing the target pose in
                Reachy coordinate system, provided as a NumPy array.
            q0: An optional initial joint configuration for the arm. If provided, the
                algorithm will use it as a starting point for finding a solution. Defaults to None.
            degrees: Indicates whether the returned joint angles should be in degrees or radians.
                If `True`, angles are in degrees; if `False`, in radians. Defaults to True.
            round: Number of decimal places to round the computed joint angles to before
                returning. If None, no rounding is performed. Defaults to None.
        
        Returns:
            A list of joint angles representing the solution to reach the target pose, in the following order:
                [shoulder_pitch, shoulder_roll, elbo_yaw, elbow_pitch, wrist.roll, wrist.pitch, wrist.yaw].
        
        Raises:
            ValueError: If the target shape is not (4, 4).
            ValueError: If the length of `q0` is not 7.
            ValueError: If vectorized kinematics is attempted (unsupported).
            ValueError: If no solution is found for the given target."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_inverse_kinematics(target, q0, degrees)

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
    def parts_arm_Arm_goto(cls, target, duration, wait, interpolation_space, interpolation_mode, degrees, q0, arc_direction, secondary_radius) -> Dict[str, Any]:
        """Move the arm to a specified target position, either in joint space or Cartesian space.
        
        This function allows the arm to move to a specified target using either:
        - A list of 7 joint positions, or
        - A 4x4 pose matrix representing the desired end-effector position.
        
        The function also supports an optional initial configuration `q0` for
        computing the inverse kinematics solution when the target is in Cartesian space.
        
        Args:
            target: The target position. It can either be a list of 7 joint values (for joint space)
                    or a 4x4 NumPy array (for Cartesian space).
            duration: The time in seconds for the movement to be completed. Defaults to 2.
            wait: If True, the function waits until the movement is completed before returning.
                    Defaults to False.
            interpolation_space: The space in which the interpolation should be performed. It can
                    be either "joint_space" or "cartesian_space". Defaults to "joint_space".
            interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk",
                    "linear" or "elliptical". Defaults to "minimum_jerk".
            degrees: If True, the joint values in the `target` argument are treated as degrees.
                    Defaults to True.
            q0: An optional list of 7 joint values representing the initial configuration
                    for inverse kinematics. Defaults to None.
            arc_direction: The direction of the arc to be followed during elliptical interpolation.
                    Can be "above", "below", "front", "back", "left" or "right" . Defaults to "above".
            secondary_radius: The secondary radius of the ellipse for elliptical interpolation, in meters.
        
        Returns:
            GoToId: The unique GoToId identifier for the movement command.
        
        Raises:
            TypeError: If the `target` is neither a list nor a pose matrix.
            TypeError: If the `q0` is not a list.
            ValueError: If the `target` list has a length other than 7, or the pose matrix is not
                of shape (4, 4).
            ValueError: If the `q0` list has a length other than 7.
            ValueError: If the `duration` is set to 0."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_goto(target, duration, wait, interpolation_space, interpolation_mode, degrees, q0, arc_direction, secondary_radius)

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
    def parts_arm_Arm_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode, open_gripper) -> Dict[str, Any]:
        """Send all joints to standard positions with optional parameters for duration, waiting, and interpolation mode.
        
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
            open_gripper: If `True`, the gripper will open, if `False`, it stays in its current position.
                Defaults to `False`.
        
        Returns:
            A unique GoToId identifier for this specific movement."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode, open_gripper)

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
    def parts_arm_Arm_get_default_posture_joints(cls, common_posture) -> Dict[str, Any]:
        """Get the list of joint positions for default or elbow_90 poses.
        
        Args:
            common_posture: The name of the posture to retrieve. Can be "default" or "elbow_90".
                Defaults to "default".
        
        Returns:
            A list of joint positions in degrees for the specified posture.
        
        Raises:
            ValueError: If `common_posture` is not "default" or "elbow_90"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_get_default_posture_joints(common_posture)

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
    def parts_arm_Arm_get_default_posture_matrix(cls, common_posture) -> Dict[str, Any]:
        """Get the 4x4 pose matrix in Reachy coordinate system for a default robot posture.
        
        Args:
            common_posture: The posture to retrieve. Can be "default" or "elbow_90".
                Defaults to "default".
        
        Returns:
            The 4x4 homogeneous pose matrix for the specified posture in Reachy coordinate system."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_get_default_posture_matrix(common_posture)

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
    def parts_arm_Arm_get_translation_by(cls, x, y, z, initial_pose, frame) -> Dict[str, Any]:
        """Return a 4x4 matrix representing a pose translated by specified x, y, z values.
        
        The translation is performed in either the robot or gripper coordinate system.
        
        Args:
            x: Translation along the x-axis in meters (forwards direction) to apply
                to the pose matrix.
            y: Translation along the y-axis in meters (left direction) to apply
                to the pose matrix.
            z: Translation along the z-axis in meters (upwards direction) to apply
                to the pose matrix.
            initial_pose: A 4x4 matrix representing the initial pose of the end-effector in Reachy coordinate system,
                expressed as a NumPy array of type `np.float64`.
                If not provided, the current pose of the arm is used. Defaults to `None`.
            frame: The coordinate system in which the translation should be performed.
                Can be either "robot" or "gripper". Defaults to "robot".
        
        Returns:
            A 4x4 pose matrix, expressed in Reachy coordinate system,
            translated by the specified x, y, z values from the initial pose.
        
        Raises:
            ValueError: If the `frame` is not "robot" or "gripper"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_get_translation_by(x, y, z, initial_pose, frame)

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
    def parts_arm_Arm_translate_by(cls, x, y, z, duration, wait, frame, interpolation_space, interpolation_mode, arc_direction, secondary_radius) -> Dict[str, Any]:
        """Create a translation movement for the arm's end effector.
        
        The movement is based on the last sent position or the current position.
        
        Args:
            x: Translation along the x-axis in meters (forwards direction) to apply
                to the pose matrix.
            y: Translation along the y-axis in meters (left direction) to apply
                to the pose matrix.
            z: Translation along the z-axis in meters (vertical direction) to apply
                to the pose matrix.
            duration: Time duration in seconds for the translation movement to be completed.
                Defaults to 2.
            wait: Determines whether the program should wait for the movement to finish before
                returning. If set to `True`, the program waits for the movement to complete before continuing
                execution. Defaults to `False`.
            frame: The coordinate system in which the translation should be performed.
                Can be "robot" or "gripper". Defaults to "robot".
            interpolation_mode: The type of interpolation to be used when moving the arm's
                joints. Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.
        
        Returns:
            The GoToId of the movement command, created using the `goto_from_matrix` method with the
            translated pose computed in the specified frame.
        
        Raises:
            ValueError: If the `frame` is not "robot" or "gripper"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_translate_by(x, y, z, duration, wait, frame, interpolation_space, interpolation_mode, arc_direction, secondary_radius)

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
    def parts_arm_Arm_get_rotation_by(cls, roll, pitch, yaw, initial_pose, degrees, frame) -> Dict[str, Any]:
        """Calculate a new pose matrix by rotating an initial pose matrix by specified roll, pitch, and yaw angles.
        
        The rotation is performed in either the robot or gripper coordinate system.
        
        Args:
            roll: Rotation around the x-axis in the Euler angles representation, specified
                in radians or degrees (based on the `degrees` parameter).
            pitch: Rotation around the y-axis in the Euler angles representation, specified
                in radians or degrees (based on the `degrees` parameter).
            yaw: Rotation around the z-axis in the Euler angles representation, specified
                in radians or degrees (based on the `degrees` parameter).
            initial_pose: A 4x4 matrix representing the initial
                pose of the end-effector, expressed as a NumPy array of type `np.float64`. If not provided,
                the current pose of the arm is used. Defaults to `None`.
            degrees: Specifies whether the rotation angles are provided in degrees. If set to
                `True`, the angles are interpreted as degrees. Defaults to `True`.
            frame: The coordinate system in which the rotation should be performed. Can be
                "robot" or "gripper". Defaults to "robot".
        
        Returns:
            A 4x4 pose matrix, expressed in the Reachy coordinate system, rotated
            by the specified roll, pitch, and yaw angles from the initial pose, in the specified frame.
        
        Raises:
            ValueError: If the `frame` is not "robot" or "gripper"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_get_rotation_by(roll, pitch, yaw, initial_pose, degrees, frame)

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
    def parts_arm_Arm_rotate_by(cls, roll, pitch, yaw, duration, wait, degrees, frame, interpolation_mode) -> Dict[str, Any]:
        """Create a rotation movement for the arm's end effector based on the specified roll, pitch, and yaw angles.
        
        The rotation is performed in either the robot or gripper frame.
        
        Args:
            roll: Rotation around the x-axis in the Euler angles representation, specified
                in radians or degrees (based on the `degrees` parameter).
            pitch: Rotation around the y-axis in the Euler angles representation, specified
                in radians or degrees (based on the `degrees` parameter).
            yaw: Rotation around the z-axis in the Euler angles representation, specified
                in radians or degrees (based on the `degrees` parameter).
            duration: Time duration in seconds for the rotation movement to be completed.
                Defaults to 2.
            wait: Determines whether the program should wait for the movement to finish before
                returning. If set to `True`, the program waits for the movement to complete before continuing
                execution. Defaults to `False`.
            degrees: Specifies whether the rotation angles are provided in degrees. If set to
                `True`, the angles are interpreted as degrees. Defaults to `True`.
            frame: The coordinate system in which the rotation should be performed. Can be
                "robot" or "gripper". Defaults to "robot".
            interpolation_mode: The type of interpolation to be used when moving the arm's
                joints. Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.
        
        Returns:
            The GoToId of the movement command, created by calling the `goto_from_matrix` method with
            the rotated pose computed in the specified frame.
        
        Raises:
            ValueError: If the `frame` is not "robot" or "gripper"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_rotate_by(roll, pitch, yaw, duration, wait, degrees, frame, interpolation_mode)

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
    def parts_arm_Arm_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send goal positions to the arm's joints, including the gripper.
        
        If goal positions have been specified for any joint of the part, sends them to the robot.
        
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'arm')

            # Call the function with parameters
            result = obj.Arm_send_goal_positions(check_positions)

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
    def parts_goto_based_part_IGoToBasedPart___init__(cls, part, goto_stub) -> Dict[str, Any]:
        """Initialize the IGoToBasedPart interface.
        
        Sets up the common attributes needed for handling goto-based movements. This includes
        associating the part with the interface and setting up the gRPC stub for performing
        goto commands.
        
        Args:
            part: The robot part that uses this interface, such as an Arm or Head.
            goto_stub: The gRPC stub used to send goto commands to the robot part."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_part_IGoToBasedPart___init__(part, goto_stub)

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
    def parts_goto_based_part_IGoToBasedPart_get_goto_playing(cls, ) -> Dict[str, Any]:
        """Return the GoToId of the currently playing goto movement on a specific part."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_part_IGoToBasedPart_get_goto_playing()

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
    def parts_goto_based_part_IGoToBasedPart_get_goto_queue(cls, ) -> Dict[str, Any]:
        """Return a list of all GoToIds waiting to be played on a specific part."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_part_IGoToBasedPart_get_goto_queue()

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
    def parts_goto_based_part_IGoToBasedPart_cancel_all_goto(cls, ) -> Dict[str, Any]:
        """Request the cancellation of all playing and waiting goto commands for a specific part.
        
        Returns:
            A GoToAck acknowledging the cancellation of all goto commands."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_part_IGoToBasedPart_cancel_all_goto()

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
    def parts_hand_Hand___init__(cls, hand_msg, grpc_channel, goto_stub) -> Dict[str, Any]:
        """Initialize the Hand component.
        
        Sets up the necessary attributes and configuration for the hand, including the gRPC
        stub and initial state.
        
        Args:
            hand_msg: The Hand_proto object containing the configuration details for the hand.
            grpc_channel: The gRPC channel used to communicate with the hand's gRPC service.
            goto_stub: The gRPC stub for controlling goto movements."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand___init__(hand_msg, grpc_channel, goto_stub)

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
    def parts_hand_Hand_is_on(cls, ) -> Dict[str, Any]:
        """Check if the hand is stiff.
        
        Returns:
            `True` if the hand is on (not compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand_is_on()

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
    def parts_hand_Hand_is_off(cls, ) -> Dict[str, Any]:
        """Check if the hand is compliant.
        
        Returns:
            `True` if the hand is off (compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand_is_off()

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
    def parts_hand_Hand_is_moving(cls, ) -> Dict[str, Any]:
        """Check if the hand is currently moving.
        
        Returns:
            `True` if any joint of the hand is moving, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand_is_moving()

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
    def parts_hand_Hand_open(cls, ) -> Dict[str, Any]:
        """Open the hand.
        
        Raises:
            RuntimeError: If the gripper is off and the open request cannot be sent."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand_open()

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
    def parts_hand_Hand_close(cls, ) -> Dict[str, Any]:
        """Close the hand.
        
        Raises:
            RuntimeError: If the gripper is off and the close request cannot be sent."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand_close()

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
    def parts_hand_Hand_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send the goal positions to the hand's joints.
        
        If any goal position has been specified for any of the gripper's joints, sends them to the robot.
        If the hand is off, the command is not sent.
        
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'hand')

            # Call the function with parameters
            result = obj.Hand_send_goal_positions(check_positions)

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
    def parts_head_Head___init__(cls, head_msg, initial_state, grpc_channel, goto_stub) -> Dict[str, Any]:
        """Initialize the Head component with its actuators.
        
        Sets up the necessary attributes and configuration for the head, including the gRPC
        stubs and initial state.
        
        Args:
            head_msg: The Head_proto object containing the configuration details for the head.
            initial_state: The initial state of the head, represented as a HeadState object.
            grpc_channel: The gRPC channel used to communicate with the head's gRPC service.
            goto_stub: The GoToServiceStub used to handle goto-based movements for the head."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head___init__(head_msg, initial_state, grpc_channel, goto_stub)

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
    def parts_head_Head___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of an Head."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head___repr__()

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
    def parts_head_Head_neck(cls, ) -> Dict[str, Any]:
        """Get the neck actuator of the head."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_neck()

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
    def parts_head_Head_l_antenna(cls, ) -> Dict[str, Any]:
        """Get the left antenna actuator of the head."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_l_antenna()

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
    def parts_head_Head_r_antenna(cls, ) -> Dict[str, Any]:
        """Get the right antenna actuator of the head."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_r_antenna()

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
    def parts_head_Head_get_current_orientation(cls, ) -> Dict[str, Any]:
        """Get the current orientation of the head.
        
        Returns:
            The orientation of the head as a quaternion (w, x, y, z)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_get_current_orientation()

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
    def parts_head_Head_get_current_positions(cls, degrees) -> Dict[str, Any]:
        """Return the current joint positions of the neck.
        
        Returns:
            A list of the current neck joint positions in the order [roll, pitch, yaw]."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_get_current_positions(degrees)

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
    def parts_head_Head_goto(cls, target, duration, wait, interpolation_mode, degrees) -> Dict[str, Any]:
        """Send the neck to a specified orientation.
        
        This method moves the neck either to a given roll-pitch-yaw (RPY) position or to a quaternion orientation.
        
        Args:
            target: The desired orientation for the neck. Can either be:
                - A list of three floats [roll, pitch, yaw] representing the RPY orientation (in degrees if `degrees=True`).
                - A pyQuat object representing a quaternion.
            duration: The time in seconds for the movement to be completed. Defaults to 2.
            wait: If True, the function waits until the movement is completed before returning.
                    Defaults to False.
            interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk"
                    or "linear". Defaults to "minimum_jerk".
            degrees: If True, the RPY values in the `target` argument are treated as degrees.
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
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_goto(target, duration, wait, interpolation_mode, degrees)

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
    def parts_head_Head_look_at(cls, x, y, z, duration, wait, interpolation_mode) -> Dict[str, Any]:
        """Compute and send a neck position to look at a specified point in Reachy's Cartesian space (torso frame).
        
        The (x, y, z) coordinates are expressed in meters, where x is forward, y is left, and z is upward.
        
        Args:
            x: The x-coordinate of the target point.
            y: The y-coordinate of the target point.
            z: The z-coordinate of the target point.
            duration: The time in seconds for the head to look at the point. Defaults to 2.0.
            wait: Whether to wait for the movement to complete before returning. Defaults to False.
            interpolation_mode: The interpolation mode for the movement, either "minimum_jerk" or "linear".
                Defaults to "minimum_jerk".
        
        Returns:
            The unique GoToId associated with the movement command.
        
        Raises:
            ValueError: If the duration is set to 0."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_look_at(x, y, z, duration, wait, interpolation_mode)

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
    def parts_head_Head_rotate_by(cls, roll, pitch, yaw, duration, wait, degrees, frame, interpolation_mode) -> Dict[str, Any]:
        """Rotate the neck by the specified angles.
        
        Args:
            roll: The angle in degrees to rotate around the x-axis (roll). Defaults to 0.
            pitch: The angle in degrees to rotate around the y-axis (pitch). Defaults to 0.
            yaw: The angle in degrees to rotate around the z-axis (yaw). Defaults to 0.
            duration: The time in seconds for the neck to reach the target posture. Defaults to 2.
            wait: Whether to wait for the movement to complete before returning. Defaults to False.
            degrees: Whether the angles are provided in degrees. If True, the angles will be converted to radians.
                Defaults to True.
            frame: The frame of reference for the rotation. Can be either "robot" or "head". Defaults to "robot".
            interpolation_mode: The interpolation mode for the movement, either "minimum_jerk" or "linear".
                Defaults to "minimum_jerk".
        
        
        Raises:
            ValueError: If the frame is not "robot" or "head".
            ValueError: If the duration is set to 0.
            ValueError: If the interpolation mode is not "minimum_jerk" or "linear"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_rotate_by(roll, pitch, yaw, duration, wait, degrees, frame, interpolation_mode)

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
    def parts_head_Head_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode) -> Dict[str, Any]:
        """Send all neck joints to standard positions within the specified duration.
        
        The default posture sets the neck joints to [0, -10, 0] (roll, pitch, yaw).
        
        Args:
            common_posture: The standard positions to which all joints will be sent.
                It can be 'default' or 'elbow_90'. Defaults to 'default'.
            duration: The time in seconds for the neck to reach the target posture. Defaults to 2.
            wait: Whether to wait for the movement to complete before returning. Defaults to False.
            wait_for_goto_end: Whether to wait for all previous goto commands to finish before executing
                the current command. If False, it cancels all ongoing commands. Defaults to True.
            interpolation_mode: The interpolation mode for the movement, either "minimum_jerk" or "linear".
                Defaults to "minimum_jerk".
        
        Returns:
            The unique GoToId associated with the movement command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'head')

            # Call the function with parameters
            result = obj.Head_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode)

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
    def parts_joints_based_part_JointsBasedPart___init__(cls, proto_msg, grpc_channel, stub) -> Dict[str, Any]:
        """Initialize the JointsBasedPart with its common attributes.
        
        Sets up the gRPC communication channel and service stub for controlling the joint-based
        part of the robot, such as an arm or head.
        
        Args:
            proto_msg: A protocol message representing the part's configuration. It can be an
                Arm_proto or Head_proto object.
            grpc_channel: The gRPC channel used to communicate with the corresponding service.
            stub: The service stub for the gRPC communication, which can be an ArmServiceStub or
                HeadServiceStub, depending on the part type."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'joints')

            # Call the function with parameters
            result = obj.based_part_JointsBasedPart___init__(proto_msg, grpc_channel, stub)

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
    def parts_joints_based_part_JointsBasedPart_joints(cls, ) -> Dict[str, Any]:
        """Get all the arm's joints.
        
        Returns:
            A dictionary of all the arm's joints, with joint names as keys and joint objects as values."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'joints')

            # Call the function with parameters
            result = obj.based_part_JointsBasedPart_joints()

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
    def parts_joints_based_part_JointsBasedPart_get_current_positions(cls, ) -> Dict[str, Any]:
        """Get the current positions of all joints.
        
        Returns:
            A list of float values representing the present positions in degrees of the arm's joints."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'joints')

            # Call the function with parameters
            result = obj.based_part_JointsBasedPart_get_current_positions()

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
    def parts_joints_based_part_JointsBasedPart_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send goal positions to the part's joints.
        
        If goal positions have been specified for any joint of the part, sends them to the robot.
        
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'joints')

            # Call the function with parameters
            result = obj.based_part_JointsBasedPart_send_goal_positions(check_positions)

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
    def parts_joints_based_part_JointsBasedPart_set_torque_limits(cls, torque_limit) -> Dict[str, Any]:
        """Set the torque limit as a percentage of the maximum torque for all motors of the part.
        
        Args:
            torque_limit: The desired torque limit as a percentage (0-100) of the maximum torque. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'joints')

            # Call the function with parameters
            result = obj.based_part_JointsBasedPart_set_torque_limits(torque_limit)

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
    def parts_joints_based_part_JointsBasedPart_set_speed_limits(cls, speed_limit) -> Dict[str, Any]:
        """Set the speed limit as a percentage of the maximum speed for all motors of the part.
        
        Args:
            speed_limit: The desired speed limit as a percentage (0-100) of the maximum speed. Can be
                specified as a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'joints')

            # Call the function with parameters
            result = obj.based_part_JointsBasedPart_set_speed_limits(speed_limit)

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
    def parts_mobile_base_MobileBase___init__(cls, mb_msg, initial_state, grpc_channel, goto_stub) -> Dict[str, Any]:
        """Initialize the MobileBase with its gRPC communication and configuration.
        
        This sets up the gRPC communication channel and service stubs for controlling the
        mobile base, initializes the drive and control modes.
        It also sets up the LIDAR safety monitoring.
        
        Args:
            mb_msg: A MobileBase_proto message containing the configuration details for the mobile base.
            initial_state: The initial state of the mobile base, as a MobileBaseState object.
            grpc_channel: The gRPC channel used to communicate with the mobile base service.
            goto_stub: The gRPC service stub for the GoTo service."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase___init__(mb_msg, initial_state, grpc_channel, goto_stub)

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
    def parts_mobile_base_MobileBase___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a mobile base."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase___repr__()

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
    def parts_mobile_base_MobileBase_battery_voltage(cls, ) -> Dict[str, Any]:
        """Return the battery voltage.
        
        The battery should be recharged if the voltage reaches 24.5V or below. If the battery level is low,
        a warning message is logged.
        
        Returns:
            The current battery voltage as a float, rounded to one decimal place."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_battery_voltage()

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
    def parts_mobile_base_MobileBase_odometry(cls, ) -> Dict[str, Any]:
        """Return the odometry of the base.
        
        The odometry includes the x and y positions in meters and theta in degrees, along with the
        velocities in the x, y directions in meters per degrees and the angular velocity in degrees per second.
        
        Returns:
            A dictionary containing the current odometry with keys 'x', 'y', 'theta', 'vx', 'vy', and 'vtheta',
            each rounded to three decimal places."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_odometry()

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
    def parts_mobile_base_MobileBase_last_cmd_vel(cls, ) -> Dict[str, Any]:
        """Return the last command velocity sent to the base.
        
        The velocity includes the x and y components in meters per second and the theta component in degrees per second.
        
        Returns:
            A dictionary containing the last command velocity with keys 'x', 'y', and 'theta',
            each rounded to three decimal places."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_last_cmd_vel()

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
    def parts_mobile_base_MobileBase_is_on(cls, ) -> Dict[str, Any]:
        """Check if the mobile base is currently stiff (not in free-wheel mode).
        
        Returns:
            `True` if the mobile base is not compliant (stiff), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_is_on()

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
    def parts_mobile_base_MobileBase_is_off(cls, ) -> Dict[str, Any]:
        """Check if the mobile base is currently compliant (in free-wheel mode).
        
        Returns:
            True if the mobile base is compliant (in free-wheel mode), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_is_off()

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
    def parts_mobile_base_MobileBase_get_current_odometry(cls, degrees) -> Dict[str, Any]:
        """Get the current odometry of the mobile base in its reference frame.
        
        Args:
            degrees (bool, optional): Whether to return the orientation (`theta` and `vtheta`) in degrees.
                                    Defaults to True.
        
        Returns:
            Dict[str, float]: A dictionary containing the current odometry of the mobile base with:
            - 'x': Position along the x-axis (in meters).
            - 'y': Position along the y-axis (in meters).
            - 'theta': Orientation (in degrees by default, radians if `degrees=False`).
            - 'vx': Linear velocity along the x-axis (in meters per second).
            - 'vy': Linear velocity along the y-axis (in meters per second).
            - 'vtheta': Angular velocity (in degrees per second by default, radians if `degrees=False`)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_get_current_odometry(degrees)

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
    def parts_mobile_base_MobileBase_goto(cls, x, y, theta, wait, degrees, distance_tolerance, angle_tolerance, timeout) -> Dict[str, Any]:
        """Send the mobile base to a specified target position.
        
        The (x, y) coordinates define the position in Cartesian space, and theta specifies the orientation in degrees.
        The zero position is set when the mobile base is started or when the `reset_odometry` method is called. A timeout
        can be provided to avoid the mobile base getting stuck. The tolerance values define the acceptable margins for
        reaching the target position.
        
        Args:
            x: The target x-coordinate in meters.
            y: The target y-coordinate in meters.
            theta: The target orientation in degrees.
            wait: If True, the function waits until the movement is completed before returning.
                    Defaults to False.
            degrees: If True, the theta value and angle_tolerance are treated as degrees.
                    Defaults to True.
            distance_tolerance: Optional; the tolerance to the target position to consider the goto finished, in meters.
            angle_tolerance: Optional; the angle tolerance to the target to consider the goto finished, in meters.
            timeout: Optional; the maximum time allowed to reach the target, in seconds.
        
        Returns:
            GoToId: The unique GoToId identifier for the movement command.
        
        Raises:
            TypeError: If the target is not reached and the mobile base is stopped due to an obstacle."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_goto(x, y, theta, wait, degrees, distance_tolerance, angle_tolerance, timeout)

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
    def parts_mobile_base_MobileBase_translate_by(cls, x, y, wait, distance_tolerance, timeout) -> Dict[str, Any]:
        """Send a target position relative to the current position of the mobile base.
        
        The (x, y) coordinates specify the desired translation in the mobile base's Cartesian space.
        
        Args:
            x: The desired translation along the x-axis in meters.
            y: The desired translation along the y-axis in meters.
            wait:  If True, the function waits until the movement is completed before returning.
            distance_tolerance: Optional; The distance tolerance to the target to consider the goto finished, in meters.
            timeout: An optional timeout for reaching the target position, in seconds.
        
        Returns:
            The GoToId of the movement command, created using the `goto` method."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_translate_by(x, y, wait, distance_tolerance, timeout)

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
    def parts_mobile_base_MobileBase_rotate_by(cls, theta, wait, degrees, angle_tolerance, timeout) -> Dict[str, Any]:
        """Send a target rotation relative to the current rotation of the mobile base.
        
        The theta parameter defines the desired rotation in degrees.
        
        Args:
            theta: The desired rotation in degrees, relative to the current orientation.
            wait: If True, the function waits until the rotation is completed before returning.
            degrees: If True, the theta value and angle_tolerance are treated as degrees, otherwise as radians.
            angle_tolerance: Optional; The angle tolerance to the target to consider the goto finished.
            timeout: An optional timeout for completing the rotation, in seconds."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_rotate_by(theta, wait, degrees, angle_tolerance, timeout)

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
    def parts_mobile_base_MobileBase_reset_odometry(cls, ) -> Dict[str, Any]:
        """Reset the odometry.
        
        This method resets the mobile base's odometry, so that the current position is now (x, y, theta) = (0, 0, 0).
        If any goto is being played, stop the goto and the queued ones."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_reset_odometry()

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
    def parts_mobile_base_MobileBase_set_goal_speed(cls, vx, vy, vtheta) -> Dict[str, Any]:
        """Set the goal speed for the mobile base.
        
        This method sets the target velocities for the mobile base's movement along the x and y axes, as well as
        its rotational speed. The actual movement is executed after calling `send_speed_command`.
        
        Args:
            vx (float | int, optional): Linear velocity along the x-axis in meters per second. Defaults to 0.
            vy (float | int, optional): Linear velocity along the y-axis in meters per second. Defaults to 0.
            vtheta (float | int, optional): Rotational velocity (around the z-axis) in degrees per second. Defaults to 0.
        
        Raises:
            TypeError: If any of the velocity values (`vx`, `vy`, `vtheta`) are not of type `float` or `int`.
        
        Notes:
            - Use `send_speed_command` after this method to execute the movement.
            - The velocities will be used to command the mobile base for a short duration (0.2 seconds)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_set_goal_speed(vx, vy, vtheta)

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
    def parts_mobile_base_MobileBase_send_speed_command(cls, ) -> Dict[str, Any]:
        """Send the speed command to the mobile base, based on previously set goal speeds.
        
        This method sends the velocity commands for the mobile base that were set with `set_goal_speed`.
        The command will be executed for a duration of 200ms, which is predefined at the ROS level of the mobile base code.
        
        Raises:
            ValueError: If the absolute value of `x_vel`, `y_vel`, or `rot_vel` exceeds the configured maximum values.
            Warning: If the mobile base is off, no command is sent, and a warning is logged.
        
        Notes:
            - This method is optimal for sending frequent speed instructions to the mobile base.
            - The goal velocities must be set with `set_goal_speed` before calling this function."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_send_speed_command()

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
    def parts_mobile_base_MobileBase_set_max_xy_goto(cls, value) -> Dict[str, Any]:
        """Set the maximum displacement in the x and y directions for the mobile base.
        
        Args:
            value: The maximum displacement value to be set, in meters."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_set_max_xy_goto(value)

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
    def parts_mobile_base_MobileBase_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode) -> Dict[str, Any]:
        """Mobile base is not affected by goto_posture. No command is sent."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'mobile')

            # Call the function with parameters
            result = obj.base_MobileBase_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode)

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
    def parts_part_Part___init__(cls, proto_msg, grpc_channel, stub) -> Dict[str, Any]:
        """Initialize the Part with common attributes for gRPC communication.
        
        This sets up the communication channel and service stubs for the specified part,
        configures the part's unique identifier. It provides the foundation for specific parts of the robot
        (Arm, Head, Hand, MobileBase) to be derived from this class.
        
        Args:
            proto_msg: The protobuf message containing configuration details for the part
                (Arm, Head, Hand, or MobileBase).
            grpc_channel: The gRPC channel used to communicate with the service.
            stub: The service stub for the gRPC communication, which could be for Arm, Head,
                Hand, or MobileBase."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'part')

            # Call the function with parameters
            result = obj.Part___init__(proto_msg, grpc_channel, stub)

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
    def parts_part_Part_turn_on(cls, ) -> Dict[str, Any]:
        """Turn on the part.
        
        This method sets the speed limits to a low value, turns on all motors of the part, and then restores the speed limits
        to maximum. It waits for a brief period to ensure the operation is complete."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'part')

            # Call the function with parameters
            result = obj.Part_turn_on()

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
    def parts_part_Part_turn_off(cls, ) -> Dict[str, Any]:
        """Turn off the part.
        
        This method turns off all motors of the part and waits for a brief period to ensure the operation is complete."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'part')

            # Call the function with parameters
            result = obj.Part_turn_off()

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
    def parts_part_Part_is_on(cls, ) -> Dict[str, Any]:
        """Check if all actuators of the part are currently on.
        
        Returns:
            True if all actuators are on, otherwise False."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'part')

            # Call the function with parameters
            result = obj.Part_is_on()

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
    def parts_part_Part_is_off(cls, ) -> Dict[str, Any]:
        """Check if all actuators of the part are currently off.
        
        Returns:
            True if all actuators are off, otherwise False."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'part')

            # Call the function with parameters
            result = obj.Part_is_off()

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
    def parts_part_Part_audit(cls, ) -> Dict[str, Any]:
        """Get the audit status of all actuators of the part.
        
        Returns:
            A dictionary where each key is the name of an actuator and the value is its audit status.
            If an error is detected in any actuator, a warning is logged. Otherwise, an informational
            message indicating no errors is logged."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'part')

            # Call the function with parameters
            result = obj.Part_audit()

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
    def parts_tripod_Tripod___init__(cls, proto_msg, initial_state, grpc_channel) -> Dict[str, Any]:
        """Initialize the Tripod with its initial state and configuration.
        
        This sets up the tripod by assigning its state based on the provided initial values.
        
        Args:
            proto_msg: The protobuf message containing configuration details for the part.
            initial_state: The initial state of the tripod's joints.
            grpc_channel: The gRPC channel used to communicate with the DynamixelMotor service."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'tripod')

            # Call the function with parameters
            result = obj.Tripod___init__(proto_msg, initial_state, grpc_channel)

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
    def parts_tripod_Tripod___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of the Tripod."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'tripod')

            # Call the function with parameters
            result = obj.Tripod___repr__()

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
    def parts_tripod_Tripod_height(cls, ) -> Dict[str, Any]:
        """Get the current height of the robot torso in meters."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'tripod')

            # Call the function with parameters
            result = obj.Tripod_height()

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
    def parts_tripod_Tripod_set_height(cls, height) -> Dict[str, Any]:
        """Set the height of the tripod.
        
        Args:
            height: The height of the tripod in meters.
        
        Raises:
            TypeError: If the height is not a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'tripod')

            # Call the function with parameters
            result = obj.Tripod_set_height(height)

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
    def parts_tripod_Tripod_reset_height(cls, ) -> Dict[str, Any]:
        """Reset the height of the tripod to its default position."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'tripod')

            # Call the function with parameters
            result = obj.Tripod_reset_height()

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
    def parts_tripod_Tripod_get_limits(cls, ) -> Dict[str, Any]:
        """Get the limits of the tripod's height.
        
        Returns:
            A tuple containing the minimum and maximum height values."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'tripod')

            # Call the function with parameters
            result = obj.Tripod_get_limits()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
