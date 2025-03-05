from reachy2_sdk.reachy_sdk import ReachySDK

# Connect to the robot
reachy = ReachySDK(host="localhost")

try:
    # Turn on the robot's systems
    reachy.turn_on()
    print("Reachy is now turned on and ready.")

finally:
    # Disconnect from the robot
    reachy.disconnect()