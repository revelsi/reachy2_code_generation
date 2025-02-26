#!/usr/bin/env python
"""
Arm tools for controlling the Reachy 2 robot's arms.

This module provides tools for controlling the arms of the Reachy 2 robot,
including joint space control, cartesian space control, kinematics, and gripper operations.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import time
import math
import numpy as np

from .base_tool import BaseTool, get_reachy_connection


class ArmTools(BaseTool):
    """Tools for controlling the Reachy 2 robot's arms."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all arm tools."""
        # Register move_arm tool - Core SDK function
        cls.register_tool(
            name="move_arm",
            func=cls.move_arm,
            schema=cls.create_tool_schema(
                name="move_arm",
                description="Move a robot arm to a specified position with interpolation.",
                parameters={
                    "arm": {
                        "type": "string",
                        "description": "Which arm to move ('left' or 'right').",
                        "enum": ["left", "right"]
                    },
                    "positions": {
                        "type": "array",
                        "description": "List of 7 joint positions in degrees: [shoulder_pitch, shoulder_roll, arm_yaw, elbow_pitch, forearm_yaw, wrist_pitch, wrist_roll].",
                        "items": {
                            "type": "number"
                        }
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration of the movement in seconds."
                    },
                    "interpolation_mode": {
                        "type": "string",
                        "description": "Type of interpolation ('linear' or 'minimum_jerk').",
                        "enum": ["linear", "minimum_jerk"]
                    },
                    "wait": {
                        "type": "boolean",
                        "description": "Whether to wait for the movement to complete before returning."
                    }
                },
                required=["arm", "positions"]
            )
        )
        
        # Register move_arm_cartesian tool
        cls.register_tool(
            name="move_arm_cartesian",
            func=cls.move_arm_cartesian,
            schema=cls.create_tool_schema(
                name="move_arm_cartesian",
                description="Move a robot arm to a target pose in cartesian space.",
                parameters={
                    "arm": {
                        "type": "string",
                        "description": "Which arm to move ('left' or 'right').",
                        "enum": ["left", "right"]
                    },
                    "target_pose": {
                        "type": "array",
                        "description": "4x4 pose matrix specifying target position and orientation.",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration of the movement in seconds."
                    },
                    "interpolation_mode": {
                        "type": "string",
                        "description": "Type of interpolation ('linear' or 'minimum_jerk').",
                        "enum": ["linear", "minimum_jerk"]
                    },
                    "wait": {
                        "type": "boolean",
                        "description": "Whether to wait for the movement to complete."
                    }
                },
                required=["arm", "target_pose"]
            )
        )
        
        # Register forward_kinematics tool
        cls.register_tool(
            name="forward_kinematics",
            func=cls.forward_kinematics,
            schema=cls.create_tool_schema(
                name="forward_kinematics",
                description="Compute forward kinematics for an arm.",
                parameters={
                    "arm": {
                        "type": "string",
                        "description": "Which arm to compute for ('left' or 'right').",
                        "enum": ["left", "right"]
                    },
                    "positions": {
                        "type": "array",
                        "description": "Optional list of 7 joint positions. If None, uses current positions.",
                        "items": {
                            "type": "number"
                        }
                    }
                },
                required=["arm"]
            )
        )
        
        # Register inverse_kinematics tool
        cls.register_tool(
            name="inverse_kinematics",
            func=cls.inverse_kinematics,
            schema=cls.create_tool_schema(
                name="inverse_kinematics",
                description="Compute inverse kinematics for an arm.",
                parameters={
                    "arm": {
                        "type": "string",
                        "description": "Which arm to compute for ('left' or 'right').",
                        "enum": ["left", "right"]
                    },
                    "target_pose": {
                        "type": "array",
                        "description": "4x4 pose matrix specifying target position and orientation.",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                },
                required=["arm", "target_pose"]
            )
        )
        
        # Register control_gripper tool
        cls.register_tool(
            name="control_gripper",
            func=cls.control_gripper,
            schema=cls.create_tool_schema(
                name="control_gripper",
                description="Control the gripper on an arm.",
                parameters={
                    "arm": {
                        "type": "string",
                        "description": "Which arm's gripper to control ('left' or 'right').",
                        "enum": ["left", "right"]
                    },
                    "command": {
                        "type": "string",
                        "description": "Command to execute ('open', 'close', or 'set_opening').",
                        "enum": ["open", "close", "set_opening"]
                    },
                    "opening": {
                        "type": "number",
                        "description": "Opening percentage (0-100) when using 'set_opening'."
                    }
                },
                required=["arm", "command"]
            )
        )
        
        # Register get_arm_position tool
        cls.register_tool(
            name="get_arm_position",
            func=cls.get_arm_position,
            schema=cls.create_tool_schema(
                name="get_arm_position",
                description="Get the current position of a robot arm.",
                parameters={
                    "arm": {
                        "type": "string",
                        "description": "Which arm to get the position of ('left' or 'right').",
                        "enum": ["left", "right"]
                    }
                },
                required=["arm"]
            )
        )
    
    @staticmethod
    def move_arm(
        arm: str,
        positions: List[float],
        duration: float = 2.0,
        interpolation_mode: str = "minimum_jerk",
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Move a robot arm to a specified position with interpolation.
        
        Args:
            arm: Which arm to move ('left' or 'right').
            positions: List of 7 joint positions in degrees.
            duration: Duration of the movement in seconds.
            interpolation_mode: Type of interpolation ('linear' or 'minimum_jerk').
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate arm parameter
            if arm not in ["left", "right"]:
                return {
                    "success": False,
                    "error": f"Invalid arm: {arm}. Must be 'left' or 'right'."
                }
            
            # Validate positions parameter
            if len(positions) != 7:
                return {
                    "success": False,
                    "error": f"Invalid positions: {positions}. Must be a list of 7 joint positions."
                }
            
            # Validate interpolation mode
            if interpolation_mode not in ["linear", "minimum_jerk"]:
                return {
                    "success": False,
                    "error": f"Invalid interpolation mode: {interpolation_mode}. Must be 'linear' or 'minimum_jerk'."
                }
            
            # Get the arm object
            arm_obj = getattr(reachy, f"{arm[0]}_arm")
            
            # Move the arm
            arm_obj.goto(
                positions,
                duration=duration,
                interpolation_mode=interpolation_mode,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Moved {arm} arm to {positions}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def move_arm_cartesian(
        arm: str,
        target_pose: List[List[float]],
        duration: float = 2.0,
        interpolation_mode: str = "minimum_jerk",
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Move a robot arm to a target pose in cartesian space.
        
        Args:
            arm: Which arm to move ('left' or 'right').
            target_pose: 4x4 pose matrix specifying target position and orientation.
            duration: Duration of the movement in seconds.
            interpolation_mode: Type of interpolation ('linear' or 'minimum_jerk').
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate arm parameter
            if arm not in ["left", "right"]:
                return {
                    "success": False,
                    "error": f"Invalid arm: {arm}. Must be 'left' or 'right'."
                }
            
            # Validate target_pose parameter
            if (len(target_pose) != 4 or 
                any(len(row) != 4 for row in target_pose)):
                return {
                    "success": False,
                    "error": "target_pose must be a 4x4 matrix."
                }
            
            # Convert target_pose to numpy array
            pose_matrix = np.array(target_pose)
            
            # Get the arm object
            arm_obj = getattr(reachy, f"{arm[0]}_arm")
            
            # Move the arm using cartesian control
            arm_obj.goto(
                pose_matrix,
                duration=duration,
                interpolation_mode=interpolation_mode,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Moved {arm} arm to target pose"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def forward_kinematics(
        arm: str,
        positions: Optional[List[float]] = None,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Compute forward kinematics for an arm.
        
        Args:
            arm: Which arm to compute for ('left' or 'right').
            positions: Optional list of 7 joint positions. If None, uses current positions.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing the 4x4 pose matrix.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate arm parameter
            if arm not in ["left", "right"]:
                return {
                    "success": False,
                    "error": f"Invalid arm: {arm}. Must be 'left' or 'right'."
                }
            
            # Get the arm object
            arm_obj = getattr(reachy, f"{arm[0]}_arm")
            
            # Compute forward kinematics
            if positions is not None:
                # Validate positions parameter
                if len(positions) != 7:
                    return {
                        "success": False,
                        "error": f"Invalid positions: {positions}. Must be a list of 7 joint positions."
                    }
                pose_matrix = arm_obj.forward_kinematics(positions)
            else:
                pose_matrix = arm_obj.forward_kinematics()
            
            return {
                "success": True,
                "result": pose_matrix.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def inverse_kinematics(
        arm: str,
        target_pose: List[List[float]],
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Compute inverse kinematics for an arm.
        
        Args:
            arm: Which arm to compute for ('left' or 'right').
            target_pose: 4x4 pose matrix specifying target position and orientation.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing joint positions to achieve the pose.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate arm parameter
            if arm not in ["left", "right"]:
                return {
                    "success": False,
                    "error": f"Invalid arm: {arm}. Must be 'left' or 'right'."
                }
            
            # Validate target_pose parameter
            if (len(target_pose) != 4 or 
                any(len(row) != 4 for row in target_pose)):
                return {
                    "success": False,
                    "error": "target_pose must be a 4x4 matrix."
                }
            
            # Convert target_pose to numpy array
            pose_matrix = np.array(target_pose)
            
            # Get the arm object
            arm_obj = getattr(reachy, f"{arm[0]}_arm")
            
            # Compute inverse kinematics
            joint_positions = arm_obj.inverse_kinematics(pose_matrix)
            
            return {
                "success": True,
                "result": joint_positions.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def control_gripper(
        arm: str,
        command: str,
        opening: Optional[float] = None,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Control the gripper on an arm.
        
        Args:
            arm: Which arm's gripper to control ('left' or 'right').
            command: Command to execute ('open', 'close', or 'set_opening').
            opening: Opening percentage (0-100) when using 'set_opening'.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate arm parameter
            if arm not in ["left", "right"]:
                return {
                    "success": False,
                    "error": f"Invalid arm: {arm}. Must be 'left' or 'right'."
                }
            
            # Validate command parameter
            if command not in ["open", "close", "set_opening"]:
                return {
                    "success": False,
                    "error": f"Invalid command: {command}. Must be 'open', 'close', or 'set_opening'."
                }
            
            # Get the gripper object
            gripper = getattr(reachy, f"{arm[0]}_arm").gripper
            
            # Execute the command
            if command == "open":
                gripper.open()
            elif command == "close":
                gripper.close()
            else:  # set_opening
                if opening is None:
                    return {
                        "success": False,
                        "error": "Opening percentage required for 'set_opening' command."
                    }
                if not 0 <= opening <= 100:
                    return {
                        "success": False,
                        "error": "Opening percentage must be between 0 and 100."
                    }
                gripper.set_opening(opening)
            
            # Wait for the gripper to finish moving
            while gripper.is_moving():
                time.sleep(0.1)
            
            return {
                "success": True,
                "result": f"Executed {command} command on {arm} gripper"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_arm_position(arm: str, host: str = "localhost") -> Dict[str, Any]:
        """
        Get the current position of a robot arm.
        
        Args:
            arm: Which arm to get the position of ('left' or 'right').
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing current joint positions and names.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate arm parameter
            if arm not in ["left", "right"]:
                return {
                    "success": False,
                    "error": f"Invalid arm: {arm}. Must be 'left' or 'right'."
                }
            
            # Get the arm object
            arm_obj = getattr(reachy, f"{arm[0]}_arm")
            
            # Get current positions
            positions = arm_obj.get_current_positions()
            
            # Get joint names
            joint_names = list(arm_obj.joints.keys())
            
            return {
                "success": True,
                "result": {
                    "positions": positions,
                    "joint_names": joint_names
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 