#!/usr/bin/env python
"""
Interactive demonstration script for the virtual Reachy.

This script provides a simple interactive interface to test the virtual Reachy
functionality without needing to use the full agent.

Note: The virtual Reachy uses the exact same API as a physical robot - the only
difference is that it's running in a Docker container on localhost instead of
connecting to a physical robot's IP address.
"""

import os
import sys
import logging
import time
import argparse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("demo_virtual_reachy")

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def setup_virtual_reachy():
    """Set up and connect to the virtual Reachy running in Docker."""
    from agent.tools.connection_manager import connect_to_reachy, get_connection_info
    
    logger.info("Connecting to virtual Reachy (Docker container)...")
    reachy = connect_to_reachy(host="localhost")
    
    # Get connection info
    info = get_connection_info()
    logger.info(f"Connection info: {info}")
    
    return reachy

def print_available_commands():
    """Print the available commands for the demo."""
    print("\n=== Available Commands ===")
    print("1. arm - Get arm positions and move arms")
    print("2. head - Control head movements")
    print("3. gripper - Control grippers")
    print("4. camera - Access camera feeds")
    print("5. info - Get robot information")
    print("6. help - Show this help message")
    print("7. exit - Exit the demo")
    print("==========================\n")

def handle_arm_commands(reachy):
    """Handle arm-related commands."""
    print("\n=== Arm Commands ===")
    print("1. get_left - Get left arm positions")
    print("2. get_right - Get right arm positions")
    print("3. move_left - Move left arm to a position")
    print("4. move_right - Move right arm to a position")
    print("5. back - Return to main menu")
    
    while True:
        cmd = input("\nEnter arm command: ").strip().lower()
        
        if cmd == "back":
            break
        elif cmd == "get_left":
            positions = reachy.arms["left"].get_current_positions()
            print(f"Left arm positions: {positions}")
        elif cmd == "get_right":
            positions = reachy.arms["right"].get_current_positions()
            print(f"Right arm positions: {positions}")
        elif cmd == "move_left":
            try:
                print("Enter 7 joint positions (space-separated):")
                positions = list(map(float, input().strip().split()))
                if len(positions) != 7:
                    print("Error: Must provide exactly 7 positions")
                    continue
                reachy.arms["left"].goto(positions, wait=True)
                print("Left arm moved successfully")
            except Exception as e:
                print(f"Error moving left arm: {e}")
        elif cmd == "move_right":
            try:
                print("Enter 7 joint positions (space-separated):")
                positions = list(map(float, input().strip().split()))
                if len(positions) != 7:
                    print("Error: Must provide exactly 7 positions")
                    continue
                reachy.arms["right"].goto(positions, wait=True)
                print("Right arm moved successfully")
            except Exception as e:
                print(f"Error moving right arm: {e}")
        else:
            print("Unknown command")

def handle_head_commands(reachy):
    """Handle head-related commands."""
    print("\n=== Head Commands ===")
    print("1. get_position - Get head position")
    print("2. look_at - Make the head look at a point")
    print("3. move - Move head to a position")
    print("4. back - Return to main menu")
    
    while True:
        cmd = input("\nEnter head command: ").strip().lower()
        
        if cmd == "back":
            break
        elif cmd == "get_position":
            positions = reachy.head.get_current_positions()
            print(f"Head positions: {positions}")
        elif cmd == "look_at":
            try:
                print("Enter point coordinates (x y z):")
                x, y, z = map(float, input().strip().split())
                reachy.head.look_at(x, y, z, wait=True)
                print("Head moved successfully")
            except Exception as e:
                print(f"Error moving head: {e}")
        elif cmd == "move":
            try:
                print("Enter 3 joint positions (roll pitch yaw):")
                positions = list(map(float, input().strip().split()))
                if len(positions) != 3:
                    print("Error: Must provide exactly 3 positions")
                    continue
                reachy.head.goto(positions, wait=True)
                print("Head moved successfully")
            except Exception as e:
                print(f"Error moving head: {e}")
        else:
            print("Unknown command")

def handle_gripper_commands(reachy):
    """Handle gripper-related commands."""
    print("\n=== Gripper Commands ===")
    print("1. open_left - Open left gripper")
    print("2. close_left - Close left gripper")
    print("3. open_right - Open right gripper")
    print("4. close_right - Close right gripper")
    print("5. back - Return to main menu")
    
    while True:
        cmd = input("\nEnter gripper command: ").strip().lower()
        
        if cmd == "back":
            break
        elif cmd == "open_left":
            try:
                reachy.grippers["left"].open()
                print("Left gripper opened")
            except Exception as e:
                print(f"Error opening left gripper: {e}")
        elif cmd == "close_left":
            try:
                reachy.grippers["left"].close()
                print("Left gripper closed")
            except Exception as e:
                print(f"Error closing left gripper: {e}")
        elif cmd == "open_right":
            try:
                reachy.grippers["right"].open()
                print("Right gripper opened")
            except Exception as e:
                print(f"Error opening right gripper: {e}")
        elif cmd == "close_right":
            try:
                reachy.grippers["right"].close()
                print("Right gripper closed")
            except Exception as e:
                print(f"Error closing right gripper: {e}")
        else:
            print("Unknown command")

def handle_camera_commands(reachy):
    """Handle camera-related commands."""
    print("\n=== Camera Commands ===")
    print("1. list - List available cameras")
    print("2. get_frame - Get a frame from a camera")
    print("3. back - Return to main menu")
    
    while True:
        cmd = input("\nEnter camera command: ").strip().lower()
        
        if cmd == "back":
            break
        elif cmd == "list":
            if hasattr(reachy, "cameras"):
                print(f"Available cameras: {list(reachy.cameras.keys())}")
            else:
                print("No cameras available")
        elif cmd == "get_frame":
            try:
                if not hasattr(reachy, "cameras") or not reachy.cameras:
                    print("No cameras available")
                    continue
                    
                print(f"Available cameras: {list(reachy.cameras.keys())}")
                camera_name = input("Enter camera name: ").strip()
                
                if camera_name not in reachy.cameras:
                    print(f"Camera {camera_name} not found")
                    continue
                    
                frame = reachy.cameras[camera_name].get_frame()
                print(f"Got frame with shape: {frame.shape if frame is not None else None}")
                print("Note: In a real application, you would display or save this frame")
            except Exception as e:
                print(f"Error getting camera frame: {e}")
        else:
            print("Unknown command")

def handle_info_commands(reachy):
    """Handle information-related commands."""
    print("\n=== Info Commands ===")
    print("1. basic - Get basic robot information")
    print("2. detailed - Get detailed robot information")
    print("3. back - Return to main menu")
    
    while True:
        cmd = input("\nEnter info command: ").strip().lower()
        
        if cmd == "back":
            break
        elif cmd == "basic":
            try:
                info = reachy.get_info()
                print(f"Robot info: {info}")
            except Exception as e:
                print(f"Error getting robot info: {e}")
        elif cmd == "detailed":
            try:
                # Get connection info
                from agent.tools.connection_manager import get_connection_info
                conn_info = get_connection_info()
                print(f"Connection info: {conn_info}")
                
                # Get arm positions
                left_pos = reachy.arms["left"].get_current_positions()
                right_pos = reachy.arms["right"].get_current_positions()
                print(f"Left arm positions: {left_pos}")
                print(f"Right arm positions: {right_pos}")
                
                # Get head position
                head_pos = reachy.head.get_current_positions()
                print(f"Head positions: {head_pos}")
            except Exception as e:
                print(f"Error getting detailed info: {e}")
        else:
            print("Unknown command")

def main():
    """Main function for the demo."""
    parser = argparse.ArgumentParser(description="Virtual Reachy Demo")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("=== Virtual Reachy Demo ===")
    print("This demo allows you to interact with a virtual Reachy robot.")
    print("The virtual robot runs in a Docker container on localhost.")
    print("It uses the exact same API as a physical robot, making it perfect for development and testing.")
    
    try:
        # Connect to virtual Reachy
        reachy = setup_virtual_reachy()
        
        print("\nVirtual Reachy connected successfully!")
        print_available_commands()
        
        # Main command loop
        while True:
            cmd = input("Enter command: ").strip().lower()
            
            if cmd == "exit":
                break
            elif cmd == "help":
                print_available_commands()
            elif cmd == "arm":
                handle_arm_commands(reachy)
            elif cmd == "head":
                handle_head_commands(reachy)
            elif cmd == "gripper":
                handle_gripper_commands(reachy)
            elif cmd == "camera":
                handle_camera_commands(reachy)
            elif cmd == "info":
                handle_info_commands(reachy)
            else:
                print("Unknown command. Type 'help' for available commands.")
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # Disconnect from Reachy
        try:
            from agent.tools.connection_manager import disconnect_reachy
            disconnect_reachy()
            logger.info("Disconnected from virtual Reachy")
        except:
            pass
    
    print("Demo finished. Goodbye!")

if __name__ == "__main__":
    main() 