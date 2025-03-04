#!/usr/bin/env python
"""
Test script for the code generation agent with the enhanced API summary.

This script initializes the code generation agent with the enhanced API summary
and tests it with a sample query that requires detailed parameter information.
"""

import os
import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the agent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.code_generation_agent import ReachyCodeGenerationAgent

# Patch the WebSocket notification method to avoid errors
import types
def dummy_send_notification(self, response):
    """Dummy method to replace the WebSocket notification method"""
    pass

def main():
    """
    Main function to test the code generation agent with the enhanced API summary.
    """
    # Initialize the code generation agent
    logger.info("Initializing code generation agent...")
    agent = ReachyCodeGenerationAgent()
    
    # Patch the WebSocket notification method
    agent._send_websocket_notification = types.MethodType(dummy_send_notification, agent)
    
    # Test queries that require detailed parameter information
    test_queries = [
        "Move the right arm to a specific position with joint values [0, 0, 0, 0, 0, 0, 0] in degrees",
        "Initialize the robot with host 'localhost' and connect to it",
        "Make the robot look at a point in space at coordinates (0.5, 0.3, 0.2)"
    ]
    
    for i, query in enumerate(test_queries):
        logger.info(f"\n\nTesting query {i+1}: {query}")
        
        # Process the query
        response = agent.process_message(query)
        
        # Print the response
        logger.info("\nGenerated code:")
        logger.info(response["code"])
        
        # Print validation results
        logger.info("\nValidation results:")
        logger.info(f"Valid: {response['validation']['valid']}")
        if not response['validation']['valid']:
            logger.info("Errors:")
            for error in response['validation']['errors']:
                logger.info(f"- {error}")
        
        logger.info("Warnings:")
        for warning in response['validation'].get('warnings', []):
            logger.info(f"- {warning}")
        
        logger.info("\n" + "="*80)
    
    logger.info("\nTest completed.")

if __name__ == "__main__":
    main() 