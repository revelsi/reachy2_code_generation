#!/usr/bin/env python
# Generated tool implementations for orbita module
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


def orbita_utils_to_position(internal_pos: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert an internal angular value in radians to a value in degrees.

Args:
    internal_pos: The internal angular value in radians.

Returns:
    The corresponding angular value in degrees.
    
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
        result = getattr(obj, "to_position")(internal_pos)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def orbita_utils_to_internal_position(pos: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Convert an angular value in degrees to a value in radians.

The server expects values in radians, so conversion is necessary.

Args:
    pos: The angular value in degrees.

Returns:
    The corresponding value in radians.

Raises:
    TypeError: If the provided value is not of type int or float.
    
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
        result = getattr(obj, "to_internal_position")(pos)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def orbita_utils_unwrapped_pid_value(value: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Unwrap the internal PID value from a gRPC protobuf object to a Python value.

Args:
    value: The gRPC protobuf object containing the PID values.

Returns:
    A tuple representing the unwrapped PID gains (p, i, d).
    
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
        result = getattr(obj, "unwrapped_pid_value")(value)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def orbita_utils_wrapped_proto_value(value: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Wrap a simple Python value to the corresponding gRPC protobuf type.

Args:
    value: The value to be wrapped, which can be a bool, float, or int.

Returns:
    The corresponding gRPC protobuf object (BoolValue, FloatValue, or UInt32Value).

Raises:
    TypeError: If the provided value is not a supported type.
    
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
        result = getattr(obj, "wrapped_proto_value")(value)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def orbita_utils_wrapped_pid_value(value: Any, host: str = "localhost") -> Dict[str, Any]:
    """
    Wrap a simple Python value to the corresponding gRPC protobuf type.

Args:
    value: The value to be wrapped, which can be a bool, float, or int.

Returns:
    The corresponding gRPC protobuf object (BoolValue, FloatValue, or UInt32Value).

Raises:
    TypeError: If the provided value is not a supported type.
    
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
        result = getattr(obj, "wrapped_pid_value")(value)

        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
