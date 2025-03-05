#!/usr/bin/env python
"""
Connection manager for the Reachy 2 robot.

This module provides functionality for connecting to a Reachy robot
using the Reachy2 SDK.
"""

import os
import sys
import logging
import traceback
from typing import Any, Dict, Optional, Union

# Add the project root to the path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import REACHY_HOST

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("connection_manager")

# Global robot instance
_REACHY_INSTANCE = None
_CONNECTION_TYPE = None
_CONNECTION_ERROR = None

def connect_to_reachy(
    host: str = None, 
    use_mock: bool = False,
    sdk_port: int = 50051,
    audio_port: int = 50063,
    video_port: int = 50065
) -> Any:
    """
    Connect to a Reachy robot using the Reachy2 SDK.
    
    Args:
        host: Hostname or IP address of the robot
             If None, uses the REACHY_HOST from config
        use_mock: Deprecated, kept for backward compatibility
        sdk_port: The gRPC port for the SDK. Default is 50051.
        audio_port: The gRPC port for audio services. Default is 50063.
        video_port: The gRPC port for video services. Default is 50065.
        
    Returns:
        Any: Reachy instance
    """
    global _REACHY_INSTANCE, _CONNECTION_TYPE, _CONNECTION_ERROR
    
    # Use config values if parameters are not provided
    if host is None:
        host = REACHY_HOST
    
    # Return existing instance if already connected
    if _REACHY_INSTANCE is not None:
        logger.info(f"Using existing Reachy connection ({_CONNECTION_TYPE})")
        return _REACHY_INSTANCE
    
    # Reset connection error
    _CONNECTION_ERROR = None
    
    # If use_mock is True, log a warning
    if use_mock:
        logger.warning("Mock mode is deprecated")
    
    # Set connection type for internal tracking (localhost = virtual, otherwise physical)
    _CONNECTION_TYPE = "virtual" if host == "localhost" else "physical"
    logger.info(f"Connecting to Reachy at {host} (mode: {_CONNECTION_TYPE})")
    
    try:
        # Import the real SDK
        import reachy2_sdk
        
        # Create Reachy instance using only the official parameters
        _REACHY_INSTANCE = reachy2_sdk.ReachySDK(
            host=host,
        )
        logger.info(f"Connected to Reachy SDK (mode: {_CONNECTION_TYPE})")
        
        # Test the connection by getting basic info
        if hasattr(_REACHY_INSTANCE, "get_info"):
            info = _REACHY_INSTANCE.get_info()
            logger.info(f"Reachy info: {info}")
        
        return _REACHY_INSTANCE
        
    except ImportError as e:
        error_msg = f"Failed to import Reachy SDK: {e}"
        logger.error(error_msg)
        _CONNECTION_ERROR = {
            "type": "import_error",
            "message": error_msg,
            "traceback": traceback.format_exc()
        }
        raise ImportError(f"Reachy SDK is required but not installed: {e}")
            
    except Exception as e:
        error_msg = f"Failed to connect to Reachy: {e}"
        logger.error(error_msg)
        _CONNECTION_ERROR = {
            "type": "connection_error",
            "message": error_msg,
            "traceback": traceback.format_exc()
        }
        raise RuntimeError(f"Failed to connect to Reachy: {e}")


def get_reachy() -> Any:
    """
    Get the Reachy instance.
    
    Returns:
        Any: Reachy instance
    
    Raises:
        RuntimeError: If Reachy is not connected
    """
    if _REACHY_INSTANCE is None:
        error_msg = "Reachy is not connected. Call connect_to_reachy() first."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    return _REACHY_INSTANCE


def disconnect_reachy() -> None:
    """Disconnect from the Reachy robot."""
    global _REACHY_INSTANCE, _CONNECTION_TYPE
    
    if _REACHY_INSTANCE is not None:
        logger.info(f"Disconnecting from Reachy ({_CONNECTION_TYPE})")
        
        try:
            # Call close() method if it exists
            if hasattr(_REACHY_INSTANCE, "close"):
                _REACHY_INSTANCE.close()
        except Exception as e:
            logger.error(f"Error disconnecting from Reachy: {e}")
        
        _REACHY_INSTANCE = None
        _CONNECTION_TYPE = None


def is_mock() -> bool:
    """
    Check if the current connection is to a mock Reachy.
    This is kept for backward compatibility but will always return False.
    
    Returns:
        bool: Always False as mock mode is deprecated
    """
    return False


def is_virtual() -> bool:
    """
    Check if the current connection is to a virtual Reachy.
    
    Returns:
        bool: True if connected to localhost, False otherwise
    """
    return _CONNECTION_TYPE == "virtual"


def get_connection_info() -> Dict[str, Any]:
    """
    Get information about the current connection.
    
    Returns:
        Dict[str, Any]: Connection information
    """
    info = {
        "connected": _REACHY_INSTANCE is not None,
        "type": _CONNECTION_TYPE,
        "error": _CONNECTION_ERROR,
        "virtual": _CONNECTION_TYPE == "virtual"
    }
    
    # Add robot info if available
    if _REACHY_INSTANCE is not None and hasattr(_REACHY_INSTANCE, "get_info"):
        try:
            info["robot"] = _REACHY_INSTANCE.get_info()
        except Exception as e:
            logger.error(f"Error getting robot info: {e}")
            info["robot_error"] = str(e)
    
    return info


if __name__ == "__main__":
    # Example usage
    reachy = connect_to_reachy(host="localhost")
    
    # Get some information
    info = reachy.get_info()
    print(f"Robot info: {info}")
    
    # Get arm positions
    left_positions = reachy.arms["left"].get_current_positions()
    print(f"Left arm positions: {left_positions}")
    
    # Move an arm
    reachy.arms["right"].goto([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4], wait=True)
    
    # Look at a point
    reachy.head.look_at(0.5, 0.3, 0.2, wait=True)
    
    # Take a camera frame
    frame = reachy.cameras["teleop"].get_frame()
    print(f"Frame shape: {frame.shape}")
    
    # Disconnect
    disconnect_reachy() 