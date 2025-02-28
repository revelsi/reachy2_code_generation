#!/usr/bin/env python
"""
Test script for verifying the centralized model configuration features.

This script tests the model configuration functionality across different components
of the Reachy Function Calling system.
"""

import os
import sys
import json
from typing import Dict, Any
from unittest.mock import patch
from enum import Enum

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set a mock API key for testing
os.environ["OPENAI_API_KEY"] = "sk-mock-api-key-for-testing"

# Import configuration and agent modules
from config import (
    get_model_config, update_model_config, AVAILABLE_MODELS, MODEL_CONFIG
)
from agent.agent_router import AgentRouter, AgentMode
from agent.code_generation_agent import ReachyCodeGenerationAgent


def print_section(title: str) -> None:
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def print_config(config: Dict[str, Any], prefix: str = "") -> None:
    """Print a configuration dictionary."""
    for key, value in config.items():
        print(f"{prefix}{key}: {value}")


def test_config_module() -> None:
    """Test the config module functions."""
    print_section("Testing Config Module")
    
    # Get initial configuration
    initial_config = get_model_config()
    print("Initial configuration:")
    print_config(initial_config, "  ")
    
    # Update configuration
    print("\nUpdating configuration...")
    new_config = {
        "model": "gpt-4o",
        "temperature": 0.5,
        "max_tokens": 3000
    }
    update_model_config(new_config)
    
    # Get updated configuration
    updated_config = get_model_config()
    print("\nUpdated configuration:")
    print_config(updated_config, "  ")
    
    # Verify changes
    success = (
        updated_config["model"] == "gpt-4o" and
        updated_config["temperature"] == 0.5 and
        updated_config["max_tokens"] == 3000
    )
    print(f"\nConfig module test {'PASSED' if success else 'FAILED'}")
    
    # Reset configuration for other tests
    reset_config = {
        "model": initial_config["model"],
        "temperature": initial_config["temperature"],
        "max_tokens": initial_config["max_tokens"]
    }
    update_model_config(reset_config)
    print("\nReset configuration to initial values")


# Mock classes for testing without actual API calls
class MockReachyLangGraphAgent:
    def __init__(self, model="gpt-4-turbo"):
        self.model = model
        self.tools = []
    
    def process_message(self, message):
        return {"message": "Mock response", "tool_calls": []}
    
    def reset_conversation(self):
        pass
    
    def get_available_tools(self):
        return []


class MockReachyCodeGenerationAgent:
    def __init__(self, model="gpt-4-turbo", api_key=None, temperature=0.2, 
                 max_tokens=4000, top_p=0.95, frequency_penalty=0, presence_penalty=0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.api_key = api_key
    
    def process_message(self, message):
        return {"message": "Mock response", "code": "print('Hello, world!')", "validation": {"valid": True}}
    
    def reset_conversation(self):
        pass
    
    def set_tool_schemas(self, schemas):
        pass


class AgentMode(str, Enum):
    """Enum for agent modes."""
    FUNCTION_CALLING = "function_calling"
    CODE_GENERATION = "code_generation"


class MockAgentRouter:
    def __init__(self, api_key=None, model_config=None, focus_modules=None, 
                 regenerate_tools=False, default_mode=AgentMode.FUNCTION_CALLING):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model_config = model_config or get_model_config()
        self.model = self.model_config["model"]
        self.focus_modules = focus_modules
        self.regenerate_tools = regenerate_tools
        self.current_mode = default_mode
        self.function_calling_agent = MockReachyLangGraphAgent(model=self.model)
        self.code_generation_agent = MockReachyCodeGenerationAgent(
            model=self.model,
            api_key=self.api_key,
            temperature=self.model_config.get("temperature", 0.2),
            max_tokens=self.model_config.get("max_tokens", 4000),
            top_p=self.model_config.get("top_p", 0.95),
            frequency_penalty=self.model_config.get("frequency_penalty", 0),
            presence_penalty=self.model_config.get("presence_penalty", 0)
        )
    
    def get_model_config(self):
        return self.model_config.copy()
    
    def update_model_config(self, new_config):
        update_model_config(new_config)
        self.model_config = get_model_config()
        self.model = self.model_config["model"]
        self.function_calling_agent = MockReachyLangGraphAgent(model=self.model)
        self.code_generation_agent = MockReachyCodeGenerationAgent(
            model=self.model,
            api_key=self.api_key,
            temperature=self.model_config.get("temperature", 0.2),
            max_tokens=self.model_config.get("max_tokens", 4000),
            top_p=self.model_config.get("top_p", 0.95),
            frequency_penalty=self.model_config.get("frequency_penalty", 0),
            presence_penalty=self.model_config.get("presence_penalty", 0)
        )
    
    def set_mode(self, mode):
        self.current_mode = mode
    
    def get_mode(self):
        return self.current_mode
    
    def process_message(self, message):
        if self.current_mode == AgentMode.FUNCTION_CALLING:
            return self.function_calling_agent.process_message(message)
        else:
            return self.code_generation_agent.process_message(message)
    
    def reset_conversation(self):
        self.function_calling_agent.reset_conversation()
        self.code_generation_agent.reset_conversation()
    
    def get_available_tools(self):
        return self.function_calling_agent.get_available_tools()


def test_agent_router() -> None:
    """Test the AgentRouter model configuration functionality."""
    print_section("Testing AgentRouter")
    
    # Initialize agent router with default configuration
    print("Initializing AgentRouter with default configuration...")
    agent_router = MockAgentRouter()
    
    # Get initial configuration
    initial_config = agent_router.get_model_config()
    print("\nInitial configuration from AgentRouter:")
    print_config(initial_config, "  ")
    
    # Update configuration
    print("\nUpdating configuration through AgentRouter...")
    new_config = {
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 2500
    }
    agent_router.update_model_config(new_config)
    
    # Get updated configuration
    updated_config = agent_router.get_model_config()
    print("\nUpdated configuration from AgentRouter:")
    print_config(updated_config, "  ")
    
    # Verify changes
    success = (
        updated_config["model"] == "gpt-4o" and
        updated_config["temperature"] == 0.7 and
        updated_config["max_tokens"] == 2500 and
        agent_router.model == "gpt-4o"
    )
    print(f"\nAgentRouter test {'PASSED' if success else 'FAILED'}")
    
    # Verify that the global configuration was also updated
    global_config = get_model_config()
    print("\nGlobal configuration after AgentRouter update:")
    print_config(global_config, "  ")
    
    global_success = (
        global_config["model"] == "gpt-4o" and
        global_config["temperature"] == 0.7 and
        global_config["max_tokens"] == 2500
    )
    print(f"\nGlobal config synchronization {'PASSED' if global_success else 'FAILED'}")
    
    # Reset configuration for other tests
    reset_config = {
        "model": MODEL_CONFIG["model"],
        "temperature": MODEL_CONFIG["temperature"],
        "max_tokens": MODEL_CONFIG["max_tokens"]
    }
    update_model_config(reset_config)
    print("\nReset configuration to default values")


def test_code_generation_agent() -> None:
    """Test the CodeGenerationAgent model configuration functionality."""
    print_section("Testing CodeGenerationAgent")
    
    # Initialize code generation agent with custom configuration
    print("Initializing CodeGenerationAgent with custom configuration...")
    custom_config = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    code_agent = MockReachyCodeGenerationAgent(
        model=custom_config["model"],
        temperature=custom_config["temperature"],
        max_tokens=custom_config["max_tokens"]
    )
    
    # Verify configuration
    success = (
        code_agent.model == "gpt-3.5-turbo" and
        code_agent.temperature == 0.3 and
        code_agent.max_tokens == 2000
    )
    print("\nCodeGenerationAgent configuration:")
    print(f"  model: {code_agent.model}")
    print(f"  temperature: {code_agent.temperature}")
    print(f"  max_tokens: {code_agent.max_tokens}")
    
    print(f"\nCodeGenerationAgent test {'PASSED' if success else 'FAILED'}")


def test_agent_modes() -> None:
    """Test the agent mode switching functionality."""
    print_section("Testing Agent Mode Switching")
    
    # Initialize agent router
    print("Initializing AgentRouter...")
    agent_router = MockAgentRouter()
    
    # Get initial mode
    initial_mode = agent_router.get_mode()
    print(f"\nInitial mode: {initial_mode}")
    
    # Switch to code generation mode
    print("\nSwitching to CODE_GENERATION mode...")
    agent_router.set_mode(AgentMode.CODE_GENERATION)
    new_mode = agent_router.get_mode()
    print(f"New mode: {new_mode}")
    
    # Verify mode change
    mode_success = new_mode == AgentMode.CODE_GENERATION
    print(f"\nMode switching test {'PASSED' if mode_success else 'FAILED'}")
    
    # Switch back to function calling mode
    print("\nSwitching back to FUNCTION_CALLING mode...")
    agent_router.set_mode(AgentMode.FUNCTION_CALLING)
    final_mode = agent_router.get_mode()
    print(f"Final mode: {final_mode}")
    
    # Verify mode change
    final_success = final_mode == AgentMode.FUNCTION_CALLING
    print(f"\nFinal mode switching test {'PASSED' if final_success else 'FAILED'}")


def main() -> None:
    """Run all tests."""
    print_section("MODEL CONFIGURATION TESTS")
    print("Testing the centralized model configuration features")
    
    # Run tests
    test_config_module()
    test_agent_router()
    test_code_generation_agent()
    test_agent_modes()
    
    print_section("TESTS COMPLETED")


if __name__ == "__main__":
    main() 