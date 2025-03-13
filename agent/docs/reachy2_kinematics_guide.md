# Reachy2 Arm Kinematics Guide

This guide provides a conceptual understanding of Reachy2's arm kinematics, focusing on spatial awareness and body representation rather than implementation details.

## Spatial Awareness and Body Representation

Reachy2 exists in 3D space with a well-defined coordinate system from its perspective:

- **X-axis**: Extends forward from Reachy's chest (positive values are in front of the robot)
- **Y-axis**: Runs from right to left across Reachy's body (positive values are to its left)
- **Z-axis**: Points upward (positive values are above the robot)
- **Origin**: Located between Reachy's shoulders, at the center of its upper torso

Units are in meters. For example, the point (0.3, -0.2, 0) represents a position 30cm in front of the robot, 20cm to its right, and at the same height as the origin.

## Understanding Reachy's Arms

Each of Reachy's arms has 7 degrees of freedom (7 motors), similar to a human arm:

- **Shoulder**: 3 degrees of freedom (pitch, roll, yaw), allowing for a wide range of movements
- **Elbow**: 2 degrees of freedom (pitch, yaw), enabling bending and rotation
- **Wrist**: 2 degrees of freedom (pitch, roll), providing dexterity for the end-effector

This design allows Reachy to reach points in its workspace with different arm configurations, similar to how humans can reach the same point with different arm postures.

## Joint Names, Directions, and Limits

Understanding how each joint moves is crucial for generating natural and effective movements. Here's a detailed breakdown of each joint:

### Right Arm Joints

1. **r_shoulder_pitch**: Controls up/down movement of the shoulder
   - Positive values: Arm moves backward (behind the robot)
   - Negative values: Arm moves forward (in front of the robot)
   - Zero position: Arm points straight down
   - Approximate limits: -180° to 90°

2. **r_shoulder_roll**: Controls inward/outward movement of the shoulder
   - Positive values: Arm moves inward (across the body)
   - Negative values: Arm moves outward (away from the body)
   - Zero position: Arm hangs naturally at the side
   - Approximate limits: -180° to 10°

3. **r_arm_yaw**: Controls rotation of the upper arm around its long axis
   - Positive values: Arm rotates inward
   - Negative values: Arm rotates outward
   - Zero position: Neutral rotation
   - Approximate limits: -90° to 90°

4. **r_elbow_pitch**: Controls bending of the elbow
   - Positive values: Not typically used (would bend backward if possible)
   - Negative values: Elbow bends (bringing forearm closer to upper arm)
   - Zero position: Arm is straight
   - Approximate limits: -125° to 0°

5. **r_forearm_yaw**: Controls rotation of the forearm
   - Positive values: Forearm rotates inward
   - Negative values: Forearm rotates outward
   - Zero position: Neutral rotation
   - Approximate limits: -100° to 100°

6. **r_wrist_pitch**: Controls up/down movement of the wrist
   - Positive values: Wrist bends upward
   - Negative values: Wrist bends downward
   - Zero position: Wrist is straight
   - Approximate limits: -45° to 45°

7. **r_wrist_roll**: Controls rotation of the wrist
   - Positive values: Wrist rotates inward
   - Negative values: Wrist rotates outward
   - Zero position: Neutral rotation
   - Approximate limits: -45° to 45°

### Left Arm Joints

The left arm joints follow similar patterns but with some reversed directions to maintain symmetry:

1. **l_shoulder_pitch**: Controls up/down movement of the shoulder
   - Positive values: Arm moves backward (behind the robot)
   - Negative values: Arm moves forward (in front of the robot)
   - Zero position: Arm points straight down
   - Approximate limits: -180° to 90°

2. **l_shoulder_roll**: Controls inward/outward movement of the shoulder
   - Positive values: Arm moves outward (away from the body)
   - Negative values: Arm moves inward (across the body)
   - Zero position: Arm hangs naturally at the side
   - Approximate limits: -10° to 180°

3. **l_arm_yaw**: Controls rotation of the upper arm around its long axis
   - Positive values: Arm rotates inward
   - Negative values: Arm rotates outward
   - Zero position: Neutral rotation
   - Approximate limits: -90° to 90°

4. **l_elbow_pitch**: Controls bending of the elbow
   - Positive values: Elbow bends (bringing forearm closer to upper arm)
   - Negative values: Not typically used (would bend backward if possible)
   - Zero position: Arm is straight
   - Approximate limits: 0° to 125°

5. **l_forearm_yaw**: Controls rotation of the forearm
   - Positive values: Forearm rotates inward
   - Negative values: Forearm rotates outward
   - Zero position: Neutral rotation
   - Approximate limits: -100° to 100°

6. **l_wrist_pitch**: Controls up/down movement of the wrist
   - Positive values: Wrist bends upward
   - Negative values: Wrist bends downward
   - Zero position: Wrist is straight
   - Approximate limits: -45° to 45°

7. **l_wrist_roll**: Controls rotation of the wrist
   - Positive values: Wrist rotates inward
   - Negative values: Wrist rotates outward
   - Zero position: Neutral rotation
   - Approximate limits: -45° to 45°

## Common Movement Patterns

Here are some common movement patterns and how they map to joint configurations:

### Lifting Arm Upward (Toward the Sky)
To lift the arm straight up above the shoulder:
- **Primary joints**: shoulder_pitch (negative values), shoulder_roll (near zero)
- **Example (right arm)**: r_shoulder_pitch: -90°, r_shoulder_roll: 0°
- This creates an upward movement where the arm points toward the ceiling

### Reaching Forward
To extend the arm forward in front of the robot:
- **Primary joints**: shoulder_pitch (negative values), elbow_pitch (negative for right, positive for left)
- **Example (right arm)**: r_shoulder_pitch: -90°, r_elbow_pitch: -10°
- This creates a forward-reaching movement where the arm extends in front of the robot

### Reaching to the Side
To extend the arm out to the side:
- **Primary joints**: shoulder_roll (negative for right, positive for left)
- **Example (right arm)**: r_shoulder_roll: -90°
- This creates a lateral movement where the arm extends away from the body

### Bending the Elbow
To create a bent elbow position:
- **Primary joints**: elbow_pitch (negative for right, positive for left)
- **Example (right arm)**: r_elbow_pitch: -90°
- This bends the elbow to a right angle

### Waving Motion
To create a waving motion:
- **Primary joints**: shoulder_roll, wrist_pitch
- **Example (right arm)**: r_shoulder_roll: -45°, then oscillate r_wrist_pitch between -30° and 30°
- This creates a natural waving motion with the arm partially extended

### Pointing Gesture
To point at something:
- **Primary joints**: shoulder_pitch, shoulder_roll, elbow_pitch, wrist_pitch
- **Example (right arm)**: r_shoulder_pitch: -45°, r_shoulder_roll: -30°, r_elbow_pitch: -45°, r_wrist_pitch: 0°
- This creates a pointing gesture with the arm partially extended

## Kinematic Concepts

### Joint Space vs. Cartesian Space

There are two fundamental ways to think about the position of Reachy's arms:

- **Joint Space**: Refers to the angles of each motor in the arm
- **Cartesian Space**: Refers to the 3D position (x,y,z) and orientation of the end-effector

Humans naturally think in Cartesian space ("reach for the cup at this location"), while robots operate in joint space (specific motor angles). Kinematics provides the mathematical relationship between these two spaces.

### Forward Kinematics

Forward kinematics transforms joint angles into the end-effector's position and orientation.

- **Purpose**: Answers the question: "If I set these joint angles, where will the hand be?"
- **Characteristics**:
  - Always has a single, deterministic solution
  - Represented as a 4x4 matrix combining position (translation) and orientation (rotation)
  - The top-left 3x3 submatrix represents orientation
  - The top-right 3x1 vector represents position

```python
# Simple example of forward kinematics
current_pose = reachy.r_arm.forward_kinematics()
```

### Inverse Kinematics

Inverse kinematics transforms a desired end-effector position and orientation into the required joint angles.

- **Purpose**: Answers the question: "To reach this point in space, how should I configure my joints?"
- **Characteristics**:
  - May have multiple solutions (different arm configurations can reach the same point)
  - May have no solution (point is unreachable)
  - Requires an initial configuration (q0) as a starting point for the solution
  - More computationally complex than forward kinematics

```python
# Simple example of inverse kinematics
joint_angles = reachy.r_arm.inverse_kinematics(target_pose, q0=initial_guess)
```

### Workspace and Reachability

Not all points in 3D space are reachable by Reachy's arms:

- The reachable workspace is roughly a sphere around the shoulder, limited by arm length
- Joint limits further constrain the reachable workspace
- Some positions may be reachable but with limited orientation options
- The workspace of the left and right arms overlap in front of the robot

### Singularities

Singularities are special configurations where the arm loses one degree of freedom:

- **Examples**: Fully extended arm, or when two rotation axes align
- **Consequences**: Near singularities, small changes in position require large joint movements
- **Challenges**: Inverse kinematics algorithms may struggle near singularities

## Practical Understanding

When planning movements for Reachy, consider these important factors:

- **Initial Configuration**: The starting position of the arm affects which solution the inverse kinematics will find
- **Cartesian Movements**: Moving in straight lines in Cartesian space requires continuous recalculation of joint angles
- **Orientation Importance**: Orientation matters as much as position for many tasks (e.g., grasping objects)
- **Movement Smoothness**: Smooth movements require appropriate timing and acceleration profiles
- **Reachability**: Always check if a target position is within the robot's workspace

## Embodied Understanding

Think of Reachy's arms as similar to human arms, with some key differences:

- Reachy can rotate some joints in ways humans cannot
- Reachy has fixed joint limits that cannot be exceeded
- Reachy's perception of its body comes from encoders in the motors, not proprioception
- Reachy doesn't automatically avoid obstacles or self-collisions

When generating movements, imagine yourself as the robot and consider:
- How would you position your arm to reach that point?
- What would be a natural, efficient way to move from one position to another?
- How would you orient your hand to grasp an object effectively?

## Movement Guidelines

When generating code for robot movements, always apply these principles:

1. **Think Spatially**: Consider the 3D position and orientation of the end-effector in relation to the robot's body and the target. Visualize the movement in 3D space before coding it.

2. **Check Reachability**: Ensure target positions are within the robot's workspace before attempting movements. Not all points in space can be reached, and attempting to reach unreachable positions will result in errors or unexpected behavior.

3. **Prefer Natural Movements**: Generate movement patterns that follow natural, efficient paths similar to human movements. This typically means smooth, curved trajectories rather than rigid, angular movements.

4. **Maintain Orientation Awareness**: Pay attention to both position AND orientation of the end-effector for effective interaction. The orientation of the hand is often as important as its position, especially for grasping or manipulation tasks.

5. **Avoid Singularities**: Plan paths that avoid fully extended arm positions or aligned rotation axes. Near singularities, small changes in position require large joint movements, which can lead to jerky or unpredictable motion.

6. **Consider Starting Configuration**: The initial arm position significantly affects the solution found by inverse kinematics. Different starting positions can lead to different arm configurations to reach the same target.

7. **Provide Sufficient Time**: Allow adequate duration for movements to ensure smoothness and safety. Faster movements require more precise control and can be more dangerous.

8. **Implement Error Handling**: Always include error handling for kinematics operations, as they may fail to find solutions for certain targets or configurations.

9. **Test Incrementally**: When developing complex movements, test each component incrementally to ensure the robot behaves as expected at each step.

10. **Use Try/Finally Blocks**: Ensure proper cleanup (turning off motors smoothly and disconnecting) even if errors occur during movement execution.

## Common Pitfalls

1. **Unreachable Targets**: Requesting positions outside the workspace
2. **Singularities**: Creating movements that pass through or near singularities
3. **Joint Limits**: Ignoring the physical limitations of the robot's joints
4. **Orientation Neglect**: Focusing only on position while neglecting orientation
5. **Abrupt Movements**: Not providing enough time for smooth transitions between positions

## References

- [Reachy2 SDK Documentation](https://pollen-robotics.github.io/reachy2-docs/)
- [Forward and Inverse Kinematics](https://docs.pollen-robotics.com/sdk/first-moves/kinematics/)
- [Controlling the Arm](https://docs.pollen-robotics.com/sdk/first-moves/controlling-arm/) 