#!/usr/bin/env python
"""
Connection manager for the Reachy 2 robot.

This module provides functionality for connecting to either a real Reachy robot
or a mock implementation for testing.
"""

import os
import sys
import logging
import traceback
from typing import Any, Dict, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("connection_manager")

# Global robot instance
_REACHY_INSTANCE = None
_CONNECTION_TYPE = None
_CONNECTION_ERROR = None

def connect_to_reachy(
    host: str = "localhost", 
    use_mock: bool = False,
    use_virtual: bool = False,
    mock_visualize: bool = False
) -> Any:
    """
    Connect to a Reachy robot.
    
    Args:
        host: Hostname or IP address of the robot
        use_mock: Whether to use a mock implementation
        use_virtual: Whether to use a virtual robot (for real SDK)
        mock_visualize: Whether to visualize the mock robot
        
    Returns:
        Any: Reachy instance
    """
    global _REACHY_INSTANCE, _CONNECTION_TYPE, _CONNECTION_ERROR
    
    # Return existing instance if already connected
    if _REACHY_INSTANCE is not None:
        logger.info(f"Using existing Reachy connection ({_CONNECTION_TYPE})")
        return _REACHY_INSTANCE
    
    # Reset connection error
    _CONNECTION_ERROR = None
    
    # Determine connection type
    if use_mock:
        _CONNECTION_TYPE = "mock"
        logger.info(f"Connecting to mock Reachy at {host}")
        
        try:
            # Import the mock implementation directly without relying on __init__.py
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Try different import paths
            try:
                from agent.tools.mock_reachy import MockReachy
                logger.info("Imported mock_reachy from agent.tools")
            except ImportError:
                # Try relative import
                from .mock_reachy import MockReachy
                logger.info("Imported mock_reachy from relative import")
            
            # Create mock Reachy instance
            _REACHY_INSTANCE = MockReachy(host=host, use_virtual=True)
            
            # Create visualizer if requested (simplified for demo)
            if mock_visualize:
                logger.info("Mock visualization is enabled but simplified for demo")
            
            logger.info("Connected to mock Reachy")
            
        except ImportError as e:
            error_msg = f"Failed to import mock Reachy: {e}"
            logger.error(error_msg)
            _CONNECTION_ERROR = {
                "type": "import_error",
                "message": error_msg,
                "traceback": traceback.format_exc()
            }
            raise
        except Exception as e:
            error_msg = f"Failed to initialize mock Reachy: {e}"
            logger.error(error_msg)
            _CONNECTION_ERROR = {
                "type": "initialization_error",
                "message": error_msg,
                "traceback": traceback.format_exc()
            }
            raise
        
    else:
        _CONNECTION_TYPE = "real"
        logger.info(f"Connecting to real Reachy at {host} (virtual: {use_virtual})")
        
        try:
            # Import the real SDK
            import reachy2_sdk
            
            # Create Reachy instance
            _REACHY_INSTANCE = reachy2_sdk.ReachySDK(host=host, use_virtual=use_virtual)
            logger.info("Connected to real Reachy")
            
        except ImportError as e:
            error_msg = f"Failed to import Reachy SDK: {e}"
            logger.error(error_msg)
            logger.warning("Falling back to mock implementation")
            _CONNECTION_ERROR = {
                "type": "import_error",
                "message": error_msg,
                "traceback": traceback.format_exc()
            }
            
            # Fall back to mock implementation
            try:
                # Try different import paths
                try:
                    from agent.tools.mock_reachy import MockReachy
                except ImportError:
                    # Try relative import
                    from .mock_reachy import MockReachy
                
                # Create mock Reachy instance
                _REACHY_INSTANCE = MockReachy(host=host, use_virtual=True)
                _CONNECTION_TYPE = "mock (fallback)"
                logger.info("Connected to mock Reachy (fallback)")
                
            except Exception as e:
                error_msg = f"Failed to initialize fallback mock Reachy: {e}"
                logger.error(error_msg)
                _CONNECTION_ERROR = {
                    "type": "fallback_error",
                    "message": error_msg,
                    "traceback": traceback.format_exc()
                }
                raise
                
        except Exception as e:
            error_msg = f"Failed to connect to real Reachy: {e}"
            logger.error(error_msg)
            logger.warning("Falling back to mock implementation")
            _CONNECTION_ERROR = {
                "type": "connection_error",
                "message": error_msg,
                "traceback": traceback.format_exc()
            }
            
            # Fall back to mock implementation
            try:
                # Try different import paths
                try:
                    from agent.tools.mock_reachy import MockReachy
                except ImportError:
                    # Try relative import
                    from .mock_reachy import MockReachy
                
                # Create mock Reachy instance
                _REACHY_INSTANCE = MockReachy(host=host, use_virtual=True)
                _CONNECTION_TYPE = "mock (fallback)"
                logger.info("Connected to mock Reachy (fallback)")
                
            except Exception as e:
                error_msg = f"Failed to initialize fallback mock Reachy: {e}"
                logger.error(error_msg)
                _CONNECTION_ERROR = {
                    "type": "fallback_error",
                    "message": error_msg,
                    "traceback": traceback.format_exc()
                }
                raise
    
    return _REACHY_INSTANCE


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
    
    Returns:
        bool: True if connected to a mock Reachy, False otherwise
    """
    return _CONNECTION_TYPE is not None and _CONNECTION_TYPE.startswith("mock")


def get_connection_info() -> Dict[str, Any]:
    """
    Get information about the current connection.
    
    Returns:
        Dict[str, Any]: Connection information
    """
    info = {
        "connected": _REACHY_INSTANCE is not None,
        "type": _CONNECTION_TYPE,
        "error": _CONNECTION_ERROR
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
    reachy = connect_to_reachy(use_mock=True, mock_visualize=True)
    
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