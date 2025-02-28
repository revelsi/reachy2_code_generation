"""
API Examples for Reachy 2 SDK

This file contains examples of correct API usage for the Reachy 2 SDK.
These examples are used to guide the code generation agent in producing correct code.
"""

# Example 1: Basic connection and cleanup
def example_connection():
    """Example of connecting to the robot and proper cleanup."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    # Connect to the robot
    reachy = ReachySDK(host="localhost")
    
    try:
        # Your code here
        pass
    finally:
        # Always disconnect and turn off motors
        reachy.turn_off()
        reachy.disconnect()

# Example 2: Accessing robot parts (properties, not methods)
def example_accessing_parts():
    """Example of accessing robot parts (properties, not methods)."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    reachy = ReachySDK(host="localhost")
    
    try:
        # CORRECT: Access parts as properties
        right_arm = reachy.r_arm  # This is a property, not a method
        left_arm = reachy.l_arm   # This is a property, not a method
        head = reachy.head        # This is a property, not a method
        
        # INCORRECT: Do NOT use these
        # right_arm = reachy.r_arm()  # WRONG! This is not a method
        # left_arm = reachy.l_arm()   # WRONG! This is not a method
        # head = reachy.head()        # WRONG! This is not a method
    finally:
        reachy.turn_off()
        reachy.disconnect()

# Example 3: Moving the arm with goto
def example_arm_goto():
    """Example of moving the arm with goto."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    reachy = ReachySDK(host="localhost")
    
    try:
        # Access the right arm
        right_arm = reachy.r_arm
        
        # CORRECT: Move the arm to a joint position
        # The positions array must have exactly 7 values for the 7 joints
        joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 7 values for 7 joints
        right_arm.goto(
            joint_positions,
            duration=1.0,
            wait=True,
            interpolation_mode="minimum_jerk"
        )
        
        # INCORRECT: Do NOT use incorrect number of joint values
        # wrong_positions = [0.0, 0.0, 0.0]  # WRONG! Too few values
        # right_arm.goto(wrong_positions, duration=1.0, wait=True)
    finally:
        reachy.turn_off()
        reachy.disconnect()

# Example 4: Moving individual joints
def example_joint_goto():
    """Example of moving individual joints."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    reachy = ReachySDK(host="localhost")
    
    try:
        # Access individual joints
        r_shoulder_pitch = reachy.r_arm.r_shoulder_pitch
        r_shoulder_roll = reachy.r_arm.r_shoulder_roll
        r_arm_yaw = reachy.r_arm.r_arm_yaw
        r_elbow_pitch = reachy.r_arm.r_elbow_pitch
        r_forearm_yaw = reachy.r_arm.r_forearm_yaw
        r_wrist_pitch = reachy.r_arm.r_wrist_pitch
        r_wrist_roll = reachy.r_arm.r_wrist_roll
        
        # Move individual joints
        r_shoulder_pitch.goto(0.0, duration=1.0, wait=True)
        r_shoulder_roll.goto(-0.3, duration=1.0, wait=True)
        r_elbow_pitch.goto(-1.5, duration=1.0, wait=True)
    finally:
        reachy.turn_off()
        reachy.disconnect()

# Example 5: Using the head
def example_head():
    """Example of using the head."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    reachy = ReachySDK(host="localhost")
    
    try:
        # Access the head
        head = reachy.head
        
        # Look at a point in space (x, y, z coordinates)
        head.look_at(0.5, 0.3, 0.6, duration=1.0, wait=True)
    finally:
        reachy.turn_off()
        reachy.disconnect()

# Example 6: Using the gripper
def example_gripper():
    """Example of using the gripper."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    reachy = ReachySDK(host="localhost")
    
    try:
        # Access the left gripper
        left_gripper = reachy.l_arm.gripper
        
        # Open and close the gripper
        left_gripper.open()
        # Wait for the gripper to open
        import time
        time.sleep(1.0)
        
        left_gripper.close()
        # Wait for the gripper to close
        time.sleep(1.0)
    finally:
        reachy.turn_off()
        reachy.disconnect()

# Example 7: Playing audio
def example_audio():
    """Example of playing audio."""
    from reachy2_sdk.reachy_sdk import ReachySDK
    
    reachy = ReachySDK(host="localhost")
    
    try:
        # Play text using text-to-speech
        reachy.media.audio.play_text("Hello, world!")
    finally:
        reachy.disconnect() 