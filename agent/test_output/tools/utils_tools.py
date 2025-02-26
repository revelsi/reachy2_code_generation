#!/usr/bin/env python
# Generated tool implementations for utils module
from typing import Dict, Any, List, Optional, Union
from reachy2_sdk import ReachySDK

# Connection management
_reachy_instance = None

def get_reachy_connection(host: str = "localhost") -> ReachySDK:
    """
    Get or create a Reachy SDK connection.
    
    Args:
        host: Hostname or IP address of the Reachy robot.
        
    Returns:
        ReachySDK: Reachy SDK instance.
    """
    global _reachy_instance
    if _reachy_instance is None or not _reachy_instance.is_connected():
        _reachy_instance = ReachySDK(host=host)
    return _reachy_instance


def utils_utils_convert_to_radians(angles_list: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert a list of angles from degrees to radians.

Args:
    angles_list: A list of angles in degrees to convert to radians.

Returns:
    A list of angles converted to radians.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "convert_to_radians")(angles_list)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_convert_to_degrees(angles_list: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert a list of angles from radians to degrees.

Args:
    angles_list: A list of angles in radians to convert to degrees.

Returns:
    A list of angles converted to degrees.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "convert_to_degrees")(angles_list)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_list_to_arm_position(positions: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert a list of joint positions to an ArmPosition message, considering whether the positions are in degrees or radians.

Args:
    positions: A list of float values representing joint positions. The list should contain 7 values
        in the following order: [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch,wrist_yaw].
    degrees: A flag indicating whether the input joint positions are in degrees. If set to `True`,
        the input positions are in degrees. Defaults to `True`.

Returns:
    An ArmPosition message containing the shoulder position, elbow position, and wrist position
    based on the input list of joint positions.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "list_to_arm_position")(positions, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_arm_position_to_list(arm_pos: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert an ArmPosition message to a list of joint positions, with an option to return the result in degrees.

Args:
    arm_pos: An ArmPosition message containing shoulder, elbow, and wrist positions.
    degrees: Specifies whether the joint positions should be returned in degrees. If set to `True`,
        the positions are converted to degrees. Defaults to `True`.

Returns:
    A list of joint positions based on the ArmPosition, returned in the following order:
    [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_pitch, wrist_roll, wrist_pitch, wrist_yaw].
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "arm_position_to_list")(arm_pos, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_ext_euler_angles_to_list(euler_angles: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert an ExtEulerAngles 3D rotation message to a list of joint positions.

Args:
    euler_angles: An ExtEulerAngles object representing a 3D rotation message.
    degrees: Specifies whether the output should be in degrees. If set to `True`, the function
        converts the angles to degrees before returning the list. Defaults to `True`.

Returns:
    A list of joint positions representing the Euler angles in the order [roll, pitch, yaw].
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "ext_euler_angles_to_list")(euler_angles, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_get_grpc_interpolation_mode(interpolation_mode: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert a given interpolation mode string to a corresponding GoToInterpolation object.

Args:
    interpolation_mode: A string representing the type of interpolation to be used. It can be either
        "minimum_jerk" or "linear".

Returns:
    An instance of the GoToInterpolation class with the interpolation type set based on the input
    interpolation_mode string.

Raises:
    ValueError: If the interpolation_mode is not "minimum_jerk" or "linear".
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "get_grpc_interpolation_mode")(interpolation_mode)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_get_interpolation_mode(interpolation_mode: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert an interpolation mode enum to a string representation.

Args:
    interpolation_mode: The interpolation mode given as InterpolationMode. The supported interpolation
        modes are MINIMUM_JERK and LINEAR.

Returns:
    A string representing the interpolation mode based on the input interpolation_mode. Returns
    "minimum_jerk" if the mode is InterpolationMode.MINIMUM_JERK, and "linear" if it is
    InterpolationMode.LINEAR.

Raises:
    ValueError: If the interpolation_mode is not InterpolationMode.MINIMUM_JERK or InterpolationMode.LINEAR.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "get_interpolation_mode")(interpolation_mode)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_decompose_matrix(matrix: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Decompose a homogeneous 4x4 matrix into rotation (represented as a quaternion) and translation components.

Args:
    matrix: A homogeneous 4x4 matrix represented as a NumPy array of type np.float64.

Returns:
    A tuple containing a Quaternion representing the rotation component and a NumPy array
    representing the translation component of the input matrix.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "decompose_matrix")(matrix)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_recompose_matrix(rotation: Any, translation: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Recompose a homogeneous 4x4 matrix from rotation (quaternion) and translation components.

Args:
    rotation: A 3x3 rotation matrix represented as a NumPy array of type np.float64.
    translation: A vector representing the displacement in space, containing the x, y, and z
        components of the translation vector.

Returns:
    A homogeneous 4x4 matrix composed from the provided rotation and translation components.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "recompose_matrix")(rotation, translation)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_matrix_from_euler_angles(roll: Any, pitch: Any, yaw: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Create a 4x4 homogeneous rotation matrix from roll, pitch, and yaw angles, with an option to input angles in degrees.

Args:
    roll: The rotation angle around the x-axis in the Euler angles representation.
    pitch: The rotation angle around the y-axis in the Euler angles representation.
    yaw: The rotation angle around the z-axis in the Euler angles representation.
    degrees: Specifies whether the input angles (roll, pitch, yaw) are in degrees. If set to `True`,
        the input angles are expected to be in degrees. Defaults to `True`.

Returns:
    A 4x4 homogeneous rotation matrix created from the input roll, pitch, and yaw angles.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "matrix_from_euler_angles")(roll, pitch, yaw, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_get_pose_matrix(position: Any, rotation: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Create a 4x4 pose matrix from a position vector and "roll, pitch, yaw" angles (rotation).

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
    ValueError: If the length of `rotation` is not 3.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "get_pose_matrix")(position, rotation, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_quaternion_from_euler_angles(roll: Any, pitch: Any, yaw: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert Euler angles (intrinsic XYZ order) to a quaternion using the pyquaternion library.

Args:
    roll (float): Rotation angle around the X-axis (roll), in degrees by default.
    pitch (float): Rotation angle around the Y-axis (pitch), in degrees by default.
    yaw (float): Rotation angle around the Z-axis (yaw), in degrees by default.
    degrees (bool): If True, the input angles are interpreted as degrees. If False, they are
        interpreted as radians. Defaults to True.

Returns:
    Quaternion: The quaternion representing the combined rotation in 3D space.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "quaternion_from_euler_angles")(roll, pitch, yaw, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_rotate_in_self(frame: Any, rotation: Any, degrees: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Return a new homogeneous 4x4 pose matrix that is the input matrix rotated in itself.

Args:
    frame: The input frame, given as a 4x4 homogeneous matrix.
    rotation: A list of size 3 representing the rotation to be applied. The rotation is given as intrinsic angles,
        executed in roll, pitch, yaw order.
    degrees: Specifies whether the input angles are in degrees. If set to `True`, the angles are interpreted as degrees.
        If set to `False`, they are interpreted as radians. Defaults to `True`.

Returns:
    A new 4x4 homogeneous matrix after applying the specified rotation.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "rotate_in_self")(frame, rotation, degrees)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_translate_in_self(frame: Any, translation: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Return a new homogeneous 4x4 pose matrix that is the input frame translated along its own axes.

Args:
    frame: The input frame, given as a 4x4 homogeneous matrix.
    translation: A list of size 3 representing the translation to be applied, given as [x, y, z].

Returns:
    A new homogeneous 4x4 pose matrix after translating the input frame along its own axes.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "translate_in_self")(frame, translation)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_invert_affine_transformation_matrix(matrix: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Invert a 4x4 homogeneous transformation matrix.

The function computes the inverse by transposing the rotation component and adjusting the translation component.

Args:
    matrix: A 4x4 NumPy array representing a homogeneous transformation matrix.

Returns:
    A new 4x4 homogeneous matrix that is the inverse of the input matrix.

Raises:
    ValueError: If the input matrix is not 4x4.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "invert_affine_transformation_matrix")(matrix)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def utils_utils_get_normal_vector(vector: Any, arc_direction: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Calculate a normal vector to a given vector based on a specified direction.

Args:
    vector: A vector [x, y, z] in 3D space.
    arc_direction: The desired direction for the normal vector. It can be one of the following options:
        'above', 'below', 'front', 'back', 'right', or 'left'.

Returns:
    The normal vector [x, y, z] to the given vector in the specified direction. Returns `None` if the
    normal vector cannot be computed or if the vector is in the requested arc_direction.

Raises:
    ValueError: If the arc_direction is not one of 'above', 'below', 'front', 'back', 'right', or 'left'.
    
    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        reachy = get_reachy_connection(host)
        
        # Navigate to the correct object
        obj = reachy
        for part in module_path.split(".")[1:]:  # Skip 'reachy2_sdk'
            obj = getattr(obj, part)
            
        # Call the method
        result = getattr(obj, "get_normal_vector")(vector, arc_direction)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
