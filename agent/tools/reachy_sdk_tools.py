#!/usr/bin/env python
"""
reachy_sdk tools for the Reachy 2 robot.

This module provides tools for interacting with the reachy_sdk module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class ReachySdkTools(BaseTool):
    """Tools for interacting with the reachy_sdk module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all reachy_sdk tools."""
        cls.register_tool(
            name="reachy_sdk_ReachySDK___new__",
            func=cls.reachy_sdk_ReachySDK___new__,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK___new__",
                description="""Ensure only one connected instance per IP is created.""",
                parameters={'cls': {'type': 'string', 'description': 'Parameter cls'}, 'host': {'type': 'string', 'description': 'Parameter host'}},
                required=['cls', 'host']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK___init__",
            func=cls.reachy_sdk_ReachySDK___init__,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK___init__",
                description="""Initialize a connection to the robot.

Args:
    host: The IP address or hostname of the robot.
    sdk_port: The gRPC port for the SDK. Default is 50051.
    audio_port: The gRPC port for audio services. Default is 50063.
    video_port: The gRPC port for video services. Default is 50065.""",
                parameters={'host': {'type': 'string', 'description': 'The IP address or hostname of the robot.'}, 'sdk_port': {'type': 'integer', 'description': 'The gRPC port for the SDK. Default is 50051.'}, 'audio_port': {'type': 'integer', 'description': 'The gRPC port for audio services. Default is 50063.'}, 'video_port': {'type': 'integer', 'description': 'The gRPC port for video services. Default is 50065.'}},
                required=['host', 'sdk_port', 'audio_port', 'video_port']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_connect",
            func=cls.reachy_sdk_ReachySDK_connect,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_connect",
                description="""Connects the SDK to the robot.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_disconnect",
            func=cls.reachy_sdk_ReachySDK_disconnect,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_disconnect",
                description="""Disconnect the SDK from the robot's server.

Args:
    lost_connection: If `True`, indicates that the connection was lost unexpectedly.""",
                parameters={'lost_connection': {'type': 'boolean', 'description': 'If `True`, indicates that the connection was lost unexpectedly.'}},
                required=['lost_connection']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK___repr__",
            func=cls.reachy_sdk_ReachySDK___repr__,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK___repr__",
                description="""Clean representation of a Reachy.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_info",
            func=cls.reachy_sdk_ReachySDK_info,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_info",
                description="""Get ReachyInfo if connected.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_head",
            func=cls.reachy_sdk_ReachySDK_head,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_head",
                description="""Get Reachy's head.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_r_arm",
            func=cls.reachy_sdk_ReachySDK_r_arm,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_r_arm",
                description="""Get Reachy's right arm.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_l_arm",
            func=cls.reachy_sdk_ReachySDK_l_arm,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_l_arm",
                description="""Get Reachy's left arm.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_mobile_base",
            func=cls.reachy_sdk_ReachySDK_mobile_base,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_mobile_base",
                description="""Get Reachy's mobile base.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_tripod",
            func=cls.reachy_sdk_ReachySDK_tripod,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_tripod",
                description="""Get Reachy's fixed tripod.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_joints",
            func=cls.reachy_sdk_ReachySDK_joints,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_joints",
                description="""Return a dictionary of all joints of the robot.

The dictionary keys are the joint names, and the values are the corresponding OrbitaJoint objects.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK__actuators",
            func=cls.reachy_sdk_ReachySDK__actuators,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK__actuators",
                description="""Return a dictionary of all actuators of the robot.

The dictionary keys are the actuator names, and the values are the corresponding actuator objects.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_is_connected",
            func=cls.reachy_sdk_ReachySDK_is_connected,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_is_connected",
                description="""Check if the SDK is connected to the robot.

Returns:
    `True` if connected, `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_cameras",
            func=cls.reachy_sdk_ReachySDK_cameras,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_cameras",
                description="""Get the camera manager if available and connected.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_get_update_timestamp",
            func=cls.reachy_sdk_ReachySDK_get_update_timestamp,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_get_update_timestamp",
                description="""Returns the timestamp (ns) of the last update.

The timestamp is generated by ROS running on Reachy.

Returns:
    timestamp (int) in nanoseconds.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_audit",
            func=cls.reachy_sdk_ReachySDK_audit,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_audit",
                description="""Return the audit status of all enabled parts of the robot.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_turn_on",
            func=cls.reachy_sdk_ReachySDK_turn_on,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_turn_on",
                description="""Activate all motors of the robot's parts if all of them are not already turned on.

Returns:
    `True` if successful, `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_turn_off",
            func=cls.reachy_sdk_ReachySDK_turn_off,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_turn_off",
                description="""Turn all motors of enabled parts off.

All enabled parts' motors will then be compliant.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_turn_off_smoothly",
            func=cls.reachy_sdk_ReachySDK_turn_off_smoothly,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_turn_off_smoothly",
                description="""Turn all motors of robot parts off.

Arm torques are reduced during 3 seconds, then all parts' motors will be compliant.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_is_on",
            func=cls.reachy_sdk_ReachySDK_is_on,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_is_on",
                description="""Check if all actuators of Reachy parts are on (stiff).

Returns:
    `True` if all are stiff, `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_is_off",
            func=cls.reachy_sdk_ReachySDK_is_off,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_is_off",
                description="""Check if all actuators of Reachy parts are off (compliant).

Returns:
    `True` if all are compliant, `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_reset_default_limits",
            func=cls.reachy_sdk_ReachySDK_reset_default_limits,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_reset_default_limits",
                description="""Set back speed and torque limits of all parts to maximum value (100).""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_goto_posture",
            func=cls.reachy_sdk_ReachySDK_goto_posture,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_goto_posture",
                description="""Move the robot to a predefined posture.

Args:
    common_posture: The name of the posture. It can be 'default' or 'elbow_90'. Defaults to 'default'.
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
    A GoToHomeId containing movement GoToIds for each part.""",
                parameters={'common_posture': {'type': 'string', 'description': "The name of the posture. It can be 'default' or 'elbow_90'. Defaults to 'default'."}, 'duration': {'type': 'number', 'description': 'The time duration in seconds for the robot to move to the specified posture.'}, 'wait': {'type': 'boolean', 'description': 'Determines whether the program should wait for the movement to finish before'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Specifies whether commands will be sent to a part immediately or'}, 'interpolation_mode': {'type': 'string', 'description': "The type of interpolation used when moving the arm's joints."}, 'open_gripper': {'type': 'boolean', 'description': 'If `True`, the gripper will open, if `False`, it stays in its current position.'}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode', 'open_gripper']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_is_goto_finished",
            func=cls.reachy_sdk_ReachySDK_is_goto_finished,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_is_goto_finished",
                description="""Check if a goto command has completed.

Args:
    goto_id: The unique GoToId of the goto command.

Returns:
    `True` if the command is complete, `False` otherwise.""",
                parameters={'goto_id': {'type': 'string', 'description': 'The unique GoToId of the goto command.'}},
                required=['goto_id']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_get_goto_request",
            func=cls.reachy_sdk_ReachySDK_get_goto_request,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_get_goto_request",
                description="""Retrieve the details of a goto command based on its GoToId.

Args:
    goto_id: The ID of the goto command for which details are requested.

Returns:
    A `SimplifiedRequest` object containing the part name, joint goal positions
    (in degrees), movement duration, and interpolation mode.
    Returns `None` if the robot is not connected or if the `goto_id` is invalid.

Raises:
    TypeError: If `goto_id` is not an instance of `GoToId`.
    ValueError: If `goto_id` is -1, indicating an invalid command.""",
                parameters={'goto_id': {'type': 'string', 'description': 'The ID of the goto command for which details are requested.'}},
                required=['goto_id']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_cancel_goto_by_id",
            func=cls.reachy_sdk_ReachySDK_cancel_goto_by_id,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_cancel_goto_by_id",
                description="""Request the cancellation of a specific goto command based on its GoToId.

Args:
    goto_id: The ID of the goto command to cancel.

Returns:
    A `GoToAck` object indicating whether the cancellation was acknowledged.
    If the robot is not connected, returns None.

Raises:
    TypeError: If `goto_id` is not an instance of `GoToId`.""",
                parameters={'goto_id': {'type': 'string', 'description': 'The ID of the goto command to cancel.'}},
                required=['goto_id']
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_cancel_all_goto",
            func=cls.reachy_sdk_ReachySDK_cancel_all_goto,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_cancel_all_goto",
                description="""Cancel all active goto commands.

Returns:
     A `GoToAck` object indicating whether the cancellation was acknowledged.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="reachy_sdk_ReachySDK_send_goal_positions",
            func=cls.reachy_sdk_ReachySDK_send_goal_positions,
            schema=cls.create_tool_schema(
                name="reachy_sdk_ReachySDK_send_goal_positions",
                description="""Send the goal positions to the robot.

If goal positions have been specified for any joint of the robot, sends them to the robot.

Args :
    check_positions: A boolean indicating whether to check the positions after sending the command.
        Defaults to True.""",
                parameters={'check_positions': {'type': 'boolean', 'description': 'A boolean indicating whether to check the positions after sending the command.'}},
                required=['check_positions']
            )
        )

    @classmethod
    def reachy_sdk_ReachySDK___new__(cls, host) -> Dict[str, Any]:
        """Ensure only one connected instance per IP is created."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK___new__(host)

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
    def reachy_sdk_ReachySDK___init__(cls, host, sdk_port, audio_port, video_port) -> Dict[str, Any]:
        """Initialize a connection to the robot.
        
        Args:
            host: The IP address or hostname of the robot.
            sdk_port: The gRPC port for the SDK. Default is 50051.
            audio_port: The gRPC port for audio services. Default is 50063.
            video_port: The gRPC port for video services. Default is 50065."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK___init__(host, sdk_port, audio_port, video_port)

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
    def reachy_sdk_ReachySDK_connect(cls, ) -> Dict[str, Any]:
        """Connects the SDK to the robot."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_connect()

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
    def reachy_sdk_ReachySDK_disconnect(cls, lost_connection) -> Dict[str, Any]:
        """Disconnect the SDK from the robot's server.
        
        Args:
            lost_connection: If `True`, indicates that the connection was lost unexpectedly."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_disconnect(lost_connection)

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
    def reachy_sdk_ReachySDK___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a Reachy."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK___repr__()

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
    def reachy_sdk_ReachySDK_info(cls, ) -> Dict[str, Any]:
        """Get ReachyInfo if connected."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_info()

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
    def reachy_sdk_ReachySDK_head(cls, ) -> Dict[str, Any]:
        """Get Reachy's head."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_head()

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
    def reachy_sdk_ReachySDK_r_arm(cls, ) -> Dict[str, Any]:
        """Get Reachy's right arm."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_r_arm()

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
    def reachy_sdk_ReachySDK_l_arm(cls, ) -> Dict[str, Any]:
        """Get Reachy's left arm."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_l_arm()

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
    def reachy_sdk_ReachySDK_mobile_base(cls, ) -> Dict[str, Any]:
        """Get Reachy's mobile base."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_mobile_base()

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
    def reachy_sdk_ReachySDK_tripod(cls, ) -> Dict[str, Any]:
        """Get Reachy's fixed tripod."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_tripod()

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
    def reachy_sdk_ReachySDK_joints(cls, ) -> Dict[str, Any]:
        """Return a dictionary of all joints of the robot.
        
        The dictionary keys are the joint names, and the values are the corresponding OrbitaJoint objects."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_joints()

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
    def reachy_sdk_ReachySDK__actuators(cls, ) -> Dict[str, Any]:
        """Return a dictionary of all actuators of the robot.
        
        The dictionary keys are the actuator names, and the values are the corresponding actuator objects."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK__actuators()

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
    def reachy_sdk_ReachySDK_is_connected(cls, ) -> Dict[str, Any]:
        """Check if the SDK is connected to the robot.
        
        Returns:
            `True` if connected, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_is_connected()

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
    def reachy_sdk_ReachySDK_cameras(cls, ) -> Dict[str, Any]:
        """Get the camera manager if available and connected."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_cameras()

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
    def reachy_sdk_ReachySDK_get_update_timestamp(cls, ) -> Dict[str, Any]:
        """Returns the timestamp (ns) of the last update.
        
        The timestamp is generated by ROS running on Reachy.
        
        Returns:
            timestamp (int) in nanoseconds."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_get_update_timestamp()

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
    def reachy_sdk_ReachySDK_audit(cls, ) -> Dict[str, Any]:
        """Return the audit status of all enabled parts of the robot."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_audit()

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
    def reachy_sdk_ReachySDK_turn_on(cls, ) -> Dict[str, Any]:
        """Activate all motors of the robot's parts if all of them are not already turned on.
        
        Returns:
            `True` if successful, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_turn_on()

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
    def reachy_sdk_ReachySDK_turn_off(cls, ) -> Dict[str, Any]:
        """Turn all motors of enabled parts off.
        
        All enabled parts' motors will then be compliant."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_turn_off()

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
    def reachy_sdk_ReachySDK_turn_off_smoothly(cls, ) -> Dict[str, Any]:
        """Turn all motors of robot parts off.
        
        Arm torques are reduced during 3 seconds, then all parts' motors will be compliant."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_turn_off_smoothly()

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
    def reachy_sdk_ReachySDK_is_on(cls, ) -> Dict[str, Any]:
        """Check if all actuators of Reachy parts are on (stiff).
        
        Returns:
            `True` if all are stiff, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_is_on()

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
    def reachy_sdk_ReachySDK_is_off(cls, ) -> Dict[str, Any]:
        """Check if all actuators of Reachy parts are off (compliant).
        
        Returns:
            `True` if all are compliant, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_is_off()

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
    def reachy_sdk_ReachySDK_reset_default_limits(cls, ) -> Dict[str, Any]:
        """Set back speed and torque limits of all parts to maximum value (100)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_reset_default_limits()

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
    def reachy_sdk_ReachySDK_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode, open_gripper) -> Dict[str, Any]:
        """Move the robot to a predefined posture.
        
        Args:
            common_posture: The name of the posture. It can be 'default' or 'elbow_90'. Defaults to 'default'.
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
            A GoToHomeId containing movement GoToIds for each part."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode, open_gripper)

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
    def reachy_sdk_ReachySDK_is_goto_finished(cls, goto_id) -> Dict[str, Any]:
        """Check if a goto command has completed.
        
        Args:
            goto_id: The unique GoToId of the goto command.
        
        Returns:
            `True` if the command is complete, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_is_goto_finished(goto_id)

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
    def reachy_sdk_ReachySDK_get_goto_request(cls, goto_id) -> Dict[str, Any]:
        """Retrieve the details of a goto command based on its GoToId.
        
        Args:
            goto_id: The ID of the goto command for which details are requested.
        
        Returns:
            A `SimplifiedRequest` object containing the part name, joint goal positions
            (in degrees), movement duration, and interpolation mode.
            Returns `None` if the robot is not connected or if the `goto_id` is invalid.
        
        Raises:
            TypeError: If `goto_id` is not an instance of `GoToId`.
            ValueError: If `goto_id` is -1, indicating an invalid command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_get_goto_request(goto_id)

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
    def reachy_sdk_ReachySDK_cancel_goto_by_id(cls, goto_id) -> Dict[str, Any]:
        """Request the cancellation of a specific goto command based on its GoToId.
        
        Args:
            goto_id: The ID of the goto command to cancel.
        
        Returns:
            A `GoToAck` object indicating whether the cancellation was acknowledged.
            If the robot is not connected, returns None.
        
        Raises:
            TypeError: If `goto_id` is not an instance of `GoToId`."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_cancel_goto_by_id(goto_id)

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
    def reachy_sdk_ReachySDK_cancel_all_goto(cls, ) -> Dict[str, Any]:
        """Cancel all active goto commands.
        
        Returns:
             A `GoToAck` object indicating whether the cancellation was acknowledged."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_cancel_all_goto()

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
    def reachy_sdk_ReachySDK_send_goal_positions(cls, check_positions) -> Dict[str, Any]:
        """Send the goal positions to the robot.
        
        If goal positions have been specified for any joint of the robot, sends them to the robot.
        
        Args :
            check_positions: A boolean indicating whether to check the positions after sending the command.
                Defaults to True."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'sdk')

            # Call the function with parameters
            result = obj.ReachySDK_send_goal_positions(check_positions)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
