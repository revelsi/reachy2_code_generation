#!/usr/bin/env python
"""
Head tools for controlling the Reachy 2 robot's head.

This module provides tools for controlling the head of the Reachy 2 robot,
including looking at positions, orientation control, and joint space control.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import time
import math
import numpy as np

from .base_tool import BaseTool, get_reachy_connection


class HeadTools(BaseTool):
    """Tools for controlling the Reachy 2 robot's head."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all head tools."""
        # Register look_at tool
        cls.register_tool(
            name="look_at",
            func=cls.look_at,
            schema=cls.create_tool_schema(
                name="look_at",
                description="Make the robot look at a specific point in space.",
                parameters={
                    "x": {
                        "type": "number",
                        "description": "X coordinate in meters (forward is positive)."
                    },
                    "y": {
                        "type": "number",
                        "description": "Y coordinate in meters (left is positive)."
                    },
                    "z": {
                        "type": "number",
                        "description": "Z coordinate in meters (up is positive)."
                    },
                    "frame": {
                        "type": "string",
                        "description": "Reference frame ('robot' or 'head').",
                        "enum": ["robot", "head"]
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
                required=["x", "y", "z"]
            )
        )
        
        # Register rotate_by tool
        cls.register_tool(
            name="rotate_by",
            func=cls.rotate_by,
            schema=cls.create_tool_schema(
                name="rotate_by",
                description="Rotate the head by specified angles.",
                parameters={
                    "roll": {
                        "type": "number",
                        "description": "Roll angle in degrees."
                    },
                    "pitch": {
                        "type": "number",
                        "description": "Pitch angle in degrees."
                    },
                    "yaw": {
                        "type": "number",
                        "description": "Yaw angle in degrees."
                    },
                    "frame": {
                        "type": "string",
                        "description": "Reference frame ('robot' or 'head').",
                        "enum": ["robot", "head"]
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
                required=["roll", "pitch", "yaw"]
            )
        )
        
        # Register goto tool
        cls.register_tool(
            name="goto",
            func=cls.goto,
            schema=cls.create_tool_schema(
                name="goto",
                description="Move the head to specified joint positions.",
                parameters={
                    "positions": {
                        "type": "array",
                        "description": "List of joint positions in degrees: [neck_roll, neck_pitch, neck_yaw].",
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
                        "description": "Whether to wait for the movement to complete."
                    }
                },
                required=["positions"]
            )
        )
        
        # Register get_position tool
        cls.register_tool(
            name="get_position",
            func=cls.get_position,
            schema=cls.create_tool_schema(
                name="get_position",
                description="Get the current position of the head.",
                parameters={}
            )
        )
    
    @staticmethod
    def look_at(
        x: float,
        y: float,
        z: float,
        frame: str = "robot",
        duration: float = 1.0,
        interpolation_mode: str = "minimum_jerk",
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Make the robot look at a specific point in space.
        
        Args:
            x: X coordinate in meters (forward is positive).
            y: Y coordinate in meters (left is positive).
            z: Z coordinate in meters (up is positive).
            frame: Reference frame ('robot' or 'head').
            duration: Duration of the movement in seconds.
            interpolation_mode: Type of interpolation ('linear' or 'minimum_jerk').
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate frame parameter
            if frame not in ["robot", "head"]:
                return {
                    "success": False,
                    "error": f"Invalid frame: {frame}. Must be 'robot' or 'head'."
                }
            
            # Validate interpolation mode
            if interpolation_mode not in ["linear", "minimum_jerk"]:
                return {
                    "success": False,
                    "error": f"Invalid interpolation mode: {interpolation_mode}. Must be 'linear' or 'minimum_jerk'."
                }
            
            # Use the look_at method of the head
            reachy.head.look_at(
                x=x,
                y=y,
                z=z,
                frame=frame,
                duration=duration,
                interpolation_mode=interpolation_mode,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Looking at point ({x}, {y}, {z}) in {frame} frame"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def rotate_by(
        roll: float,
        pitch: float,
        yaw: float,
        frame: str = "robot",
        duration: float = 1.0,
        interpolation_mode: str = "minimum_jerk",
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Rotate the head by specified angles.
        
        Args:
            roll: Roll angle in degrees.
            pitch: Pitch angle in degrees.
            yaw: Yaw angle in degrees.
            frame: Reference frame ('robot' or 'head').
            duration: Duration of the movement in seconds.
            interpolation_mode: Type of interpolation ('linear' or 'minimum_jerk').
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate frame parameter
            if frame not in ["robot", "head"]:
                return {
                    "success": False,
                    "error": f"Invalid frame: {frame}. Must be 'robot' or 'head'."
                }
            
            # Validate interpolation mode
            if interpolation_mode not in ["linear", "minimum_jerk"]:
                return {
                    "success": False,
                    "error": f"Invalid interpolation mode: {interpolation_mode}. Must be 'linear' or 'minimum_jerk'."
                }
            
            # Use the rotate_by method of the head
            reachy.head.rotate_by(
                roll=roll,
                pitch=pitch,
                yaw=yaw,
                frame=frame,
                duration=duration,
                interpolation_mode=interpolation_mode,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Rotated head by (roll={roll}°, pitch={pitch}°, yaw={yaw}°) in {frame} frame"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def goto(
        positions: List[float],
        duration: float = 1.0,
        interpolation_mode: str = "minimum_jerk",
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Move the head to specified joint positions.
        
        Args:
            positions: List of joint positions in degrees: [neck_roll, neck_pitch, neck_yaw].
            duration: Duration of the movement in seconds.
            interpolation_mode: Type of interpolation ('linear' or 'minimum_jerk').
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate positions parameter
            if len(positions) != 3:
                return {
                    "success": False,
                    "error": f"Invalid positions: {positions}. Must be a list of 3 joint positions."
                }
            
            # Validate interpolation mode
            if interpolation_mode not in ["linear", "minimum_jerk"]:
                return {
                    "success": False,
                    "error": f"Invalid interpolation mode: {interpolation_mode}. Must be 'linear' or 'minimum_jerk'."
                }
            
            # Use the goto method of the head
            reachy.head.goto(
                positions,
                duration=duration,
                interpolation_mode=interpolation_mode,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Moved head to joint positions {positions}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_position(host: str = "localhost") -> Dict[str, Any]:
        """
        Get the current position of the head.
        
        Args:
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing current joint positions and names.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Get current positions
            positions = reachy.head.get_current_positions()
            
            # Get joint names
            joint_names = list(reachy.head.joints.keys())
            
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