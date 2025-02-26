#!/usr/bin/env python
"""
Mock implementation of the Reachy 2 SDK for testing without a physical robot.

This module provides a simulated Reachy robot for testing purposes. It replicates
the behavior of the actual SDK with simulated responses and state tracking.
"""

import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import threading
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mock_reachy")

class MockReachy:
    """Mock implementation of the Reachy 2 robot."""
    
    def __init__(self, host: str = "localhost", use_virtual: bool = True):
        """
        Initialize a mock Reachy robot.
        
        Args:
            host: Hostname for the robot (ignored in mock)
            use_virtual: Whether to use a virtual robot (always True for mock)
        """
        logger.info(f"Initializing mock Reachy (host: {host}, virtual: {use_virtual})")
        
        # Robot state
        self.arms = {
            "left": MockArm("left"),
            "right": MockArm("right")
        }
        self.head = MockHead()
        self.mobile_base = MockMobileBase() if use_virtual else None
        self.cameras = {
            "teleop": MockCamera("teleop", (640, 480)),
            "depth": MockCamera("depth", (320, 240))
        }
        self.audio = MockAudio()
        
        # Connection state
        self.connected = True
        self.errors = []
        
        logger.info("Mock Reachy initialized")

    def close(self):
        """Close the connection to the robot."""
        logger.info("Closing mock Reachy connection")
        self.connected = False

    def get_info(self) -> Dict[str, Any]:
        """Get information about the robot."""
        return {
            "name": "Mock Reachy 2",
            "version": "2.0.0",
            "parts": ["left_arm", "right_arm", "head", "mobile_base"],
            "cameras": list(self.cameras.keys()),
            "has_audio": True,
            "has_mobile_base": self.mobile_base is not None,
            "connection": "virtual",
            "errors": self.errors
        }


class MockArm:
    """Mock implementation of a Reachy arm."""
    
    def __init__(self, side: str):
        """
        Initialize a mock arm.
        
        Args:
            side: Side of the arm ("left" or "right")
        """
        self.side = side
        
        # Joint configuration
        self.joint_names = [
            f"{side}_shoulder_pitch",
            f"{side}_shoulder_roll",
            f"{side}_arm_yaw",
            f"{side}_elbow_pitch",
            f"{side}_forearm_yaw",
            f"{side}_wrist_pitch",
            f"{side}_wrist_roll"
        ]
        
        # Current state
        self.current_positions = [0.0] * 7  # Neutral position
        self.target_positions = self.current_positions.copy()
        self.moving = False
        self.gripper = MockGripper(side)
        
    def goto(self, 
             positions: List[float], 
             duration: float = 1.0, 
             interpolation_mode: str = "minimum_jerk",
             wait: bool = True) -> bool:
        """
        Move the arm to the specified joint positions.
        
        Args:
            positions: List of joint positions in radians
            duration: Duration of the movement in seconds
            interpolation_mode: Interpolation mode
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Moving {self.side} arm to {positions} over {duration}s using {interpolation_mode}")
        
        if len(positions) != len(self.joint_names):
            logger.error(f"Expected {len(self.joint_names)} positions, got {len(positions)}")
            return False
        
        # Set target positions
        self.target_positions = positions.copy()
        self.moving = True
        
        # Simulate movement
        def _simulate_movement():
            time.sleep(duration)
            self.current_positions = self.target_positions.copy()
            self.moving = False
            logger.info(f"{self.side} arm movement completed")
        
        # Start movement thread
        movement_thread = threading.Thread(target=_simulate_movement)
        movement_thread.daemon = True
        movement_thread.start()
        
        # Wait if requested
        if wait:
            movement_thread.join()
        
        return True
    
    def get_current_positions(self) -> Dict[str, float]:
        """
        Get the current positions of the arm joints.
        
        Returns:
            Dict[str, float]: Dictionary mapping joint names to positions in radians
        """
        return dict(zip(self.joint_names, self.current_positions))
    
    def is_moving(self) -> bool:
        """
        Check if the arm is currently moving.
        
        Returns:
            bool: True if moving, False otherwise
        """
        return self.moving
    
    def forward_kinematics(self, positions: Optional[List[float]] = None) -> np.ndarray:
        """
        Compute forward kinematics for the arm.
        
        Args:
            positions: Optional list of joint positions (uses current positions if None)
            
        Returns:
            np.ndarray: 4x4 homogeneous transformation matrix
        """
        if positions is None:
            positions = self.current_positions
            
        # Simple mock implementation - just returns a transformation matrix
        # In a real implementation, this would compute actual forward kinematics
        return np.array([
            [1, 0, 0, 0.3],
            [0, 1, 0, 0.4 if self.side == "left" else -0.4],
            [0, 0, 1, 0.1],
            [0, 0, 0, 1]
        ])
    
    def inverse_kinematics(self, target_pose: np.ndarray) -> List[float]:
        """
        Compute inverse kinematics for the arm.
        
        Args:
            target_pose: 4x4 homogeneous transformation matrix
            
        Returns:
            List[float]: List of joint positions in radians
        """
        # Simple mock implementation - just returns a fixed configuration
        # In a real implementation, this would compute actual inverse kinematics
        return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]


class MockGripper:
    """Mock implementation of a Reachy gripper."""
    
    def __init__(self, side: str):
        """
        Initialize a mock gripper.
        
        Args:
            side: Side of the gripper ("left" or "right")
        """
        self.side = side
        self.current_opening = 0.5  # 50% open
        self.target_opening = self.current_opening
        self.moving = False
    
    def open(self, wait: bool = True) -> bool:
        """
        Open the gripper fully.
        
        Args:
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.set_opening(1.0, wait=wait)
    
    def close(self, wait: bool = True) -> bool:
        """
        Close the gripper fully.
        
        Args:
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.set_opening(0.0, wait=wait)
    
    def set_opening(self, opening: float, wait: bool = True) -> bool:
        """
        Set the gripper opening to the specified value.
        
        Args:
            opening: Opening value between 0.0 (closed) and 1.0 (open)
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Setting {self.side} gripper opening to {opening}")
        
        if opening < 0.0 or opening > 1.0:
            logger.error(f"Opening value must be between 0.0 and 1.0, got {opening}")
            return False
        
        # Set target opening
        self.target_opening = opening
        self.moving = True
        
        # Simulate movement
        def _simulate_movement():
            time.sleep(0.5)  # Fixed duration for gripper movement
            self.current_opening = self.target_opening
            self.moving = False
            logger.info(f"{self.side} gripper movement completed")
        
        # Start movement thread
        movement_thread = threading.Thread(target=_simulate_movement)
        movement_thread.daemon = True
        movement_thread.start()
        
        # Wait if requested
        if wait:
            movement_thread.join()
        
        return True
    
    def get_opening(self) -> float:
        """
        Get the current gripper opening.
        
        Returns:
            float: Current opening value between 0.0 (closed) and 1.0 (open)
        """
        return self.current_opening


class MockHead:
    """Mock implementation of the Reachy head."""
    
    def __init__(self):
        """Initialize a mock head."""
        # Joint configuration
        self.joint_names = ["neck_roll", "neck_pitch", "neck_yaw"]
        
        # Current state
        self.current_positions = [0.0, 0.0, 0.0]  # Neutral position
        self.target_positions = self.current_positions.copy()
        self.moving = False
        
    def look_at(self, 
                x: float, 
                y: float, 
                z: float, 
                frame: str = "robot",
                duration: float = 1.0, 
                interpolation_mode: str = "minimum_jerk",
                wait: bool = True) -> bool:
        """
        Make the head look at a point in space.
        
        Args:
            x: X coordinate in meters
            y: Y coordinate in meters
            z: Z coordinate in meters
            frame: Reference frame ("robot" or "head")
            duration: Duration of the movement in seconds
            interpolation_mode: Interpolation mode
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Making head look at ({x}, {y}, {z}) in {frame} frame over {duration}s")
        
        # Compute approximate joint positions based on look_at point
        # This is a simplified version - real implementation would use proper kinematics
        roll = 0.0
        pitch = 0.2 if z > 0 else -0.2
        yaw = 0.3 if y > 0 else -0.3
        
        # Call goto with computed positions
        return self.goto([roll, pitch, yaw], duration, interpolation_mode, wait)
    
    def rotate_by(self,
                  roll: float,
                  pitch: float,
                  yaw: float,
                  frame: str = "robot",
                  duration: float = 1.0,
                  interpolation_mode: str = "minimum_jerk",
                  wait: bool = True) -> bool:
        """
        Rotate the head by the specified angles.
        
        Args:
            roll: Roll angle in degrees
            pitch: Pitch angle in degrees
            yaw: Yaw angle in degrees
            frame: Reference frame ("robot" or "head")
            duration: Duration of the movement in seconds
            interpolation_mode: Interpolation mode
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Rotating head by ({roll}, {pitch}, {yaw}) degrees in {frame} frame")
        
        # Convert to radians and add to current positions
        roll_rad = roll * np.pi / 180.0
        pitch_rad = pitch * np.pi / 180.0
        yaw_rad = yaw * np.pi / 180.0
        
        new_positions = [
            self.current_positions[0] + roll_rad,
            self.current_positions[1] + pitch_rad,
            self.current_positions[2] + yaw_rad
        ]
        
        # Call goto with computed positions
        return self.goto(new_positions, duration, interpolation_mode, wait)
    
    def goto(self, 
             positions: List[float], 
             duration: float = 1.0, 
             interpolation_mode: str = "minimum_jerk",
             wait: bool = True) -> bool:
        """
        Move the head to the specified joint positions.
        
        Args:
            positions: List of joint positions in radians
            duration: Duration of the movement in seconds
            interpolation_mode: Interpolation mode
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Moving head to {positions} over {duration}s using {interpolation_mode}")
        
        if len(positions) != len(self.joint_names):
            logger.error(f"Expected {len(self.joint_names)} positions, got {len(positions)}")
            return False
        
        # Set target positions
        self.target_positions = positions.copy()
        self.moving = True
        
        # Simulate movement
        def _simulate_movement():
            time.sleep(duration)
            self.current_positions = self.target_positions.copy()
            self.moving = False
            logger.info(f"Head movement completed")
        
        # Start movement thread
        movement_thread = threading.Thread(target=_simulate_movement)
        movement_thread.daemon = True
        movement_thread.start()
        
        # Wait if requested
        if wait:
            movement_thread.join()
        
        return True
    
    def get_current_positions(self) -> Dict[str, float]:
        """
        Get the current positions of the head joints.
        
        Returns:
            Dict[str, float]: Dictionary mapping joint names to positions in radians
        """
        return dict(zip(self.joint_names, self.current_positions))


class MockMobileBase:
    """Mock implementation of the Reachy mobile base."""
    
    def __init__(self):
        """Initialize a mock mobile base."""
        # Current state (x, y, theta)
        self.current_position = [0.0, 0.0, 0.0]  # Origin, facing forward
        self.target_position = self.current_position.copy()
        self.moving = False
    
    def move_to(self,
                x: float,
                y: float,
                theta: float,
                duration: float = 3.0,
                wait: bool = True) -> bool:
        """
        Move the base to a target position and orientation.
        
        Args:
            x: X coordinate in meters
            y: Y coordinate in meters
            theta: Orientation in degrees
            duration: Duration of the movement in seconds
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Moving base to position ({x}, {y}, {theta}) over {duration}s")
        
        # Set target position
        self.target_position = [x, y, theta]
        self.moving = True
        
        # Simulate movement
        def _simulate_movement():
            time.sleep(duration)
            self.current_position = self.target_position.copy()
            self.moving = False
            logger.info(f"Base movement completed")
        
        # Start movement thread
        movement_thread = threading.Thread(target=_simulate_movement)
        movement_thread.daemon = True
        movement_thread.start()
        
        # Wait if requested
        if wait:
            movement_thread.join()
        
        return True
    
    def translate(self,
                  x: float,
                  y: float,
                  duration: float = 2.0,
                  wait: bool = True) -> bool:
        """
        Translate the base by the specified distances.
        
        Args:
            x: X distance in meters (forward)
            y: Y distance in meters (left)
            duration: Duration of the movement in seconds
            wait: Whether to wait for the movement to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Translating base by ({x}, {y}) meters over {duration}s")
        
        # Compute new position
        new_x = self.current_position[0] + x
        new_y = self.current_position[1] + y
        theta = self.current_position[2]
        
        # Call move_to with computed position
        return self.move_to(new_x, new_y, theta, duration, wait)
    
    def get_position(self) -> Dict[str, float]:
        """
        Get the current position and orientation of the base.
        
        Returns:
            Dict[str, float]: Dictionary with x, y, and theta values
        """
        return {
            "x": self.current_position[0],
            "y": self.current_position[1],
            "theta": self.current_position[2]
        }


class MockCamera:
    """Mock implementation of a Reachy camera."""
    
    def __init__(self, name: str, resolution: Tuple[int, int]):
        """
        Initialize a mock camera.
        
        Args:
            name: Name of the camera
            resolution: Resolution of the camera (width, height)
        """
        self.name = name
        self.resolution = resolution
        self.is_depth = name == "depth"
        self.fps = 30
        
    def get_frame(self) -> np.ndarray:
        """
        Get a frame from the camera.
        
        Returns:
            np.ndarray: Image frame (RGB or depth)
        """
        width, height = self.resolution
        
        if self.is_depth:
            # Generate a simple depth image (grayscale)
            image = np.zeros((height, width), dtype=np.float32)
            
            # Add a gradient and some random noise
            x = np.linspace(0, 1, width)
            y = np.linspace(0, 1, height)
            xx, yy = np.meshgrid(x, y)
            image = 5 + 3 * np.sin(xx * 5) * np.cos(yy * 5)
            image += np.random.normal(0, 0.1, (height, width))
        else:
            # Generate a simple RGB image
            image = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add a gradient and a circle
            x = np.linspace(0, 1, width)
            y = np.linspace(0, 1, height)
            xx, yy = np.meshgrid(x, y)
            
            # Create a background gradient
            image[:,:,0] = np.uint8(255 * xx)
            image[:,:,1] = np.uint8(255 * (1 - xx) * yy)
            image[:,:,2] = np.uint8(255 * yy)
            
            # Add a circle
            center_x = width // 2
            center_y = height // 2
            radius = min(width, height) // 4
            
            # Distance from each pixel to the center
            dist = np.sqrt((xx * width - center_x) ** 2 + (yy * height - center_y) ** 2)
            
            # Pixels inside the circle
            circle_mask = dist < radius
            image[circle_mask] = [255, 0, 0]  # Red circle
        
        return image
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the camera.
        
        Returns:
            Dict[str, Any]: Camera information
        """
        return {
            "name": self.name,
            "resolution": self.resolution,
            "fps": self.fps,
            "is_depth": self.is_depth,
            "intrinsics": {
                "fx": 500.0,
                "fy": 500.0,
                "cx": self.resolution[0] / 2,
                "cy": self.resolution[1] / 2
            } if not self.is_depth else {
                "fx": 400.0,
                "fy": 400.0,
                "cx": self.resolution[0] / 2,
                "cy": self.resolution[1] / 2
            }
        }


class MockAudio:
    """Mock implementation of Reachy audio capabilities."""
    
    def __init__(self):
        """Initialize mock audio capabilities."""
        self.recording = False
        self.playing = False
    
    def play(self, file_path: str, wait: bool = True) -> bool:
        """
        Play an audio file.
        
        Args:
            file_path: Path to the audio file
            wait: Whether to wait for playback to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            return False
        
        logger.info(f"Playing audio file: {file_path}")
        self.playing = True
        
        # Simulate playback
        def _simulate_playback():
            # Assume a fixed duration for simplicity
            duration = 3.0
            time.sleep(duration)
            self.playing = False
            logger.info(f"Audio playback completed")
        
        # Start playback thread
        playback_thread = threading.Thread(target=_simulate_playback)
        playback_thread.daemon = True
        playback_thread.start()
        
        # Wait if requested
        if wait:
            playback_thread.join()
        
        return True
    
    def record(self, file_path: str, duration: float) -> bool:
        """
        Record audio to a file.
        
        Args:
            file_path: Path to save the audio file
            duration: Duration of recording in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            logger.error(f"Error creating directory for audio file: {e}")
            return False
        
        logger.info(f"Recording audio to file: {file_path} for {duration} seconds")
        self.recording = True
        
        # Simulate recording
        time.sleep(duration)
        
        # Create an empty file
        try:
            with open(file_path, 'w') as f:
                f.write("Mock audio data")
        except Exception as e:
            logger.error(f"Error writing audio file: {e}")
            return False
        
        self.recording = False
        logger.info(f"Audio recording completed")
        return True


class MockReachyVisualizer:
    """Visualizer for the mock Reachy robot state."""
    
    def __init__(self, mock_reachy: MockReachy):
        """
        Initialize the visualizer.
        
        Args:
            mock_reachy: Mock Reachy instance to visualize
        """
        self.reachy = mock_reachy
        self.figure = None
        self.axes = None
        
    def create_visualization(self) -> Figure:
        """
        Create a visualization of the robot state.
        
        Returns:
            Figure: Matplotlib figure
        """
        self.figure = plt.figure(figsize=(12, 8))
        
        # Create subplots
        ax1 = self.figure.add_subplot(221, projection='3d')  # 3D robot visualization
        ax2 = self.figure.add_subplot(222)                   # Camera view
        ax3 = self.figure.add_subplot(223)                   # Arm joint angles
        ax4 = self.figure.add_subplot(224)                   # Head and mobile base
        
        self.axes = {
            "robot_3d": ax1,
            "camera": ax2,
            "joints": ax3,
            "head_base": ax4
        }
        
        # Setup 3D visualization
        ax1.set_title("Robot 3D Visualization")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")
        ax1.set_xlim([-0.5, 0.5])
        ax1.set_ylim([-0.5, 0.5])
        ax1.set_zlim([0, 1.0])
        
        # Setup camera view
        ax2.set_title("Camera View")
        ax2.axis('off')
        
        # Setup joint angles view
        ax3.set_title("Arm Joint Angles")
        ax3.set_xlabel("Joint")
        ax3.set_ylabel("Angle (rad)")
        ax3.set_ylim([-3.14, 3.14])
        
        # Setup head and mobile base view
        ax4.set_title("Head & Mobile Base")
        ax4.set_xlabel("X (m)")
        ax4.set_ylabel("Y (m)")
        ax4.set_xlim([-2, 2])
        ax4.set_ylim([-2, 2])
        
        # Update with initial state
        self.update_visualization()
        
        return self.figure
    
    def update_visualization(self) -> None:
        """Update the visualization with the current robot state."""
        if self.figure is None or self.axes is None:
            self.create_visualization()
        
        # Clear axes
        for ax in self.axes.values():
            ax.clear()
        
        # Update 3D robot visualization
        ax1 = self.axes["robot_3d"]
        ax1.set_title("Robot 3D Visualization")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")
        ax1.set_xlim([-0.5, 0.5])
        ax1.set_ylim([-0.5, 0.5])
        ax1.set_zlim([0, 1.0])
        
        # Draw robot base
        ax1.plot([0, 0], [0, 0], [0, 0.5], 'k-', linewidth=2)  # Torso
        
        # Draw arms
        for side, arm in self.reachy.arms.items():
            # Get arm position from forward kinematics
            pose = arm.forward_kinematics()
            
            # Draw arm line
            if side == "left":
                ax1.plot([0, pose[0, 3]], [0, pose[1, 3]], [0.5, pose[2, 3]], 'b-', linewidth=2)
                ax1.scatter(pose[0, 3], pose[1, 3], pose[2, 3], color='b', s=50, label=f"{side} arm")
            else:
                ax1.plot([0, pose[0, 3]], [0, pose[1, 3]], [0.5, pose[2, 3]], 'r-', linewidth=2)
                ax1.scatter(pose[0, 3], pose[1, 3], pose[2, 3], color='r', s=50, label=f"{side} arm")
        
        # Draw head
        head_pos = [0, 0, 0.6]  # Fixed position
        head_roll, head_pitch, head_yaw = self.reachy.head.current_positions
        
        # Simplified visualization of head orientation
        length = 0.2
        dx = length * np.cos(head_yaw) * np.cos(head_pitch)
        dy = length * np.sin(head_yaw) * np.cos(head_pitch)
        dz = length * np.sin(head_pitch)
        
        ax1.plot([head_pos[0], head_pos[0] + dx],
                 [head_pos[1], head_pos[1] + dy],
                 [head_pos[2], head_pos[2] + dz], 'g-', linewidth=2)
        ax1.scatter(head_pos[0], head_pos[1], head_pos[2], color='g', s=80, label="head")
        
        ax1.legend()
        
        # Update camera view
        ax2 = self.axes["camera"]
        ax2.set_title("Camera View (teleop)")
        ax2.axis('off')
        
        # Get and display camera frame
        camera_frame = self.reachy.cameras["teleop"].get_frame()
        ax2.imshow(camera_frame)
        
        # Update joint angles view
        ax3 = self.axes["joints"]
        ax3.set_title("Arm Joint Angles")
        ax3.set_xlabel("Joint")
        ax3.set_ylabel("Angle (rad)")
        ax3.set_ylim([-3.14, 3.14])
        
        # Plot left and right arm joint angles
        left_positions = self.reachy.arms["left"].current_positions
        right_positions = self.reachy.arms["right"].current_positions
        
        joint_indices = range(len(left_positions))
        joint_labels = ["S.Pitch", "S.Roll", "A.Yaw", "E.Pitch", "F.Yaw", "W.Pitch", "W.Roll"]
        
        ax3.bar([i - 0.2 for i in joint_indices], left_positions, width=0.4, color='b', alpha=0.7, label="Left Arm")
        ax3.bar([i + 0.2 for i in joint_indices], right_positions, width=0.4, color='r', alpha=0.7, label="Right Arm")
        ax3.set_xticks(joint_indices)
        ax3.set_xticklabels(joint_labels, rotation=45)
        ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax3.legend()
        
        # Update head and mobile base view
        ax4 = self.axes["head_base"]
        ax4.set_title("Head & Mobile Base")
        ax4.set_xlabel("X (m)")
        ax4.set_ylabel("Y (m)")
        ax4.set_xlim([-2, 2])
        ax4.set_ylim([-2, 2])
        
        # Plot mobile base position and orientation
        if self.reachy.mobile_base:
            pos = self.reachy.mobile_base.current_position
            x, y, theta = pos[0], pos[1], pos[2] * np.pi / 180.0
            
            # Draw triangle for mobile base
            base_size = 0.3
            vertices = np.array([
                [x + base_size * np.cos(theta), y + base_size * np.sin(theta)],
                [x + base_size * np.cos(theta + 2.5), y + base_size * np.sin(theta + 2.5)],
                [x + base_size * np.cos(theta - 2.5), y + base_size * np.sin(theta - 2.5)]
            ])
            
            ax4.add_patch(plt.Polygon(vertices, closed=True, fill=True, color='purple', alpha=0.7))
            
            # Draw direction indicator
            ax4.arrow(x, y, 0.5 * np.cos(theta), 0.5 * np.sin(theta), 
                      head_width=0.1, head_length=0.2, fc='k', ec='k')
            
            ax4.text(x + 0.2, y + 0.2, f"({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}°)")
        
        # Plot head orientation
        head_roll, head_pitch, head_yaw = self.reachy.head.current_positions
        ax4.text(-1.8, 1.8, f"Head: Roll={head_roll:.2f}, Pitch={head_pitch:.2f}, Yaw={head_yaw:.2f}")
        
        # Update figure
        self.figure.tight_layout()
        self.figure.canvas.draw_idle()


# Helper function to get a mock Reachy instance
def get_mock_reachy(host: str = "localhost", use_virtual: bool = True) -> MockReachy:
    """
    Get a mock Reachy instance.
    
    Args:
        host: Hostname for the robot
        use_virtual: Whether to use a virtual robot
        
    Returns:
        MockReachy: Mock Reachy instance
    """
    return MockReachy(host=host, use_virtual=use_virtual)


# For direct import
if __name__ == "__main__":
    # Example usage
    reachy = MockReachy()
    print(f"Mock Reachy initialized: {reachy.get_info()}")
    
    # Move an arm
    reachy.arms["right"].goto([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], wait=True)
    
    # Look at a point
    reachy.head.look_at(0.5, 0.3, 0.2, wait=True)
    
    # Close connection
    reachy.close() 