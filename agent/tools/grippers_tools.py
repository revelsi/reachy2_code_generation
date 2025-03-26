#!/usr/bin/env python
"""
grippers tools for the Reachy 2 robot.

This module provides tools for interacting with the grippers module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class GrippersTools(BaseTool):
    """Tools for interacting with the grippers module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all grippers tools."""
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint___init__",
            func=cls.grippers_gripper_joint_GripperJoint___init__,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint___init__",
                description="""Initialize the GripperJoint with its initial state.

This sets up the joint by assigning its state based on the provided initial values.

Args:
    initial_state: A HandState containing the initial state of the joint.""",
                parameters={'initial_state': {'type': 'string', 'description': 'A HandState containing the initial state of the joint.'}},
                required=['initial_state']
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint___repr__",
            func=cls.grippers_gripper_joint_GripperJoint___repr__,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint___repr__",
                description="""Clean representation of a GripperJoint.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint_opening",
            func=cls.grippers_gripper_joint_GripperJoint_opening,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint_opening",
                description="""Get the opening of the joint as a percentage.

Returns:
    The joint opening as a percentage (0-100), rounded to two decimal places.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint_present_position",
            func=cls.grippers_gripper_joint_GripperJoint_present_position,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint_present_position",
                description="""Get the current position of the joint.

Returns:
    The present position of the joint in degrees.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint_goal_position",
            func=cls.grippers_gripper_joint_GripperJoint_goal_position,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint_goal_position",
                description="""Set the goal position for the joint.

Args:
    value: The goal position to set, specified as a float or int.

Raises:
    TypeError: If the provided value is not a float or int.""",
                parameters={'value': {'type': 'string', 'description': 'The goal position to set, specified as a float or int.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint_is_on",
            func=cls.grippers_gripper_joint_GripperJoint_is_on,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint_is_on",
                description="""Check if the joint is stiff.

Returns:
    `True` if the joint is on (not compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint_is_off",
            func=cls.grippers_gripper_joint_GripperJoint_is_off,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint_is_off",
                description="""Check if the joint is compliant.

Returns:
    `True` if the joint is off (compliant), `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_gripper_joint_GripperJoint_is_moving",
            func=cls.grippers_gripper_joint_GripperJoint_is_moving,
            schema=cls.create_tool_schema(
                name="grippers_gripper_joint_GripperJoint_is_moving",
                description="""Check if the joint is currently moving.

Returns:
    `True` if the joint is moving, `False` otherwise.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper___init__",
            func=cls.grippers_parallel_gripper_ParallelGripper___init__,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper___init__",
                description="""Initialize the ParallelGripper component.

Sets up the necessary attributes and configuration for the hand, including the gRPC
stub and initial state.

Args:
    hand_msg: The Hand_proto object containing the configuration details for the hand.
    initial_state: The initial state of the hand, represented as a HandState object.
    grpc_channel: The gRPC channel used to communicate with the hand's gRPC service.
    goto_stub: The gRPC stub for controlling goto movements.""",
                parameters={'hand_msg': {'type': 'string', 'description': 'The Hand_proto object containing the configuration details for the hand.'}, 'initial_state': {'type': 'string', 'description': 'The initial state of the hand, represented as a HandState object.'}, 'grpc_channel': {'type': 'string', 'description': "The gRPC channel used to communicate with the hand's gRPC service."}, 'goto_stub': {'type': 'string', 'description': 'The gRPC stub for controlling goto movements.'}},
                required=['hand_msg', 'initial_state', 'grpc_channel', 'goto_stub']
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper___repr__",
            func=cls.grippers_parallel_gripper_ParallelGripper___repr__,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper___repr__",
                description="""Clean representation of a ParallelGripper.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_opening",
            func=cls.grippers_parallel_gripper_ParallelGripper_opening,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_opening",
                description="""Get the opening of the parallel gripper only joint as a percentage.

Returns:
    The hand opening as a percentage (0-100), rounded to two decimal places.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_present_position",
            func=cls.grippers_parallel_gripper_ParallelGripper_present_position,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_present_position",
                description="""Get the current position of the parallel gripper only joint.

Returns:
    The present position of the hand in degrees.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_goal_position",
            func=cls.grippers_parallel_gripper_ParallelGripper_goal_position,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_goal_position",
                description="""Set the goal position for the parallel gripper only joint.

Args:
    value: The goal position to set, specified as a float or int.

Raises:
    TypeError: If the provided value is not a float or int.""",
                parameters={'value': {'type': 'string', 'description': 'The goal position to set, specified as a float or int.'}},
                required=['value']
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_get_current_opening",
            func=cls.grippers_parallel_gripper_ParallelGripper_get_current_opening,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_get_current_opening",
                description="""Get the current opening of the parallel gripper only joint.

Returns:
    The current opening of the hand as a percentage (0-100).""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_set_opening",
            func=cls.grippers_parallel_gripper_ParallelGripper_set_opening,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_set_opening",
                description="""Set the opening value for the parallel gripper only joint.

Args:
    percentage: The desired opening percentage of the hand, ranging from 0 to 100.

Raises:
    ValueError: If the percentage is not between 0 and 100.
    RuntimeError: If the gripper is off and the opening value cannot be set.""",
                parameters={'percentage': {'type': 'number', 'description': 'The desired opening percentage of the hand, ranging from 0 to 100.'}},
                required=['percentage']
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_goto_posture",
            func=cls.grippers_parallel_gripper_ParallelGripper_goto_posture,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_goto_posture",
                description="""Send the gripper to default open posture with optional parameters for duration, waiting, and interpolation mode.

Args:
    common_posture: The standard posture. It can be 'default' or 'elbow_90'. Defaults to 'default'.
        Modifying the posture has no effect on the hand.
    duration: The time duration in seconds for the robot to move to the specified posture.
        Defaults to 2.
    wait: Determines whether the program should wait for the movement to finish before
        returning. If set to `True`, the program waits for the movement to complete before continuing
        execution. Defaults to `False`.
    wait_for_goto_end: Specifies whether commands will be sent to a part immediately or
        only after all previous commands in the queue have been executed. If set to `False`, the program
        will cancel all executing moves and queues. Defaults to `True`.
    interpolation_mode: The type of interpolation used when moving the gripper.
        Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.

Returns:
    A unique GoToId identifier for this specific movement.""",
                parameters={'common_posture': {'type': 'string', 'description': "The standard posture. It can be 'default' or 'elbow_90'. Defaults to 'default'."}, 'duration': {'type': 'number', 'description': 'The time duration in seconds for the robot to move to the specified posture.'}, 'wait': {'type': 'boolean', 'description': 'Determines whether the program should wait for the movement to finish before'}, 'wait_for_goto_end': {'type': 'boolean', 'description': 'Specifies whether commands will be sent to a part immediately or'}, 'interpolation_mode': {'type': 'string', 'description': 'The type of interpolation used when moving the gripper.'}},
                required=['common_posture', 'duration', 'wait', 'wait_for_goto_end', 'interpolation_mode']
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_goto",
            func=cls.grippers_parallel_gripper_ParallelGripper_goto,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_goto",
                description="""Move the hand to a specified goal position.

Args:
    target: The target position. It can either be a float or int.
    duration: The time in seconds for the movement to be completed. Defaults to 2.
    wait: If True, the function waits until the movement is completed before returning.
            Defaults to False.
    interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk"
            or "linear". Defaults to "minimum_jerk".
    degrees: If True, the joint values in the `target` argument are treated as degrees.
            Defaults to True.
    percentage: If True, the target value is treated as a percentage of opening. Defaults to False.

Returns:
    GoToId: The unique GoToId identifier for the movement command.""",
                parameters={'target': {'type': 'string', 'description': 'The target position. It can either be a float or int.'}, 'duration': {'type': 'number', 'description': 'The time in seconds for the movement to be completed. Defaults to 2.'}, 'wait': {'type': 'boolean', 'description': 'If True, the function waits until the movement is completed before returning.'}, 'interpolation_mode': {'type': 'string', 'description': 'The interpolation method to be used. It can be either "minimum_jerk"'}, 'degrees': {'type': 'boolean', 'description': 'If True, the joint values in the `target` argument are treated as degrees.'}, 'percentage': {'type': 'number', 'description': 'If True, the target value is treated as a percentage of opening. Defaults to False.'}},
                required=['target', 'duration', 'wait', 'interpolation_mode', 'degrees', 'percentage']
            )
        )
        cls.register_tool(
            name="grippers_parallel_gripper_ParallelGripper_status",
            func=cls.grippers_parallel_gripper_ParallelGripper_status,
            schema=cls.create_tool_schema(
                name="grippers_parallel_gripper_ParallelGripper_status",
                description="""Get the current audit status of the actuator.

Returns:
    The audit status as a string, representing the latest error or status
    message, or `None` if there is no error.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def grippers_gripper_joint_GripperJoint___init__(cls, initial_state) -> Dict[str, Any]:
        """Initialize the GripperJoint with its initial state.
        
        This sets up the joint by assigning its state based on the provided initial values.
        
        Args:
            initial_state: A HandState containing the initial state of the joint."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint___init__(initial_state)

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
    def grippers_gripper_joint_GripperJoint___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a GripperJoint."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint___repr__()

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
    def grippers_gripper_joint_GripperJoint_opening(cls, ) -> Dict[str, Any]:
        """Get the opening of the joint as a percentage.
        
        Returns:
            The joint opening as a percentage (0-100), rounded to two decimal places."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint_opening()

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
    def grippers_gripper_joint_GripperJoint_present_position(cls, ) -> Dict[str, Any]:
        """Get the current position of the joint.
        
        Returns:
            The present position of the joint in degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint_present_position()

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
    def grippers_gripper_joint_GripperJoint_goal_position(cls, value) -> Dict[str, Any]:
        """Set the goal position for the joint.
        
        Args:
            value: The goal position to set, specified as a float or int.
        
        Raises:
            TypeError: If the provided value is not a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint_goal_position(value)

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
    def grippers_gripper_joint_GripperJoint_is_on(cls, ) -> Dict[str, Any]:
        """Check if the joint is stiff.
        
        Returns:
            `True` if the joint is on (not compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint_is_on()

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
    def grippers_gripper_joint_GripperJoint_is_off(cls, ) -> Dict[str, Any]:
        """Check if the joint is compliant.
        
        Returns:
            `True` if the joint is off (compliant), `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint_is_off()

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
    def grippers_gripper_joint_GripperJoint_is_moving(cls, ) -> Dict[str, Any]:
        """Check if the joint is currently moving.
        
        Returns:
            `True` if the joint is moving, `False` otherwise."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'gripper')

            # Call the function with parameters
            result = obj.joint_GripperJoint_is_moving()

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
    def grippers_parallel_gripper_ParallelGripper___init__(cls, hand_msg, initial_state, grpc_channel, goto_stub) -> Dict[str, Any]:
        """Initialize the ParallelGripper component.
        
        Sets up the necessary attributes and configuration for the hand, including the gRPC
        stub and initial state.
        
        Args:
            hand_msg: The Hand_proto object containing the configuration details for the hand.
            initial_state: The initial state of the hand, represented as a HandState object.
            grpc_channel: The gRPC channel used to communicate with the hand's gRPC service.
            goto_stub: The gRPC stub for controlling goto movements."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper___init__(hand_msg, initial_state, grpc_channel, goto_stub)

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
    def grippers_parallel_gripper_ParallelGripper___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a ParallelGripper."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper___repr__()

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
    def grippers_parallel_gripper_ParallelGripper_opening(cls, ) -> Dict[str, Any]:
        """Get the opening of the parallel gripper only joint as a percentage.
        
        Returns:
            The hand opening as a percentage (0-100), rounded to two decimal places."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_opening()

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
    def grippers_parallel_gripper_ParallelGripper_present_position(cls, ) -> Dict[str, Any]:
        """Get the current position of the parallel gripper only joint.
        
        Returns:
            The present position of the hand in degrees."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_present_position()

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
    def grippers_parallel_gripper_ParallelGripper_goal_position(cls, value) -> Dict[str, Any]:
        """Set the goal position for the parallel gripper only joint.
        
        Args:
            value: The goal position to set, specified as a float or int.
        
        Raises:
            TypeError: If the provided value is not a float or int."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_goal_position(value)

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
    def grippers_parallel_gripper_ParallelGripper_get_current_opening(cls, ) -> Dict[str, Any]:
        """Get the current opening of the parallel gripper only joint.
        
        Returns:
            The current opening of the hand as a percentage (0-100)."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_get_current_opening()

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
    def grippers_parallel_gripper_ParallelGripper_set_opening(cls, percentage) -> Dict[str, Any]:
        """Set the opening value for the parallel gripper only joint.
        
        Args:
            percentage: The desired opening percentage of the hand, ranging from 0 to 100.
        
        Raises:
            ValueError: If the percentage is not between 0 and 100.
            RuntimeError: If the gripper is off and the opening value cannot be set."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_set_opening(percentage)

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
    def grippers_parallel_gripper_ParallelGripper_goto_posture(cls, common_posture, duration, wait, wait_for_goto_end, interpolation_mode) -> Dict[str, Any]:
        """Send the gripper to default open posture with optional parameters for duration, waiting, and interpolation mode.
        
        Args:
            common_posture: The standard posture. It can be 'default' or 'elbow_90'. Defaults to 'default'.
                Modifying the posture has no effect on the hand.
            duration: The time duration in seconds for the robot to move to the specified posture.
                Defaults to 2.
            wait: Determines whether the program should wait for the movement to finish before
                returning. If set to `True`, the program waits for the movement to complete before continuing
                execution. Defaults to `False`.
            wait_for_goto_end: Specifies whether commands will be sent to a part immediately or
                only after all previous commands in the queue have been executed. If set to `False`, the program
                will cancel all executing moves and queues. Defaults to `True`.
            interpolation_mode: The type of interpolation used when moving the gripper.
                Can be 'minimum_jerk' or 'linear'. Defaults to 'minimum_jerk'.
        
        Returns:
            A unique GoToId identifier for this specific movement."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_goto_posture(common_posture, duration, wait, wait_for_goto_end, interpolation_mode)

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
    def grippers_parallel_gripper_ParallelGripper_goto(cls, target, duration, wait, interpolation_mode, degrees, percentage) -> Dict[str, Any]:
        """Move the hand to a specified goal position.
        
        Args:
            target: The target position. It can either be a float or int.
            duration: The time in seconds for the movement to be completed. Defaults to 2.
            wait: If True, the function waits until the movement is completed before returning.
                    Defaults to False.
            interpolation_mode: The interpolation method to be used. It can be either "minimum_jerk"
                    or "linear". Defaults to "minimum_jerk".
            degrees: If True, the joint values in the `target` argument are treated as degrees.
                    Defaults to True.
            percentage: If True, the target value is treated as a percentage of opening. Defaults to False.
        
        Returns:
            GoToId: The unique GoToId identifier for the movement command."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_goto(target, duration, wait, interpolation_mode, degrees, percentage)

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
    def grippers_parallel_gripper_ParallelGripper_status(cls, ) -> Dict[str, Any]:
        """Get the current audit status of the actuator.
        
        Returns:
            The audit status as a string, representing the latest error or status
            message, or `None` if there is no error."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'parallel')

            # Call the function with parameters
            result = obj.gripper_ParallelGripper_status()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
