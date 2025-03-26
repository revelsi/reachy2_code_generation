#!/usr/bin/env python
"""
utils tools for the Reachy 2 robot.

This module provides tools for interacting with the utils module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class UtilsTools(BaseTool):
    """Tools for interacting with the utils module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all utils tools."""
        cls.register_tool(
            name="utils_utils_convert_to_radians",
            func=cls.utils_utils_convert_to_radians,
            schema=cls.create_tool_schema(
                name="utils_utils_convert_to_radians",
                description="""Convert a list of angles from degrees to radians.

Args:
    angles_list: A list of angles in degrees to convert to radians.

Returns:
    A list of angles converted to radians.""",
                parameters={'angles_list': {'type': 'array', 'description': 'A list of angles in degrees to convert to radians.'}},
                required=['angles_list']
            )
        )
        cls.register_tool(
            name="utils_utils_convert_to_degrees",
            func=cls.utils_utils_convert_to_degrees,
            schema=cls.create_tool_schema(
                name="utils_utils_convert_to_degrees",
                description="""Convert a list of angles from radians to degrees.

Args:
    angles_list: A list of angles in radians to convert to degrees.

Returns:
    A list of angles converted to degrees.""",
                parameters={'angles_list': {'type': 'array', 'description': 'A list of angles in radians to convert to degrees.'}},
                required=['angles_list']
            )
        )
        cls.register_tool(
            name="utils_utils_list_to_arm_position",
            func=cls.utils_utils_list_to_arm_position,
            schema=cls.create_tool_schema(
                name="utils_utils_list_to_arm_position",
                description="""Convert a list of joint positions to an ArmPosition message, considering whether the positions are in degrees or radians.

Args:
    positions: A list of float values representing joint positions. The list should contain 7 values
        in the following order: [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch,wrist_yaw].
    degrees: A flag indicating whether the input joint positions are in degrees. If set to `True`,
        the input positions are in degrees. Defaults to `True`.

Returns:
    An ArmPosition message containing the shoulder position, elbow position, and wrist position
    based on the input list of joint positions.""",
                parameters={'positions': {'type': 'array', 'description': 'A list of float values representing joint positions. The list should contain 7 values'}, 'degrees': {'type': 'boolean', 'description': 'A flag indicating whether the input joint positions are in degrees. If set to `True`,'}},
                required=['positions', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_arm_position_to_list",
            func=cls.utils_utils_arm_position_to_list,
            schema=cls.create_tool_schema(
                name="utils_utils_arm_position_to_list",
                description="""Convert an ArmPosition message to a list of joint positions, with an option to return the result in degrees.

Args:
    arm_pos: An ArmPosition message containing shoulder, elbow, and wrist positions.
    degrees: Specifies whether the joint positions should be returned in degrees. If set to `True`,
        the positions are converted to degrees. Defaults to `True`.

Returns:
    A list of joint positions based on the ArmPosition, returned in the following order:
    [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch, wrist_yaw].""",
                parameters={'arm_pos': {'type': 'string', 'description': 'An ArmPosition message containing shoulder, elbow, and wrist positions.'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the joint positions should be returned in degrees. If set to `True`,'}},
                required=['arm_pos', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_ext_euler_angles_to_list",
            func=cls.utils_utils_ext_euler_angles_to_list,
            schema=cls.create_tool_schema(
                name="utils_utils_ext_euler_angles_to_list",
                description="""Convert an ExtEulerAngles 3D rotation message to a list of joint positions.

Args:
    euler_angles: An ExtEulerAngles object representing a 3D rotation message.
    degrees: Specifies whether the output should be in degrees. If set to `True`, the function
        converts the angles to degrees before returning the list. Defaults to `True`.

Returns:
    A list of joint positions representing the Euler angles in the order [roll, pitch, yaw].""",
                parameters={'euler_angles': {'type': 'string', 'description': 'An ExtEulerAngles object representing a 3D rotation message.'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the output should be in degrees. If set to `True`, the function'}},
                required=['euler_angles', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_get_grpc_interpolation_mode",
            func=cls.utils_utils_get_grpc_interpolation_mode,
            schema=cls.create_tool_schema(
                name="utils_utils_get_grpc_interpolation_mode",
                description="""Convert a given interpolation mode string to a corresponding GoToInterpolation object.

Args:
    interpolation_mode: A string representing the type of interpolation to be used. It can be either
        "minimum_jerk", "linear" or "elliptical".

Returns:
    An instance of the GoToInterpolation class with the interpolation type set based on the input
    interpolation_mode string.

Raises:
    ValueError: If the interpolation_mode is not "minimum_jerk", "linear" or "elliptical".""",
                parameters={'interpolation_mode': {'type': 'string', 'description': 'A string representing the type of interpolation to be used. It can be either'}},
                required=['interpolation_mode']
            )
        )
        cls.register_tool(
            name="utils_utils_get_grpc_interpolation_space",
            func=cls.utils_utils_get_grpc_interpolation_space,
            schema=cls.create_tool_schema(
                name="utils_utils_get_grpc_interpolation_space",
                description="""Convert a given interpolation space string to a corresponding GoToInterpolationSpace object.

Args:
    interpolation_space: A string representing the interpolation space to be used. It can be either
        "joint_space" or "cartesian_space".

Returns:
    An instance of the GoToInterpolationSpace class with the interpolation type set based on the input
    interpolation_space string.

Raises:
    ValueError: If the interpolation_space is not "joint_space" or "cartesian_space".""",
                parameters={'interpolation_space': {'type': 'string', 'description': 'A string representing the interpolation space to be used. It can be either'}},
                required=['interpolation_space']
            )
        )
        cls.register_tool(
            name="utils_utils_get_interpolation_mode",
            func=cls.utils_utils_get_interpolation_mode,
            schema=cls.create_tool_schema(
                name="utils_utils_get_interpolation_mode",
                description="""Convert an interpolation mode enum to a string representation.

Args:
    interpolation_mode: The interpolation mode given as InterpolationMode. The supported interpolation
        modes are MINIMUM_JERK, LINEAR and ELLIPTICAL.

Returns:
    A string representing the interpolation mode based on the input interpolation_mode. Returns
    "minimum_jerk" if the mode is InterpolationMode.MINIMUM_JERK, "linear" if it is
    InterpolationMode.LINEAR, and "elliptical" if it is InterpolationMode.ELLIPTICAL.

Raises:
    ValueError: If the interpolation_mode is not InterpolationMode.MINIMUM_JERK, InterpolationMode.LINEAR
    or InterpolationMode.ELLIPTICAL.""",
                parameters={'interpolation_mode': {'type': 'string', 'description': 'The interpolation mode given as InterpolationMode. The supported interpolation'}},
                required=['interpolation_mode']
            )
        )
        cls.register_tool(
            name="utils_utils_get_interpolation_space",
            func=cls.utils_utils_get_interpolation_space,
            schema=cls.create_tool_schema(
                name="utils_utils_get_interpolation_space",
                description="""Convert an interpolation space enum to a string representation.

Args:
    interpolation_space: The interpolation space given as InterpolationSpace. The supported interpolation
        modes are JOINT_SPACE and CARTESIAN_SPACE.

Returns:
    A string representing the interpolation mode based on the input interpolation_space. Returns
    "joint_space" if the mode is InterpolationSpace.JOINT_SPACE, and "cartesian_space" if it is
    InterpolationSpace.CARTESIAN_SPACE.

Raises:
    ValueError: If the interpolation_space is not InterpolationSpace.JOINT_SPACE or InterpolationSpace.CARTESIAN_SPACE.""",
                parameters={'interpolation_space': {'type': 'string', 'description': 'The interpolation space given as InterpolationSpace. The supported interpolation'}},
                required=['interpolation_space']
            )
        )
        cls.register_tool(
            name="utils_utils_get_grpc_arc_direction",
            func=cls.utils_utils_get_grpc_arc_direction,
            schema=cls.create_tool_schema(
                name="utils_utils_get_grpc_arc_direction",
                description="""Convert a given arc direction string to a corresponding ArcDirection object.

Args:
    arc_direction: A string representing the direction of the arc. It can be one of the following options:
        "above", "below", "front", "back", "right", or "left".

Returns:
    An instance of the ArcDirection class with the direction set based on the input arc_direction string.

Raises:
    ValueError: If the arc_direction is not one of "above", "below", "front", "back", "right", or "left".""",
                parameters={'arc_direction': {'type': 'string', 'description': 'A string representing the direction of the arc. It can be one of the following options:'}},
                required=['arc_direction']
            )
        )
        cls.register_tool(
            name="utils_utils_get_arc_direction",
            func=cls.utils_utils_get_arc_direction,
            schema=cls.create_tool_schema(
                name="utils_utils_get_arc_direction",
                description="""Convert an arc direction enum to a string representation.

Args:
    arc_direction: The arc direction given as ArcDirection. The supported arc directions are ABOVE, BELOW, FRONT,
        BACK, RIGHT, and LEFT.

Returns:
    A string representing the arc direction based on the input arc_direction. Returns "above" if the direction is
    ArcDirection.ABOVE, "below" if it is ArcDirection.BELOW, "front" if it is ArcDirection.FRONT, "back" if it is
    ArcDirection.BACK, "right" if it is ArcDirection.RIGHT, and "left" if it is ArcDirection.LEFT.

Raises:
    ValueError: If the arc_direction is not ArcDirection.ABOVE, ArcDirection.BELOW, ArcDirection.FRONT, ArcDirection.BACK,
    ArcDirection.RIGHT, or ArcDirection.LEFT.""",
                parameters={'arc_direction': {'type': 'string', 'description': 'The arc direction given as ArcDirection. The supported arc directions are ABOVE, BELOW, FRONT,'}},
                required=['arc_direction']
            )
        )
        cls.register_tool(
            name="utils_utils_decompose_matrix",
            func=cls.utils_utils_decompose_matrix,
            schema=cls.create_tool_schema(
                name="utils_utils_decompose_matrix",
                description="""Decompose a homogeneous 4x4 matrix into rotation (represented as a quaternion) and translation components.

Args:
    matrix: A homogeneous 4x4 matrix represented as a NumPy array of type np.float64.

Returns:
    A tuple containing a Quaternion representing the rotation component and a NumPy array
    representing the translation component of the input matrix.""",
                parameters={'matrix': {'type': 'string', 'description': 'A homogeneous 4x4 matrix represented as a NumPy array of type np.float64.'}},
                required=['matrix']
            )
        )
        cls.register_tool(
            name="utils_utils_recompose_matrix",
            func=cls.utils_utils_recompose_matrix,
            schema=cls.create_tool_schema(
                name="utils_utils_recompose_matrix",
                description="""Recompose a homogeneous 4x4 matrix from rotation (quaternion) and translation components.

Args:
    rotation: A 3x3 rotation matrix represented as a NumPy array of type np.float64.
    translation: A vector representing the displacement in space, containing the x, y, and z
        components of the translation vector.

Returns:
    A homogeneous 4x4 matrix composed from the provided rotation and translation components.""",
                parameters={'rotation': {'type': 'string', 'description': 'A 3x3 rotation matrix represented as a NumPy array of type np.float64.'}, 'translation': {'type': 'string', 'description': 'A vector representing the displacement in space, containing the x, y, and z'}},
                required=['rotation', 'translation']
            )
        )
        cls.register_tool(
            name="utils_utils_matrix_from_euler_angles",
            func=cls.utils_utils_matrix_from_euler_angles,
            schema=cls.create_tool_schema(
                name="utils_utils_matrix_from_euler_angles",
                description="""Create a 4x4 homogeneous rotation matrix from roll, pitch, and yaw angles, with an option to input angles in degrees.

Args:
    roll: The rotation angle around the x-axis in the Euler angles representation.
    pitch: The rotation angle around the y-axis in the Euler angles representation.
    yaw: The rotation angle around the z-axis in the Euler angles representation.
    degrees: Specifies whether the input angles (roll, pitch, yaw) are in degrees. If set to `True`,
        the input angles are expected to be in degrees. Defaults to `True`.

Returns:
    A 4x4 homogeneous rotation matrix created from the input roll, pitch, and yaw angles.""",
                parameters={'roll': {'type': 'number', 'description': 'The rotation angle around the x-axis in the Euler angles representation.'}, 'pitch': {'type': 'number', 'description': 'The rotation angle around the y-axis in the Euler angles representation.'}, 'yaw': {'type': 'number', 'description': 'The rotation angle around the z-axis in the Euler angles representation.'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the input angles (roll, pitch, yaw) are in degrees. If set to `True`,'}},
                required=['roll', 'pitch', 'yaw', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_get_pose_matrix",
            func=cls.utils_utils_get_pose_matrix,
            schema=cls.create_tool_schema(
                name="utils_utils_get_pose_matrix",
                description="""Create a 4x4 pose matrix from a position vector and "roll, pitch, yaw" angles (rotation).

Args:
    position: A list of size 3 representing the requested position of the end effector in the Reachy coordinate system.
    rotation: A list of size 3 representing the requested orientation of the end effector in the Reachy coordinate system.
        The rotation is given as intrinsic angles, executed in roll, pitch, yaw order.
    degrees: Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.
        If set to `False`, they are interpreted as radians. Defaults to `True`.

Returns:
    The constructed 4x4 pose matrix.

Raises:
    TypeError: If `position` is not a list of floats or integers.
    TypeError: If `rotation` is not a list of floats or integers.
    ValueError: If the length of `position` is not 3.
    ValueError: If the length of `rotation` is not 3.""",
                parameters={'position': {'type': 'array', 'description': 'A list of size 3 representing the requested position of the end effector in the Reachy coordinate system.'}, 'rotation': {'type': 'array', 'description': 'A list of size 3 representing the requested orientation of the end effector in the Reachy coordinate system.'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.'}},
                required=['position', 'rotation', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_quaternion_from_euler_angles",
            func=cls.utils_utils_quaternion_from_euler_angles,
            schema=cls.create_tool_schema(
                name="utils_utils_quaternion_from_euler_angles",
                description="""Convert Euler angles (intrinsic XYZ order) to a quaternion using the pyquaternion library.

Args:
    roll (float): Rotation angle around the X-axis (roll), in degrees by default.
    pitch (float): Rotation angle around the Y-axis (pitch), in degrees by default.
    yaw (float): Rotation angle around the Z-axis (yaw), in degrees by default.
    degrees (bool): If True, the input angles are interpreted as degrees. If False, they are
        interpreted as radians. Defaults to True.

Returns:
    Quaternion: The quaternion representing the combined rotation in 3D space.""",
                parameters={'roll': {'type': 'number', 'description': 'Parameter roll'}, 'pitch': {'type': 'number', 'description': 'Parameter pitch'}, 'yaw': {'type': 'number', 'description': 'Parameter yaw'}, 'degrees': {'type': 'boolean', 'description': 'Parameter degrees'}},
                required=['roll', 'pitch', 'yaw', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_rotate_in_self",
            func=cls.utils_utils_rotate_in_self,
            schema=cls.create_tool_schema(
                name="utils_utils_rotate_in_self",
                description="""Return a new homogeneous 4x4 pose matrix that is the input matrix rotated in itself.

Args:
    frame: The input frame, given as a 4x4 homogeneous matrix.
    rotation: A list of size 3 representing the rotation to be applied. The rotation is given as intrinsic angles,
        executed in roll, pitch, yaw order.
    degrees: Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.
        If set to `False`, they are interpreted as radians. Defaults to `True`.

Returns:
    A new 4x4 homogeneous matrix after applying the specified rotation.""",
                parameters={'frame': {'type': 'string', 'description': 'The input frame, given as a 4x4 homogeneous matrix.'}, 'rotation': {'type': 'array', 'description': 'A list of size 3 representing the rotation to be applied. The rotation is given as intrinsic angles,'}, 'degrees': {'type': 'boolean', 'description': 'Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.'}},
                required=['frame', 'rotation', 'degrees']
            )
        )
        cls.register_tool(
            name="utils_utils_translate_in_self",
            func=cls.utils_utils_translate_in_self,
            schema=cls.create_tool_schema(
                name="utils_utils_translate_in_self",
                description="""Return a new homogeneous 4x4 pose matrix that is the input frame translated along its own axes.

Args:
    frame: The input frame, given as a 4x4 homogeneous matrix.
    translation: A list of size 3 representing the translation to be applied, given as [x, y, z].

Returns:
    A new homogeneous 4x4 pose matrix after translating the input frame along its own axes.""",
                parameters={'frame': {'type': 'string', 'description': 'The input frame, given as a 4x4 homogeneous matrix.'}, 'translation': {'type': 'array', 'description': 'A list of size 3 representing the translation to be applied, given as [x, y, z].'}},
                required=['frame', 'translation']
            )
        )
        cls.register_tool(
            name="utils_utils_invert_affine_transformation_matrix",
            func=cls.utils_utils_invert_affine_transformation_matrix,
            schema=cls.create_tool_schema(
                name="utils_utils_invert_affine_transformation_matrix",
                description="""Invert a 4x4 homogeneous transformation matrix.

The function computes the inverse by transposing the rotation component and adjusting the translation component.

Args:
    matrix: A 4x4 NumPy array representing a homogeneous transformation matrix.

Returns:
    A new 4x4 homogeneous matrix that is the inverse of the input matrix.

Raises:
    ValueError: If the input matrix is not 4x4.""",
                parameters={'matrix': {'type': 'string', 'description': 'A 4x4 NumPy array representing a homogeneous transformation matrix.'}},
                required=['matrix']
            )
        )
        cls.register_tool(
            name="utils_utils_get_normal_vector",
            func=cls.utils_utils_get_normal_vector,
            schema=cls.create_tool_schema(
                name="utils_utils_get_normal_vector",
                description="""Calculate a normal vector to a given vector based on a specified direction.

Args:
    vector: A vector [x, y, z] in 3D space.
    arc_direction: The desired direction for the normal vector. It can be one of the following options:
        'above', 'below', 'front', 'back', 'right', or 'left'.

Returns:
    The normal vector [x, y, z] to the given vector in the specified direction. Returns `None` if the
    normal vector cannot be computed or if the vector is in the requested arc_direction.

Raises:
    ValueError: If the arc_direction is not one of 'above', 'below', 'front', 'back', 'right', or 'left'.""",
                parameters={'vector': {'type': 'string', 'description': 'A vector [x, y, z] in 3D space.'}, 'arc_direction': {'type': 'string', 'description': 'The desired direction for the normal vector. It can be one of the following options:'}},
                required=['vector', 'arc_direction']
            )
        )
        cls.register_tool(
            name="utils_custom_dict_CustomDict___repr__",
            func=cls.utils_custom_dict_CustomDict___repr__,
            schema=cls.create_tool_schema(
                name="utils_custom_dict_CustomDict___repr__",
                description="""Clean representation of the CustomDict.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_goto_request",
            func=cls.utils_goto_based_element_process_goto_request,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_goto_request",
                description="""Process the response from a goto request and return a SimplifiedRequest object.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_arm_cartesian_goal",
            func=cls.utils_goto_based_element_process_arm_cartesian_goal,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_arm_cartesian_goal",
                description="""Process the response from a goto request containing an arm cartesian goal.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_arm_joint_goal",
            func=cls.utils_goto_based_element_process_arm_joint_goal,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_arm_joint_goal",
                description="""Process the response from a goto request containing an arm joint goal.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_neck_joint_goal",
            func=cls.utils_goto_based_element_process_neck_joint_goal,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_neck_joint_goal",
                description="""Process the response from a goto request containing a neck joint goal.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_antenna_joint_goal",
            func=cls.utils_goto_based_element_process_antenna_joint_goal,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_antenna_joint_goal",
                description="""Process the response from a goto request containing an antenna joint goal.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_hand_joint_goal",
            func=cls.utils_goto_based_element_process_hand_joint_goal,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_hand_joint_goal",
                description="""Process the response from a goto request containing a hand joint goal.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_process_odometry_goal",
            func=cls.utils_goto_based_element_process_odometry_goal,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_process_odometry_goal",
                description="""Process the response from a goto request containing an odometry goal.""",
                parameters={'response': {'type': 'string', 'description': 'Parameter response'}},
                required=['response']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_build_simplified_joints_request",
            func=cls.utils_goto_based_element_build_simplified_joints_request,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_build_simplified_joints_request",
                description="""Build a SimplifiedRequest object from a dictionary of joints request details.""",
                parameters={'request_dict': {'type': 'object', 'description': 'Parameter request_dict'}},
                required=['request_dict']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_build_simplified_odometry_request",
            func=cls.utils_goto_based_element_build_simplified_odometry_request,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_build_simplified_odometry_request",
                description="""Build a SimplifiedRequest object from a dictionary of odomztry request details.""",
                parameters={'request_dict': {'type': 'object', 'description': 'Parameter request_dict'}},
                required=['request_dict']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_IGoToBasedElement___init__",
            func=cls.utils_goto_based_element_IGoToBasedElement___init__,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_IGoToBasedElement___init__",
                description="""Initialize the IGoToBasedElement interface.

Sets up the common attributes needed for handling goto-based movements. This includes
associating the component with the interface and setting up the gRPC stub for performing
goto commands.

Args:
    element_id: The robot component or part that uses this interface.
    goto_stub: The gRPC stub used to send goto commands to the robot element.""",
                parameters={'element_id': {'type': 'string', 'description': 'The robot component or part that uses this interface.'}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub used to send goto commands to the robot element.'}},
                required=['element_id', 'goto_stub']
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_IGoToBasedElement_get_goto_playing",
            func=cls.utils_goto_based_element_IGoToBasedElement_get_goto_playing,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_IGoToBasedElement_get_goto_playing",
                description="""Return the GoToId of the currently playing goto movement on a specific element.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_IGoToBasedElement_get_goto_queue",
            func=cls.utils_goto_based_element_IGoToBasedElement_get_goto_queue,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_IGoToBasedElement_get_goto_queue",
                description="""Return a list of all GoToIds waiting to be played on a specific element.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_IGoToBasedElement_cancel_all_goto",
            func=cls.utils_goto_based_element_IGoToBasedElement_cancel_all_goto,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_IGoToBasedElement_cancel_all_goto",
                description="""Request the cancellation of all playing and waiting goto commands for a specific element.

Returns:
    A GoToAck acknowledging the cancellation of all goto commands.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="utils_goto_based_element_IGoToBasedElement_goto_posture",
            func=cls.utils_goto_based_element_IGoToBasedElement_goto_posture,
            schema=cls.create_tool_schema(
                name="utils_goto_based_element_IGoToBasedElement_goto_posture",
                description="""Send all joints to standard positions with optional parameters for duration, waiting, and interpolation mode.""",
                parameters={'common_posture': {'type': 'string', 'description': 'Parameter common_posture'}, 'duration': {'type': 'number', 'description': 'Parameter duration'}, 'wait': {'type': 'boolean', 'description': 'Parameter wait'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Parameter wait_for_goto_end'}, 'interpolation_mode': {'type': 'string', 'description': 'Parameter interpolation_mode'}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode']
            )
        )

    @classmethod
    def utils_utils_convert_to_radians(cls, angles_list) -> Dict[str, Any]:
        """Convert a list of angles from degrees to radians.
        
        Args:
            angles_list: A list of angles in degrees to convert to radians.
        
        Returns:
            A list of angles converted to radians."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.convert_to_radians(angles_list)

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
    def utils_utils_convert_to_degrees(cls, angles_list) -> Dict[str, Any]:
        """Convert a list of angles from radians to degrees.
        
        Args:
            angles_list: A list of angles in radians to convert to degrees.
        
        Returns:
            A list of angles converted to degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.convert_to_degrees(angles_list)

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
    def utils_utils_list_to_arm_position(cls, positions, degrees) -> Dict[str, Any]:
        """Convert a list of joint positions to an ArmPosition message, considering whether the positions are in degrees or radians.
        
        Args:
            positions: A list of float values representing joint positions. The list should contain 7 values
                in the following order: [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch,wrist_yaw].
            degrees: A flag indicating whether the input joint positions are in degrees. If set to `True`,
                the input positions are in degrees. Defaults to `True`.
        
        Returns:
            An ArmPosition message containing the shoulder position, elbow position, and wrist position
            based on the input list of joint positions."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.list_to_arm_position(positions, degrees)

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
    def utils_utils_arm_position_to_list(cls, arm_pos, degrees) -> Dict[str, Any]:
        """Convert an ArmPosition message to a list of joint positions, with an option to return the result in degrees.
        
        Args:
            arm_pos: An ArmPosition message containing shoulder, elbow, and wrist positions.
            degrees: Specifies whether the joint positions should be returned in degrees. If set to `True`,
                the positions are converted to degrees. Defaults to `True`.
        
        Returns:
            A list of joint positions based on the ArmPosition, returned in the following order:
            [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch, wrist_yaw]."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.arm_position_to_list(arm_pos, degrees)

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
    def utils_utils_ext_euler_angles_to_list(cls, euler_angles, degrees) -> Dict[str, Any]:
        """Convert an ExtEulerAngles 3D rotation message to a list of joint positions.
        
        Args:
            euler_angles: An ExtEulerAngles object representing a 3D rotation message.
            degrees: Specifies whether the output should be in degrees. If set to `True`, the function
                converts the angles to degrees before returning the list. Defaults to `True`.
        
        Returns:
            A list of joint positions representing the Euler angles in the order [roll, pitch, yaw]."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.ext_euler_angles_to_list(euler_angles, degrees)

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
    def utils_utils_get_grpc_interpolation_mode(cls, interpolation_mode) -> Dict[str, Any]:
        """Convert a given interpolation mode string to a corresponding GoToInterpolation object.
        
        Args:
            interpolation_mode: A string representing the type of interpolation to be used. It can be either
                "minimum_jerk", "linear" or "elliptical".
        
        Returns:
            An instance of the GoToInterpolation class with the interpolation type set based on the input
            interpolation_mode string.
        
        Raises:
            ValueError: If the interpolation_mode is not "minimum_jerk", "linear" or "elliptical"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_grpc_interpolation_mode(interpolation_mode)

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
    def utils_utils_get_grpc_interpolation_space(cls, interpolation_space) -> Dict[str, Any]:
        """Convert a given interpolation space string to a corresponding GoToInterpolationSpace object.
        
        Args:
            interpolation_space: A string representing the interpolation space to be used. It can be either
                "joint_space" or "cartesian_space".
        
        Returns:
            An instance of the GoToInterpolationSpace class with the interpolation type set based on the input
            interpolation_space string.
        
        Raises:
            ValueError: If the interpolation_space is not "joint_space" or "cartesian_space"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_grpc_interpolation_space(interpolation_space)

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
    def utils_utils_get_interpolation_mode(cls, interpolation_mode) -> Dict[str, Any]:
        """Convert an interpolation mode enum to a string representation.
        
        Args:
            interpolation_mode: The interpolation mode given as InterpolationMode. The supported interpolation
                modes are MINIMUM_JERK, LINEAR and ELLIPTICAL.
        
        Returns:
            A string representing the interpolation mode based on the input interpolation_mode. Returns
            "minimum_jerk" if the mode is InterpolationMode.MINIMUM_JERK, "linear" if it is
            InterpolationMode.LINEAR, and "elliptical" if it is InterpolationMode.ELLIPTICAL.
        
        Raises:
            ValueError: If the interpolation_mode is not InterpolationMode.MINIMUM_JERK, InterpolationMode.LINEAR
            or InterpolationMode.ELLIPTICAL."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_interpolation_mode(interpolation_mode)

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
    def utils_utils_get_interpolation_space(cls, interpolation_space) -> Dict[str, Any]:
        """Convert an interpolation space enum to a string representation.
        
        Args:
            interpolation_space: The interpolation space given as InterpolationSpace. The supported interpolation
                modes are JOINT_SPACE and CARTESIAN_SPACE.
        
        Returns:
            A string representing the interpolation mode based on the input interpolation_space. Returns
            "joint_space" if the mode is InterpolationSpace.JOINT_SPACE, and "cartesian_space" if it is
            InterpolationSpace.CARTESIAN_SPACE.
        
        Raises:
            ValueError: If the interpolation_space is not InterpolationSpace.JOINT_SPACE or InterpolationSpace.CARTESIAN_SPACE."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_interpolation_space(interpolation_space)

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
    def utils_utils_get_grpc_arc_direction(cls, arc_direction) -> Dict[str, Any]:
        """Convert a given arc direction string to a corresponding ArcDirection object.
        
        Args:
            arc_direction: A string representing the direction of the arc. It can be one of the following options:
                "above", "below", "front", "back", "right", or "left".
        
        Returns:
            An instance of the ArcDirection class with the direction set based on the input arc_direction string.
        
        Raises:
            ValueError: If the arc_direction is not one of "above", "below", "front", "back", "right", or "left"."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_grpc_arc_direction(arc_direction)

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
    def utils_utils_get_arc_direction(cls, arc_direction) -> Dict[str, Any]:
        """Convert an arc direction enum to a string representation.
        
        Args:
            arc_direction: The arc direction given as ArcDirection. The supported arc directions are ABOVE, BELOW, FRONT,
                BACK, RIGHT, and LEFT.
        
        Returns:
            A string representing the arc direction based on the input arc_direction. Returns "above" if the direction is
            ArcDirection.ABOVE, "below" if it is ArcDirection.BELOW, "front" if it is ArcDirection.FRONT, "back" if it is
            ArcDirection.BACK, "right" if it is ArcDirection.RIGHT, and "left" if it is ArcDirection.LEFT.
        
        Raises:
            ValueError: If the arc_direction is not ArcDirection.ABOVE, ArcDirection.BELOW, ArcDirection.FRONT, ArcDirection.BACK,
            ArcDirection.RIGHT, or ArcDirection.LEFT."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_arc_direction(arc_direction)

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
    def utils_utils_decompose_matrix(cls, matrix) -> Dict[str, Any]:
        """Decompose a homogeneous 4x4 matrix into rotation (represented as a quaternion) and translation components.
        
        Args:
            matrix: A homogeneous 4x4 matrix represented as a NumPy array of type np.float64.
        
        Returns:
            A tuple containing a Quaternion representing the rotation component and a NumPy array
            representing the translation component of the input matrix."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.decompose_matrix(matrix)

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
    def utils_utils_recompose_matrix(cls, rotation, translation) -> Dict[str, Any]:
        """Recompose a homogeneous 4x4 matrix from rotation (quaternion) and translation components.
        
        Args:
            rotation: A 3x3 rotation matrix represented as a NumPy array of type np.float64.
            translation: A vector representing the displacement in space, containing the x, y, and z
                components of the translation vector.
        
        Returns:
            A homogeneous 4x4 matrix composed from the provided rotation and translation components."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.recompose_matrix(rotation, translation)

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
    def utils_utils_matrix_from_euler_angles(cls, roll, pitch, yaw, degrees) -> Dict[str, Any]:
        """Create a 4x4 homogeneous rotation matrix from roll, pitch, and yaw angles, with an option to input angles in degrees.
        
        Args:
            roll: The rotation angle around the x-axis in the Euler angles representation.
            pitch: The rotation angle around the y-axis in the Euler angles representation.
            yaw: The rotation angle around the z-axis in the Euler angles representation.
            degrees: Specifies whether the input angles (roll, pitch, yaw) are in degrees. If set to `True`,
                the input angles are expected to be in degrees. Defaults to `True`.
        
        Returns:
            A 4x4 homogeneous rotation matrix created from the input roll, pitch, and yaw angles."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.matrix_from_euler_angles(roll, pitch, yaw, degrees)

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
    def utils_utils_get_pose_matrix(cls, position, rotation, degrees) -> Dict[str, Any]:
        """Create a 4x4 pose matrix from a position vector and "roll, pitch, yaw" angles (rotation).
        
        Args:
            position: A list of size 3 representing the requested position of the end effector in the Reachy coordinate system.
            rotation: A list of size 3 representing the requested orientation of the end effector in the Reachy coordinate system.
                The rotation is given as intrinsic angles, executed in roll, pitch, yaw order.
            degrees: Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.
                If set to `False`, they are interpreted as radians. Defaults to `True`.
        
        Returns:
            The constructed 4x4 pose matrix.
        
        Raises:
            TypeError: If `position` is not a list of floats or integers.
            TypeError: If `rotation` is not a list of floats or integers.
            ValueError: If the length of `position` is not 3.
            ValueError: If the length of `rotation` is not 3."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_pose_matrix(position, rotation, degrees)

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
    def utils_utils_quaternion_from_euler_angles(cls, roll, pitch, yaw, degrees) -> Dict[str, Any]:
        """Convert Euler angles (intrinsic XYZ order) to a quaternion using the pyquaternion library.
        
        Args:
            roll (float): Rotation angle around the X-axis (roll), in degrees by default.
            pitch (float): Rotation angle around the Y-axis (pitch), in degrees by default.
            yaw (float): Rotation angle around the Z-axis (yaw), in degrees by default.
            degrees (bool): If True, the input angles are interpreted as degrees. If False, they are
                interpreted as radians. Defaults to True.
        
        Returns:
            Quaternion: The quaternion representing the combined rotation in 3D space."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.quaternion_from_euler_angles(roll, pitch, yaw, degrees)

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
    def utils_utils_rotate_in_self(cls, frame, rotation, degrees) -> Dict[str, Any]:
        """Return a new homogeneous 4x4 pose matrix that is the input matrix rotated in itself.
        
        Args:
            frame: The input frame, given as a 4x4 homogeneous matrix.
            rotation: A list of size 3 representing the rotation to be applied. The rotation is given as intrinsic angles,
                executed in roll, pitch, yaw order.
            degrees: Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.
                If set to `False`, they are interpreted as radians. Defaults to `True`.
        
        Returns:
            A new 4x4 homogeneous matrix after applying the specified rotation."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.rotate_in_self(frame, rotation, degrees)

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
    def utils_utils_translate_in_self(cls, frame, translation) -> Dict[str, Any]:
        """Return a new homogeneous 4x4 pose matrix that is the input frame translated along its own axes.
        
        Args:
            frame: The input frame, given as a 4x4 homogeneous matrix.
            translation: A list of size 3 representing the translation to be applied, given as [x, y, z].
        
        Returns:
            A new homogeneous 4x4 pose matrix after translating the input frame along its own axes."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.translate_in_self(frame, translation)

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
    def utils_utils_invert_affine_transformation_matrix(cls, matrix) -> Dict[str, Any]:
        """Invert a 4x4 homogeneous transformation matrix.
        
        The function computes the inverse by transposing the rotation component and adjusting the translation component.
        
        Args:
            matrix: A 4x4 NumPy array representing a homogeneous transformation matrix.
        
        Returns:
            A new 4x4 homogeneous matrix that is the inverse of the input matrix.
        
        Raises:
            ValueError: If the input matrix is not 4x4."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.invert_affine_transformation_matrix(matrix)

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
    def utils_utils_get_normal_vector(cls, vector, arc_direction) -> Dict[str, Any]:
        """Calculate a normal vector to a given vector based on a specified direction.
        
        Args:
            vector: A vector [x, y, z] in 3D space.
            arc_direction: The desired direction for the normal vector. It can be one of the following options:
                'above', 'below', 'front', 'back', 'right', or 'left'.
        
        Returns:
            The normal vector [x, y, z] to the given vector in the specified direction. Returns `None` if the
            normal vector cannot be computed or if the vector is in the requested arc_direction.
        
        Raises:
            ValueError: If the arc_direction is not one of 'above', 'below', 'front', 'back', 'right', or 'left'."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = reachy.utils

            # Call the function with parameters
            result = obj.get_normal_vector(vector, arc_direction)

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
    def utils_custom_dict_CustomDict___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of the CustomDict."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'custom')

            # Call the function with parameters
            result = obj.dict_CustomDict___repr__()

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
    def utils_goto_based_element_process_goto_request(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request and return a SimplifiedRequest object."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_goto_request(response)

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
    def utils_goto_based_element_process_arm_cartesian_goal(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request containing an arm cartesian goal."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_arm_cartesian_goal(response)

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
    def utils_goto_based_element_process_arm_joint_goal(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request containing an arm joint goal."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_arm_joint_goal(response)

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
    def utils_goto_based_element_process_neck_joint_goal(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request containing a neck joint goal."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_neck_joint_goal(response)

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
    def utils_goto_based_element_process_antenna_joint_goal(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request containing an antenna joint goal."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_antenna_joint_goal(response)

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
    def utils_goto_based_element_process_hand_joint_goal(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request containing a hand joint goal."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_hand_joint_goal(response)

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
    def utils_goto_based_element_process_odometry_goal(cls, response) -> Dict[str, Any]:
        """Process the response from a goto request containing an odometry goal."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_process_odometry_goal(response)

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
    def utils_goto_based_element_build_simplified_joints_request(cls, request_dict) -> Dict[str, Any]:
        """Build a SimplifiedRequest object from a dictionary of joints request details."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_build_simplified_joints_request(request_dict)

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
    def utils_goto_based_element_build_simplified_odometry_request(cls, request_dict) -> Dict[str, Any]:
        """Build a SimplifiedRequest object from a dictionary of odomztry request details."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_build_simplified_odometry_request(request_dict)

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
    def utils_goto_based_element_IGoToBasedElement___init__(cls, element_id, goto_stub) -> Dict[str, Any]:
        """Initialize the IGoToBasedElement interface.
        
        Sets up the common attributes needed for handling goto-based movements. This includes
        associating the component with the interface and setting up the gRPC stub for performing
        goto commands.
        
        Args:
            element_id: The robot component or part that uses this interface.
            goto_stub: The gRPC stub used to send goto commands to the robot element."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_IGoToBasedElement___init__(element_id, goto_stub)

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
    def utils_goto_based_element_IGoToBasedElement_get_goto_playing(cls, ) -> Dict[str, Any]:
        """Return the GoToId of the currently playing goto movement on a specific element."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_IGoToBasedElement_get_goto_playing()

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
    def utils_goto_based_element_IGoToBasedElement_get_goto_queue(cls, ) -> Dict[str, Any]:
        """Return a list of all GoToIds waiting to be played on a specific element."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_IGoToBasedElement_get_goto_queue()

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
    def utils_goto_based_element_IGoToBasedElement_cancel_all_goto(cls, ) -> Dict[str, Any]:
        """Request the cancellation of all playing and waiting goto commands for a specific element.
        
        Returns:
            A GoToAck acknowledging the cancellation of all goto commands."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_IGoToBasedElement_cancel_all_goto()

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
    def utils_goto_based_element_IGoToBasedElement_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode) -> Dict[str, Any]:
        """Send all joints to standard positions with optional parameters for duration, waiting, and interpolation mode."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'goto')

            # Call the function with parameters
            result = obj.based_element_IGoToBasedElement_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
