#!/usr/bin/env python
"""
Reachy Function Calling Agent

This package provides a framework for transparent function calling with the Reachy 2 robot.
It demonstrates how to create a system that:

1. Shows the reasoning behind each function call
2. Displays the function call with parameters
3. Requests user permission before execution
4. Shows execution results

The agent can operate in two modes:
- Function Calling: Uses OpenAI's function calling to control the robot
- Code Generation: Generates Python code for more complex interactions

Additional documentation:
- For arm kinematics (forward/inverse kinematics): see docs/reachy2_kinematics_guide.md
"""

# Import only essential components that don't have complex dependencies
# Other components will be imported directly when needed

from .agent_router import AgentRouter, AgentMode
from .transparent_executor import TransparentExecutor
from .langgraph_agent import ReachyLangGraphAgent
from .code_generation_agent import ReachyCodeGenerationAgent
from .code_generation_interface import CodeGenerationInterface
from .web_interface import AgentInterface

# Import setup_agent function from cli.py instead of a class
from .cli import setup_agent

__all__ = [
    'AgentRouter',
    'AgentMode',
    'TransparentExecutor',
    'ReachyLangGraphAgent',
    'ReachyCodeGenerationAgent',
    'CodeGenerationInterface',
    'AgentInterface',
    'setup_agent',
]

__version__ = "1.0.0" 