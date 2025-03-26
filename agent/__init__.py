#!/usr/bin/env python
"""
Reachy 2 Code Generation Agent

This package provides a code generation agent for the Reachy 2 robot.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent")

# Ensure the parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Export key classes
from .agent_router import AgentRouter
from .code_generation_agent import ReachyCodeGenerationAgent

# Define version
__version__ = "0.1.0"

def create_agent(api_key: Optional[str] = None, model_config: Optional[Dict[str, Any]] = None) -> AgentRouter:
    """
    Create a Reachy 2 Code Generation Agent.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY from config.
        model_config: Model configuration. If None, will use the configuration from config.py.
        
    Returns:
        AgentRouter: The agent router.
    """
    return AgentRouter(api_key=api_key, model_config=model_config) 