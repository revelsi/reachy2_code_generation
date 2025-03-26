#!/usr/bin/env python
"""
Test module for the Code Generation functionality.

This module contains tests for the code generation system, including:
- Prompt construction
- Code extraction
- Code validation
- Code execution (where possible)
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to load environment variables from .env file
load_dotenv()

from agent.code_generation_agent import ReachyCodeGenerationAgent
from agent.prompt_config import get_prompt_sections, get_default_prompt_order


class TestCodeGeneration(unittest.TestCase):
    """Test cases for the code generation system."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Skip tests if no API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise unittest.SkipTest("No OpenAI API key available")
        
        # Create a test agent
        cls.agent = ReachyCodeGenerationAgent(
            api_key=api_key,
            model="gpt-3.5-turbo",  # Use a cheaper model for testing
            temperature=0.0,  # Use 0 temperature for deterministic outputs
            max_tokens=1000
        )
    
    def test_prompt_construction(self):
        """Test that the system prompt is constructed correctly."""
        # Get the system prompt
        system_prompt = self.agent._build_system_prompt()
        
        # Verify that essential components are included
        self.assertIn("Reachy 2 robot", system_prompt)
        self.assertIn("Python code", system_prompt)
        
        # Check if all default sections are included
        prompt_sections = get_prompt_sections()
        for section_name in get_default_prompt_order():
            if section_name in prompt_sections:
                section_content = prompt_sections[section_name]
                self.assertIn(section_content[:50], system_prompt)
    
    @patch('agent.code_generation_agent.client.chat.completions.create')
    def test_code_extraction(self, mock_completion):
        """Test that code is correctly extracted from the model's response."""
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """
        Here's how you can make the right arm wave:
        
        ```python
        import time
        from reachy2_sdk import ReachySDK
        
        # Connect to the robot
        reachy = ReachySDK(host="localhost")
        
        # Wave the right arm
        reachy.arms["right"].set_stiffness(1.0)
        for i in range(3):
            reachy.arms["right"].set_target_position({"shoulder_pitch": -1.0})
            time.sleep(1)
            reachy.arms["right"].set_target_position({"shoulder_pitch": 0.0})
            time.sleep(1)
        
        # Reduce stiffness when done
        reachy.arms["right"].set_stiffness(0.0)
        ```
        
        This code will make the right arm wave up and down 3 times.
        """
        mock_completion.return_value = mock_response
        
        # Call the agent's generate_code method
        response = self.agent.generate_code("Make the right arm wave")
        
        # Verify that the code was extracted correctly
        self.assertIn("import time", response["code"])
        self.assertIn("ReachySDK", response["code"])
        self.assertIn("wave the right arm", response["code"].lower())
        
        # Check the structure of the response
        self.assertIn("code", response)
        self.assertIn("message", response)
        self.assertIn("raw_response", response)
    
    @patch('agent.code_generation_agent.client.chat.completions.create')
    def test_code_validation(self, mock_completion):
        """Test that code validation works correctly."""
        # Mock the OpenAI API response with valid code
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """
        ```python
        from reachy2_sdk import ReachySDK
        
        # Connect to the robot
        reachy = ReachySDK(host="localhost")
        
        # Get the battery level
        battery = reachy.get_battery_level()
        print(f"Battery level: {battery}%")
        ```
        """
        mock_completion.return_value = mock_response
        
        # Call the agent's generate_code method
        response = self.agent.generate_code("Get the battery level")
        
        # Validate the code
        validation = self.agent.validate_code(response["code"])
        
        # Verify that validation passed
        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["errors"]), 0)
    
    @patch('agent.code_generation_agent.client.chat.completions.create')
    def test_invalid_code_detection(self, mock_completion):
        """Test that invalid code is correctly identified."""
        # Mock the OpenAI API response with invalid code
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """
        ```python
        from reachy2_sdk import ReachySDK
        
        # Connect to the robot
        reachy = ReachySDK(host="localhost")
        
        # This line has a syntax error
        if battery > 50
            print("Battery level is good")
        ```
        """
        mock_completion.return_value = mock_response
        
        # Call the agent's generate_code method
        response = self.agent.generate_code("Check if battery level is good")
        
        # Validate the code
        validation = self.agent.validate_code(response["code"])
        
        # Verify that validation failed
        self.assertFalse(validation["valid"])
        self.assertTrue(len(validation["errors"]) > 0)


if __name__ == "__main__":
    unittest.main() 