#!/usr/bin/env python
"""
Test script to verify that the agent can properly connect to the virtual Reachy.

This script tests:
1. Connection to the virtual Reachy (running in a Docker container on localhost)
2. Basic tool discovery and registration
3. Simple tool execution

Note: The virtual Reachy uses the exact same API as a physical robot - the only
difference is that it's running in a Docker container on localhost instead of
connecting to a physical robot's IP address.
"""

import os
import sys
import logging
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_virtual_reachy")

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_connection():
    """Test connection to the virtual Reachy running in Docker."""
    logger.info("Testing connection to virtual Reachy (Docker container)...")
    
    try:
        from agent.tools.connection_manager import connect_to_reachy, disconnect_reachy, get_connection_info
        
        # Connect to virtual Reachy - this connects to the Docker container on localhost
        # using the same SDK as would be used for a physical robot
        reachy = connect_to_reachy(host="localhost")
        
        # Get connection info
        info = get_connection_info()
        logger.info(f"Connection info: {info}")
        
        # Test if the connection is virtual
        from agent.tools.connection_manager import is_virtual
        assert is_virtual(), "Connection should be virtual"
        
        # Get basic robot info - this API call is identical for both virtual and physical robots
        robot_info = reachy.get_info()
        logger.info(f"Robot info: {robot_info}")
        
        # Test successful
        logger.info("✅ Connection test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    finally:
        # Always try to disconnect
        try:
            disconnect_reachy()
        except:
            pass

def test_agent_initialization():
    """Test agent initialization with virtual Reachy."""
    logger.info("Testing agent initialization with virtual Reachy...")
    
    try:
        from agent.langgraph_agent import ReachyLangGraphAgent
        
        # Initialize agent
        agent = ReachyLangGraphAgent(model="gpt-4-turbo")
        
        # Check if tools were loaded
        tools = agent.get_available_tools()
        logger.info(f"Loaded {len(tools)} tools")
        
        # Verify that at least some tools were loaded
        assert len(tools) > 0, "No tools were loaded"
        
        # Test successful
        logger.info("✅ Agent initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent initialization test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_basic_tool_execution():
    """Test basic tool execution with virtual Reachy."""
    logger.info("Testing basic tool execution with virtual Reachy...")
    
    try:
        from agent.tools.connection_manager import connect_to_reachy, disconnect_reachy
        
        # Connect to virtual Reachy
        reachy = connect_to_reachy(host="localhost")
        
        # Test getting arm positions
        logger.info("Testing get_arm_position...")
        left_positions = reachy.arms["left"].get_current_positions()
        logger.info(f"Left arm positions: {left_positions}")
        
        # Test head movement
        logger.info("Testing head.look_at...")
        reachy.head.look_at(0.5, 0.3, 0.2, wait=True)
        
        # Test camera
        logger.info("Testing camera.get_frame...")
        if hasattr(reachy, "cameras") and "teleop" in reachy.cameras:
            frame = reachy.cameras["teleop"].get_frame()
            logger.info(f"Camera frame shape: {frame.shape if frame is not None else None}")
        
        # Test successful
        logger.info("✅ Basic tool execution test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Basic tool execution test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    finally:
        # Always try to disconnect
        try:
            disconnect_reachy()
        except:
            pass

def test_agent_tool_execution():
    """Test tool execution through the agent with virtual Reachy."""
    logger.info("Testing tool execution through the agent...")
    
    try:
        from agent.langgraph_agent import ReachyLangGraphAgent
        
        # Initialize agent
        agent = ReachyLangGraphAgent(model="gpt-4-turbo")
        
        # Process a simple message that should trigger tool execution
        response = agent.process_message("What is the current position of the left arm?")
        
        # Check if the response contains the expected fields
        logger.info(f"Response keys: {response.keys()}")
        assert "message" in response, "Response should contain a message field"
        assert "tool_calls" in response, "Response should contain tool_calls field"
        
        # Log the tool calls
        logger.info(f"Tool calls: {response['tool_calls']}")
        
        # Test successful
        logger.info("✅ Agent tool execution test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent tool execution test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def run_all_tests():
    """Run all tests."""
    tests = [
        test_connection,
        test_agent_initialization,
        test_basic_tool_execution,
        test_agent_tool_execution
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{i+1}. {test.__name__}: {status}")
    
    # Overall result
    if all(results):
        logger.info("\n🎉 All tests passed! The virtual Reachy integration is working correctly.")
        return True
    else:
        logger.info("\n❌ Some tests failed. Please check the logs for details.")
        return False

if __name__ == "__main__":
    logger.info("Starting virtual Reachy tests...")
    success = run_all_tests()
    sys.exit(0 if success else 1) 