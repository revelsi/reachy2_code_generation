#!/usr/bin/env python
"""
Utility tools for the Reachy 2 robot.

This module provides utility tools for the Reachy 2 robot, including camera access,
audio control, mobile base control, and robot information.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import time
import datetime
import platform
import psutil
import os
import json
import subprocess
import requests
import numpy as np

from .base_tool import BaseTool, get_reachy_connection


class UtilityTools(BaseTool):
    """General utility tools for the Reachy 2 robot."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all utility tools."""
        # Register camera tools
        cls.register_tool(
            name="get_camera_frame",
            func=cls.get_camera_frame,
            schema=cls.create_tool_schema(
                name="get_camera_frame",
                description="Get a frame from a specified camera."
            )
        )
        
        cls.register_tool(
            name="get_camera_info",
            func=cls.get_camera_info,
            schema=cls.create_tool_schema(
                name="get_camera_info",
                description="Get information about a specified camera."
            )
        )
        
        # Register audio tools
        cls.register_tool(
            name="play_audio",
            func=cls.play_audio,
            schema=cls.create_tool_schema(
                name="play_audio",
                description="Play an audio file."
            )
        )
        
        cls.register_tool(
            name="record_audio",
            func=cls.record_audio,
            schema=cls.create_tool_schema(
                name="record_audio",
                description="Record audio for a specified duration."
            )
        )
        
        # Register mobile base tools
        cls.register_tool(
            name="move_base",
            func=cls.move_base,
            schema=cls.create_tool_schema(
                name="move_base",
                description="Move the mobile base to a target pose."
            )
        )
        
        cls.register_tool(
            name="translate_base",
            func=cls.translate_base,
            schema=cls.create_tool_schema(
                name="translate_base",
                description="Translate the mobile base by a specified distance."
            )
        )
        
        cls.register_tool(
            name="get_base_position",
            func=cls.get_base_position,
            schema=cls.create_tool_schema(
                name="get_base_position",
                description="Get the current position of the mobile base."
            )
        )
        
        # Register robot info tool
        cls.register_tool(
            name="get_robot_info",
            func=cls.get_robot_info,
            schema=cls.create_tool_schema(
                name="get_robot_info",
                description="Get information about the Reachy 2 robot."
            )
        )
        
        # Register get_system_info tool
        cls.register_tool(
            name="get_system_info",
            func=cls.get_system_info,
            schema=cls.create_tool_schema(
                name="get_system_info",
                description="Get information about the system running the robot.",
                parameters={}
            )
        )
        
        # Register get_time tool
        cls.register_tool(
            name="get_time",
            func=cls.get_time,
            schema=cls.create_tool_schema(
                name="get_time",
                description="Get the current time and date.",
                parameters={}
            )
        )
        
        # Register sleep tool
        cls.register_tool(
            name="sleep",
            func=cls.sleep,
            schema=cls.create_tool_schema(
                name="sleep",
                description="Pause execution for a specified number of seconds.",
                parameters={
                    "seconds": {
                        "type": "number",
                        "description": "Number of seconds to sleep."
                    }
                },
                required=["seconds"]
            )
        )
        
        # Register run_command tool
        cls.register_tool(
            name="run_command",
            func=cls.run_command,
            schema=cls.create_tool_schema(
                name="run_command",
                description="Run a shell command on the robot's system.",
                parameters={
                    "command": {
                        "type": "string",
                        "description": "The command to run."
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds for the command."
                    }
                },
                required=["command"]
            )
        )
        
        # Register fetch_url tool
        cls.register_tool(
            name="fetch_url",
            func=cls.fetch_url,
            schema=cls.create_tool_schema(
                name="fetch_url",
                description="Fetch content from a URL.",
                parameters={
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch."
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method to use.",
                        "enum": ["GET", "POST", "PUT", "DELETE"]
                    },
                    "headers": {
                        "type": "object",
                        "description": "HTTP headers to include in the request."
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to include in the request body."
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds for the request."
                    }
                },
                required=["url"]
            )
        )
        
        # Register save_data tool
        cls.register_tool(
            name="save_data",
            func=cls.save_data,
            schema=cls.create_tool_schema(
                name="save_data",
                description="Save data to a file.",
                parameters={
                    "data": {
                        "type": "object",
                        "description": "The data to save."
                    },
                    "filename": {
                        "type": "string",
                        "description": "The filename to save the data to."
                    },
                    "format": {
                        "type": "string",
                        "description": "The format to save the data in.",
                        "enum": ["json", "text"]
                    }
                },
                required=["data", "filename"]
            )
        )
        
        # Register load_data tool
        cls.register_tool(
            name="load_data",
            func=cls.load_data,
            schema=cls.create_tool_schema(
                name="load_data",
                description="Load data from a file.",
                parameters={
                    "filename": {
                        "type": "string",
                        "description": "The filename to load the data from."
                    },
                    "format": {
                        "type": "string",
                        "description": "The format of the data in the file.",
                        "enum": ["json", "text"]
                    }
                },
                required=["filename"]
            )
        )
    
    @staticmethod
    def get_camera_frame(
        camera: str,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Get a frame from a specified camera.
        
        Args:
            camera: Which camera to use ('teleop' or 'depth').
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing the camera frame.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate camera parameter
            if camera not in ["teleop", "depth"]:
                return {
                    "success": False,
                    "error": f"Invalid camera: {camera}. Must be 'teleop' or 'depth'."
                }
            
            # Get the camera object
            camera_obj = getattr(reachy.cameras, camera)
            
            # Get the frame
            frame = camera_obj.get_frame()
            
            return {
                "success": True,
                "result": {
                    "frame": frame.tolist() if isinstance(frame, np.ndarray) else frame,
                    "timestamp": time.time()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_camera_info(
        camera: str,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Get information about a specified camera.
        
        Args:
            camera: Which camera to get info for ('teleop' or 'depth').
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing camera information.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Validate camera parameter
            if camera not in ["teleop", "depth"]:
                return {
                    "success": False,
                    "error": f"Invalid camera: {camera}. Must be 'teleop' or 'depth'."
                }
            
            # Get the camera object
            camera_obj = getattr(reachy.cameras, camera)
            
            # Get camera info
            info = {
                "name": camera,
                "resolution": camera_obj.resolution if hasattr(camera_obj, "resolution") else None,
                "fps": camera_obj.fps if hasattr(camera_obj, "fps") else None,
                "parameters": camera_obj.parameters if hasattr(camera_obj, "parameters") else None
            }
            
            return {
                "success": True,
                "result": info
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def play_audio(
        file_path: str,
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Play an audio file.
        
        Args:
            file_path: Path to the audio file to play.
            wait: Whether to wait for playback to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Play the audio file
            reachy.audio.play(file_path, wait=wait)
            
            return {
                "success": True,
                "result": f"Playing audio file: {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def record_audio(
        duration: float,
        file_path: str,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Record audio for a specified duration.
        
        Args:
            duration: Duration to record in seconds.
            file_path: Path where to save the recorded audio.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Record audio
            reachy.audio.record(duration=duration, file_path=file_path)
            
            return {
                "success": True,
                "result": f"Recorded {duration} seconds of audio to {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def move_base(
        x: float,
        y: float,
        theta: float,
        duration: float = 2.0,
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Move the mobile base to a target pose.
        
        Args:
            x: Target X position in meters.
            y: Target Y position in meters.
            theta: Target orientation in degrees.
            duration: Duration of the movement in seconds.
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Move the base
            reachy.mobile_base.goto(
                x=x,
                y=y,
                theta=theta,
                duration=duration,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Moved base to (x={x}m, y={y}m, theta={theta}°)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def translate_base(
        x: float = 0.0,
        y: float = 0.0,
        theta: float = 0.0,
        duration: float = 2.0,
        wait: bool = True,
        host: str = "localhost"
    ) -> Dict[str, Any]:
        """
        Translate the mobile base by a specified distance.
        
        Args:
            x: Distance to move in X direction (meters).
            y: Distance to move in Y direction (meters).
            theta: Angle to rotate (degrees).
            duration: Duration of the movement in seconds.
            wait: Whether to wait for the movement to complete.
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Translate the base
            reachy.mobile_base.translate_by(
                x=x,
                y=y,
                theta=theta,
                duration=duration,
                wait=wait
            )
            
            return {
                "success": True,
                "result": f"Translated base by (x={x}m, y={y}m, theta={theta}°)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_base_position(host: str = "localhost") -> Dict[str, Any]:
        """
        Get the current position of the mobile base.
        
        Args:
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing current base position and orientation.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Get current position
            position = reachy.mobile_base.get_position()
            
            return {
                "success": True,
                "result": {
                    "x": position.x,
                    "y": position.y,
                    "theta": position.theta
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_robot_info(host: str = "localhost") -> Dict[str, Any]:
        """
        Get information about the Reachy 2 robot.
        
        Args:
            host: Hostname or IP address of the Reachy robot.
            
        Returns:
            Dict[str, Any]: Result containing robot information.
        """
        try:
            reachy = get_reachy_connection(host)
            
            # Collect information about the robot
            info = {
                "robot_name": "Reachy 2",
                "sdk_version": reachy.sdk_version if hasattr(reachy, "sdk_version") else "Unknown",
                "hardware_version": reachy.hardware_version if hasattr(reachy, "hardware_version") else "Unknown",
                "available_parts": [],
                "connection_status": "Connected"
            }
            
            # Check which parts are available
            if hasattr(reachy, "arms"):
                info["available_parts"].append("arms")
            if hasattr(reachy, "head"):
                info["available_parts"].append("head")
            if hasattr(reachy, "mobile_base"):
                info["available_parts"].append("mobile_base")
            if hasattr(reachy, "cameras"):
                info["available_parts"].append("cameras")
            if hasattr(reachy, "audio"):
                info["available_parts"].append("audio")
            
            return {
                "success": True,
                "result": info
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        Get information about the system running the robot.
        
        Returns:
            Dict[str, Any]: Result of the operation with system information.
        """
        try:
            # Collect system information
            info = {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free,
                    "percent": psutil.disk_usage('/').percent
                }
            }
            
            return {
                "success": True,
                "result": info
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_time() -> Dict[str, Any]:
        """
        Get the current time and date.
        
        Returns:
            Dict[str, Any]: Result of the operation with time information.
        """
        try:
            now = datetime.datetime.now()
            
            # Format the time information
            time_info = {
                "timestamp": now.timestamp(),
                "iso_format": now.isoformat(),
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "timezone": time.tzname[0]
            }
            
            return {
                "success": True,
                "result": time_info
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def sleep(seconds: float) -> Dict[str, Any]:
        """
        Pause execution for a specified number of seconds.
        
        Args:
            seconds: Number of seconds to sleep.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            # Validate seconds parameter
            if seconds < 0:
                return {
                    "success": False,
                    "error": f"Invalid seconds: {seconds}. Must be a non-negative number."
                }
            
            # Sleep for the specified number of seconds
            time.sleep(seconds)
            
            return {
                "success": True,
                "result": f"Slept for {seconds} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def run_command(command: str, timeout: float = 30.0) -> Dict[str, Any]:
        """
        Run a shell command on the robot's system.
        
        Args:
            command: The command to run.
            timeout: Timeout in seconds for the command.
            
        Returns:
            Dict[str, Any]: Result of the operation with command output.
        """
        try:
            # Run the command and capture output
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Format the result
            command_result = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }
            
            return {
                "success": result.returncode == 0,
                "result": command_result
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds: {command}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def fetch_url(
        url: str,
        method: str = "GET",
        headers: Dict[str, str] = None,
        data: Dict[str, Any] = None,
        timeout: float = 10.0
    ) -> Dict[str, Any]:
        """
        Fetch content from a URL.
        
        Args:
            url: The URL to fetch.
            method: HTTP method to use.
            headers: HTTP headers to include in the request.
            data: Data to include in the request body.
            timeout: Timeout in seconds for the request.
            
        Returns:
            Dict[str, Any]: Result of the operation with response content.
        """
        try:
            # Set default headers if none provided
            if headers is None:
                headers = {
                    "User-Agent": "Reachy2-Robot/1.0"
                }
            
            # Make the request
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if method in ["POST", "PUT"] else None,
                params=data if method == "GET" else None,
                timeout=timeout
            )
            
            # Try to parse JSON response
            try:
                content = response.json()
            except:
                content = response.text
            
            # Format the result
            fetch_result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": content,
                "url": url
            }
            
            return {
                "success": response.status_code < 400,
                "result": fetch_result
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def save_data(
        data: Dict[str, Any],
        filename: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Save data to a file.
        
        Args:
            data: The data to save.
            filename: The filename to save the data to.
            format: The format to save the data in.
            
        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
            
            # Save the data in the specified format
            if format == "json":
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
            else:  # text format
                with open(filename, 'w') as f:
                    f.write(str(data))
            
            return {
                "success": True,
                "result": f"Data saved to {filename} in {format} format"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def load_data(
        filename: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Load data from a file.
        
        Args:
            filename: The filename to load the data from.
            format: The format of the data in the file.
            
        Returns:
            Dict[str, Any]: Result of the operation with loaded data.
        """
        try:
            # Check if file exists
            if not os.path.exists(filename):
                return {
                    "success": False,
                    "error": f"File not found: {filename}"
                }
            
            # Load the data from the specified format
            if format == "json":
                with open(filename, 'r') as f:
                    data = json.load(f)
            else:  # text format
                with open(filename, 'r') as f:
                    data = f.read()
            
            return {
                "success": True,
                "result": data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 