#!/usr/bin/env python
"""
Test module for the Code Evaluator functionality.

This module contains tests for the CodeEvaluator class, focusing on:
- Interaction with the OpenAI API (mocked)
- Parsing of valid and invalid JSON responses
- Error handling during API calls or JSON parsing
- Summarization of evaluation results
"""

import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to import the class to test
try:
    from agent.code_evaluator import CodeEvaluator, EvaluationResult
    from agent.prompt_config import build_evaluator_prompt # Needed for verifying calls
except ImportError as e:
    # Provide a more informative error if imports fail
    raise ImportError(f"Failed to import CodeEvaluator or dependencies. Ensure agent/code_evaluator.py and agent/prompt_config.py exist and are importable. Original error: {e}")

# Dummy API key for testing when mocking
DUMMY_API_KEY = "test_key_123"

class TestCodeEvaluator(unittest.TestCase):
    """Test cases for the CodeEvaluator."""

    def setUp(self):
        """Set up the evaluator instance for each test, mocking the client."""
        # We mock the OpenAI client within the tests that need it
        self.evaluator = CodeEvaluator(api_key=DUMMY_API_KEY, model="test-model")
        self.sample_code = "print('Hello, Reachy!')"
        self.sample_request = "Make reachy say hello"

    @patch('agent.code_evaluator.OpenAI')
    def test_initialization(self, MockOpenAI):
        """Test that the CodeEvaluator initializes correctly and creates an OpenAI client."""
        client_instance = MockOpenAI.return_value
        evaluator = CodeEvaluator(api_key="another_key", model="gpt-eval", temperature=0.5)
        
        MockOpenAI.assert_called_once_with(api_key="another_key")
        self.assertEqual(evaluator.api_key, "another_key")
        self.assertEqual(evaluator.model, "gpt-eval")
        self.assertEqual(evaluator.temperature, 0.5)
        self.assertIsNotNone(evaluator.client)
        self.assertEqual(evaluator.client, client_instance)

    @patch('agent.code_evaluator.OpenAI')
    def test_evaluate_code_valid_json(self, MockOpenAI):
        """Test evaluation with a valid JSON response from the mocked API."""
        # Mock the client instance returned by OpenAI()
        mock_client_instance = MockOpenAI.return_value
        
        # Mock the API response structure
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()

        # Define the expected JSON payload from the LLM
        expected_eval_json = {
            "valid": True,
            "errors": [],
            "warnings": ["Consider adding comments"],
            "suggestions": ["Use f-strings for printing"],
            "score": 95.5,
            "explanation": "Code is generally good but could use comments."
        }
        mock_message.content = json.dumps(expected_eval_json)
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        
        # Set the return value for the mocked client instance's method
        mock_client_instance.chat.completions.create.return_value = mock_completion

        # Re-initialize evaluator *within the test* so it uses the mocked OpenAI class
        evaluator = CodeEvaluator(api_key=DUMMY_API_KEY, model="test-model")

        # Call the method under test
        result = evaluator.evaluate_code(self.sample_code, self.sample_request)

        # Assertions
        mock_client_instance.chat.completions.create.assert_called_once()
        call_args, call_kwargs = mock_client_instance.chat.completions.create.call_args
        
        # Verify prompt components were passed
        self.assertEqual(call_kwargs['model'], evaluator.model)
        self.assertEqual(call_kwargs['temperature'], evaluator.temperature)
        self.assertEqual(call_kwargs['max_tokens'], evaluator.max_tokens)
        self.assertEqual(call_kwargs['response_format'], {"type": "json_object"})
        
        messages = call_kwargs['messages']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[0]['content'], build_evaluator_prompt()) # Check system prompt
        self.assertEqual(messages[1]['role'], 'user')
        self.assertIn(self.sample_request, messages[1]['content']) # Check user request in user message
        self.assertIn(self.sample_code, messages[1]['content'])   # Check code in user message

        # Verify the parsed result matches the mocked JSON
        self.assertTrue(result['valid'])
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['warnings'], ["Consider adding comments"])
        self.assertEqual(result['suggestions'], ["Use f-strings for printing"])
        self.assertEqual(result['score'], 95.5)
        self.assertEqual(result['explanation'], "Code is generally good but could use comments.")
        
    @patch('agent.code_evaluator.OpenAI')
    def test_evaluate_code_invalid_json(self, MockOpenAI):
        """Test evaluation when the API returns malformed JSON."""
        # Mock the client instance returned by OpenAI()
        mock_client_instance = MockOpenAI.return_value

        mock_completion = MagicMock()
        mock_choice = MagicMock()
        
        # Malformed JSON (missing closing brace)
        mock_choice.message.content = '{"valid": true, "errors": [], "score": 90.0' 
        mock_choice.message = mock_choice.message
        mock_completion.choices = [mock_choice]
        
        mock_client_instance.chat.completions.create.return_value = mock_completion

        # Re-initialize evaluator *within the test*
        evaluator = CodeEvaluator(api_key=DUMMY_API_KEY, model="test-model")
        result = evaluator.evaluate_code(self.sample_code, self.sample_request)

        # Check that it returns the fallback error structure
        self.assertFalse(result['valid'])
        self.assertIn("Error parsing evaluation JSON", result['errors'][0])
        self.assertEqual(result['warnings'], [])
        self.assertEqual(result['suggestions'], ["Try generating code again"])
        self.assertEqual(result['score'], 0.0)
        self.assertTrue(result['explanation'].startswith("Error parsing evaluation response:"))

    @patch('agent.code_evaluator.OpenAI')
    def test_evaluate_code_api_error(self, MockOpenAI):
        """Test evaluation when the API call itself raises an exception."""
        # Mock the client instance returned by OpenAI()
        mock_client_instance = MockOpenAI.return_value
        
        # Configure the mock to raise an exception
        mock_client_instance.chat.completions.create.side_effect = Exception("API connection failed")

        # Re-initialize evaluator *within the test*
        evaluator = CodeEvaluator(api_key=DUMMY_API_KEY, model="test-model")
        result = evaluator.evaluate_code(self.sample_code, self.sample_request)

        # Check that it returns the fallback error structure for general exceptions
        self.assertFalse(result['valid'])
        self.assertTrue(result['errors'][0].startswith("Error during evaluation:"))
        self.assertIn("API connection failed", result['errors'][0])
        self.assertEqual(result['warnings'], [])
        self.assertEqual(result['suggestions'], [])
        self.assertEqual(result['score'], 0.0)
        self.assertTrue(result['explanation'].startswith("An error occurred during evaluation:"))
        self.assertIn("API connection failed", result['explanation'])
        
    def test_evaluate_code_no_code(self):
        """Test evaluation when no code is provided."""
        result = self.evaluator.evaluate_code("", self.sample_request)
        
        self.assertFalse(result['valid'])
        self.assertEqual(result['errors'], ["No code provided for evaluation"])
        self.assertEqual(result['score'], 0.0)
        self.assertEqual(result['explanation'], "No code was provided for evaluation.")

    def test_summarize_evaluation(self):
        """Test the summarization of evaluation results."""
        # Test case 1: Valid code with warnings and suggestions
        valid_result: EvaluationResult = {
            "valid": True, "errors": [], "warnings": ["W1"], 
            "suggestions": ["S1"], "score": 85.0, "explanation": "Good code"
        }
        summary1 = self.evaluator.summarize_evaluation(valid_result)
        self.assertIn("Score: 85.0/100", summary1)
        self.assertIn("✅ **Valid code**", summary1)
        self.assertNotIn("Critical Errors", summary1)
        self.assertIn("### Warnings:", summary1)
        self.assertIn("- ⚠️ W1", summary1)
        self.assertIn("### Suggestions:", summary1)
        self.assertIn("- 💡 S1", summary1)
        self.assertIn("### Explanation:", summary1)
        self.assertIn("Good code", summary1)

        # Test case 2: Invalid code with errors
        invalid_result: EvaluationResult = {
            "valid": False, "errors": ["E1", "E2"], "warnings": [], 
            "suggestions": [], "score": 20.0, "explanation": "Bad code"
        }
        summary2 = self.evaluator.summarize_evaluation(invalid_result)
        self.assertIn("Score: 20.0/100", summary2)
        self.assertIn("❌ **Invalid code**", summary2)
        self.assertIn("### Critical Errors:", summary2)
        self.assertIn("- 🚫 E1", summary2)
        self.assertIn("- 🚫 E2", summary2)
        self.assertNotIn("Warnings:", summary2)
        self.assertNotIn("Suggestions:", summary2)
        self.assertIn("Bad code", summary2)
        
        # Test case 3: Valid code with no issues
        perfect_result: EvaluationResult = {
            "valid": True, "errors": [], "warnings": [], 
            "suggestions": [], "score": 100.0, "explanation": "Perfect!"
        }
        summary3 = self.evaluator.summarize_evaluation(perfect_result)
        self.assertIn("Score: 100.0/100", summary3)
        self.assertIn("✅ **Valid code**", summary3)
        self.assertNotIn("Critical Errors", summary3)
        self.assertNotIn("Warnings:", summary3)
        self.assertNotIn("Suggestions:", summary3)
        self.assertIn("Perfect!", summary3)

if __name__ == "__main__":
    unittest.main() 