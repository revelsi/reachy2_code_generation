#!/usr/bin/env python
"""
Agent Router for the Reachy 2 robot.

This module provides a router that directs requests to either the function calling agent
or the code generation agent based on the selected mode.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional, Literal, Union
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_router")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import configuration
from config import get_model_config, update_model_config, OPENAI_API_KEY

# Import agents
from agent.langgraph_agent import ReachyLangGraphAgent
from agent.code_generation_agent import ReachyCodeGenerationAgent


class AgentMode(str, Enum):
    """Enum for agent modes."""
    FUNCTION_CALLING = "function_calling"
    CODE_GENERATION = "code_generation"


class AgentRouter:
    """
    Router for directing requests to the appropriate agent based on the selected mode.
    
    This class manages both the function calling agent and the code generation agent,
    providing a unified interface for interacting with either agent.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_config: Optional[Dict[str, Any]] = None,
        focus_modules: Optional[List[str]] = None,
        regenerate_tools: bool = False,
        default_mode: AgentMode = AgentMode.FUNCTION_CALLING
    ):
        """
        Initialize the agent router.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY from config.
            model_config: Model configuration. If None, will use the configuration from config.py.
            focus_modules: Optional list of module names to focus on.
            regenerate_tools: Whether to regenerate tool definitions and implementations.
            default_mode: The default agent mode to use.
        """
        self.api_key = api_key or OPENAI_API_KEY
        
        # Get model configuration
        self.model_config = model_config or get_model_config()
        self.model = self.model_config["model"]
        
        self.focus_modules = focus_modules
        self.regenerate_tools = regenerate_tools
        self.current_mode = default_mode
        
        # Initialize agents
        logger.info(f"Initializing function calling agent with model: {self.model}")
        self.function_calling_agent = ReachyLangGraphAgent(model=self.model)
        
        logger.info(f"Initializing code generation agent with model: {self.model}")
        self.code_generation_agent = ReachyCodeGenerationAgent(
            model=self.model,
            api_key=self.api_key,
            temperature=self.model_config.get("temperature", 0.2),
            max_tokens=self.model_config.get("max_tokens", 4000),
            top_p=self.model_config.get("top_p", 0.95),
            frequency_penalty=self.model_config.get("frequency_penalty", 0),
            presence_penalty=self.model_config.get("presence_penalty", 0)
        )
        
        # Share tool definitions between agents
        self._share_tool_definitions()
        
        logger.info(f"Agent router initialized with default mode: {default_mode}")
    
    def _share_tool_definitions(self):
        """Share tool definitions between agents."""
        # Share tool schemas from function calling agent to code generation agent
        self.code_generation_agent.set_tool_schemas(self.function_calling_agent.tools)
        logger.info(f"Shared {len(self.function_calling_agent.tools)} tool definitions with code generation agent")
    
    def set_mode(self, mode: AgentMode) -> None:
        """
        Set the current agent mode.
        
        Args:
            mode: The agent mode to use.
        """
        if mode not in AgentMode:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {list(AgentMode)}")
        
        self.current_mode = mode
        logger.info(f"Agent mode set to: {mode}")
    
    def get_mode(self) -> AgentMode:
        """
        Get the current agent mode.
        
        Returns:
            AgentMode: The current agent mode.
        """
        return self.current_mode
    
    def update_model_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update the model configuration for both agents.
        
        Args:
            new_config: The new model configuration.
        """
        # Update the global configuration
        update_model_config(new_config)
        
        # Get the updated configuration
        self.model_config = get_model_config()
        self.model = self.model_config["model"]
        
        # Update the agents
        logger.info(f"Updating agents with new model configuration: {self.model}")
        
        # Reinitialize agents with new configuration
        self.function_calling_agent = ReachyLangGraphAgent(model=self.model)
        
        self.code_generation_agent = ReachyCodeGenerationAgent(
            model=self.model,
            api_key=self.api_key,
            temperature=self.model_config.get("temperature", 0.2),
            max_tokens=self.model_config.get("max_tokens", 4000),
            top_p=self.model_config.get("top_p", 0.95),
            frequency_penalty=self.model_config.get("frequency_penalty", 0),
            presence_penalty=self.model_config.get("presence_penalty", 0)
        )
        
        # Share tool definitions between agents
        self._share_tool_definitions()
        
        logger.info("Model configuration updated successfully")
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message using the current agent mode.
        
        Args:
            message: The user message to process.
            
        Returns:
            Dict[str, Any]: The response from the agent.
        """
        logger.info(f"Processing message in {self.current_mode} mode")
        
        if self.current_mode == AgentMode.FUNCTION_CALLING:
            response = self.function_calling_agent.process_message(message)
            return self._format_function_calling_response(response)
        
        elif self.current_mode == AgentMode.CODE_GENERATION:
            response = self.code_generation_agent.process_message(message)
            return self._format_code_generation_response(response)
        
        else:
            raise ValueError(f"Unknown mode: {self.current_mode}")
    
    def _format_function_calling_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the response from the function calling agent.
        
        Args:
            response: The response from the function calling agent.
            
        Returns:
            Dict[str, Any]: The formatted response.
        """
        # Add mode information to the response
        response["mode"] = AgentMode.FUNCTION_CALLING
        return response
    
    def _format_code_generation_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the response from the code generation agent.
        
        Args:
            response: The response from the code generation agent.
            
        Returns:
            Dict[str, Any]: The formatted response.
        """
        # Add mode information to the response
        response["mode"] = AgentMode.CODE_GENERATION
        return response
    
    def reset_conversation(self) -> None:
        """Reset the conversation state for both agents."""
        self.function_calling_agent.reset_conversation()
        self.code_generation_agent.reset_conversation()
        logger.info("Reset conversation state for both agents")
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of available tools.
        
        Returns:
            List[Dict[str, Any]]: List of tool schemas
        """
        return self.function_calling_agent.get_available_tools()
    
    def get_model_config(self) -> Dict[str, Any]:
        """
        Get the current model configuration.
        
        Returns:
            Dict[str, Any]: The model configuration.
        """
        return self.model_config.copy() 