# Reachy2 Arm Positioning Guide

## CONTROLLING REACHY'S ARMS: TWO APPROACHES

There are two ways to control Reachy's arms using the `goto()` method:

### 1. JOINT SPACE CONTROL (RECOMMENDED FOR BEGINNERS)

Control the arm by specifying the angle for each joint:

```python
# Example: Position the right arm using joint angles (in degrees)
reachy.r_arm.goto([0, 10, -10, -90, 0, 0, 0], duration=1.0)
time.sleep(1.5)  # IMPORTANT: Always wait for movement to complete

# Example: Position the left arm using joint angles (in degrees)
reachy.l_arm.goto([0, -10, 10, -90, 0, 0, 0], duration=1.0)
time.sleep(1.5)  # IMPORTANT: Always wait for movement to complete
```

IMPORTANT: When using joint space control, ALWAYS provide EXACTLY 7 joint values for arms (or 3 for the head).

### 2. CARTESIAN SPACE CONTROL (FOR PRECISE POSITIONING)

Control the arm by specifying a target position in 3D space using a pose matrix:

```python
import numpy as np
import time

# Create a 4x4 pose matrix for the target position
target_pose = np.array([[1, 0, 0, 0.3],  # x = 0.3m (forward)
                         [0, 1, 0, -0.2], # y = -0.2m (to the right)
                         [0, 0, 1, 0.1],  # z = 0.1m (up)
                         [0, 0, 0, 1]])

# Move the arm to the target position
reachy.r_arm.goto(target_pose, duration=1.0)
time.sleep(1.5)  # IMPORTANT: Always wait for movement to complete
```

For more precise control, you can use inverse kinematics:

```python
import time

# Create a target pose matrix
target_pose = np.array([[1, 0, 0, 0.3],
                         [0, 1, 0, -0.2],
                         [0, 0, 1, 0.1],
                         [0, 0, 0, 1]])

# Calculate joint positions using inverse kinematics
joint_positions = reachy.r_arm.inverse_kinematics(target_pose)

# Move the arm to the calculated joint positions
reachy.r_arm.goto(joint_positions, duration=1.0)
time.sleep(1.5)  # IMPORTANT: Always wait for movement to complete
```

WARNING: The `goto()` method DOES NOT accept named parameters like `x`, `y`, `z`. It only accepts a list of joint angles or a 4x4 pose matrix.

INCORRECT: `reachy.r_arm.goto(x=0.3, y=-0.2, z=0.1, duration=1.0)`

### COORDINATE SYSTEM

Reachy's coordinate system from its perspective:
- X-axis: Forward from chest (positive = front)
- Y-axis: Right to left across body (positive = left)
- Z-axis: Upward (positive = above)
- Origin: Between shoulders, center of upper torso

Units are in meters. Example: (0.3, -0.2, 0.1) = 30cm in front, 20cm to right, 10cm above origin.

### PRACTICAL GUIDELINES

1. KEEP MOVEMENTS SIMPLE: Use direct paths between positions
2. USE REASONABLE DURATIONS: 1-2 seconds for most movements
3. STAY WITHIN REACH: Keep positions within ~0.6 meters of the robot's torso
4. AVOID EXTREME POSITIONS: Don't position arms at the limits of their reach
5. INCLUDE ERROR HANDLING: Always catch and handle exceptions
6. ADD SLEEP AFTER MOVEMENTS: The `goto()` method is non-blocking, so always add `time.sleep()` after movement commands to ensure they complete before the script exits
7. VERIFY REACHABILITY: Always check if a target pose is reachable before attempting to move to it

### ENSURING TARGET POSES ARE REACHABLE

To ensure a target pose is reachable before attempting to move to it, use the `inverse_kinematics` method with a try/except block:

```python
import numpy as np
import time

# Create a target pose matrix
target_pose = np.array([[1, 0, 0, 0.3],
                         [0, 1, 0, -0.2],
                         [0, 0, 1, 0.1],
                         [0, 0, 0, 1]])

# Check if the target pose is reachable before attempting to move
try:
    # Try to calculate joint positions using inverse kinematics
    joint_positions = reachy.r_arm.inverse_kinematics(target_pose)
    print("Target is reachable! Joint positions:", joint_positions)
    
    # If we get here, the target is reachable, so we can move to it
    reachy.r_arm.goto(joint_positions, duration=1.0)
    time.sleep(1.5)  # Wait for movement to complete
    
except ValueError as e:
    print(f"Target is not reachable: {e}")
    # Use a fallback position or strategy
    print("Using a fallback position instead...")
    reachy.r_arm.goto([0, 10, -10, -90, 0, 0, 0], duration=1.0)
    time.sleep(1.5)  # Wait for movement to complete
```



## COMMON TASKS

1. REACHING FORWARD:
   ```python
   # Using joint space control
   reachy.r_arm.goto([0, 0, 0, -90, 0, 0, 0], duration=1.0)
   time.sleep(1.5)  # Wait for movement to complete
   
   # Using cartesian space control
   target_pose = np.array([[1, 0, 0, 0.3],
                           [0, 1, 0, -0.2],
                           [0, 0, 1, 0.0],
                           [0, 0, 0, 1]])
   reachy.r_arm.goto(target_pose, duration=1.0)
   time.sleep(1.5)  # Wait for movement to complete
   ```

2. REACHING UPWARD:
   ```python
   # Using joint space control
   reachy.r_arm.goto([-45, 0, 0, -45, 0, 0, 0], duration=1.0)
   time.sleep(1.5)  # Wait for movement to complete
   
   # Using cartesian space control
   target_pose = np.array([[1, 0, 0, 0.2],
                           [0, 1, 0, -0.2],
                           [0, 0, 1, 0.3],
                           [0, 0, 0, 1]])
   reachy.r_arm.goto(target_pose, duration=1.0)
   time.sleep(1.5)  # Wait for movement to complete
   ```

3. RETURNING TO DEFAULT:
   ```python
   reachy.goto_posture('default')
   time.sleep(2.0)  # Wait for posture to complete
   ``` 