#!/usr/bin/env python
"""
LangGraph implementation of the Reachy 2 robot agent.

This module provides a graph-based implementation of the Reachy 2 agent using LangGraph,
which allows for more complex workflows, better state management, and improved error handling.
"""

import json
import os
import importlib
import inspect
import sys
from typing import Dict, List, Any, Optional, Callable, Union, TypedDict, Sequence
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Handle Annotated import for different Python versions
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from .tool_mapper import ReachyToolMapper


class Message(BaseModel):
    """A message in the conversation."""
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ToolCall(BaseModel):
    """A tool call made by the agent."""
    name: str
    arguments: Dict[str, Any]
    id: str


class ToolResult(BaseModel):
    """The result of a tool execution."""
    tool_call_id: str
    result: Dict[str, Any]


class AgentState(BaseModel):
    """
    The state of the agent, including conversation history and tool-related information.
    """
    messages: List[Message] = Field(default_factory=list)
    current_tool_calls: List[ToolCall] = Field(default_factory=list)
    tool_results: List[ToolResult] = Field(default_factory=list)
    error: Optional[str] = None
    final_response: Optional[str] = None


class ReachyLangGraphAgent:
    """
    A LangGraph implementation of the Reachy 2 agent.
    
    This agent uses a graph-based approach to manage the conversation flow,
    tool selection, and execution, providing more flexibility and better error handling.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ):
        """
        Initialize the Reachy LangGraph agent.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            model: LLM model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
            temperature: Temperature for LLM sampling.
            max_tokens: Maximum tokens for LLM response.
        """
        self.client = OpenAI(api_key=api_key)
        
        # Use model from environment variable if not provided
        if model is None:
            model = os.environ.get("MODEL", "gpt-4-turbo")
            
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self.tools = {}  # Tool schemas
        self.tool_implementations = {}  # Tool functions
        
        # System prompt for the agent
        self.system_prompt = """
        You are an AI assistant that controls a Reachy 2 robot. You have access to various
        functions that allow you to control the robot's movements and actions.
        
        When a user asks you to perform an action with the robot, analyze their request
        and call the appropriate function to control the robot. Be precise and safe in your
        actions, and always confirm what you're about to do before executing potentially
        dangerous movements.
        
        If you're unsure about a request or if it seems unsafe, ask for clarification.
        Always prioritize the safety of the robot and any humans around it.
        """
        
        # Load tools using the tool mapper
        self._load_tools()
        
        # Build the agent graph
        self.graph = self._build_graph()
    
    def _load_tools(self) -> None:
        """
        Load tools using the ReachyToolMapper.
        """
        # Create a tool mapper instance
        mapper = ReachyToolMapper()
        
        # Discover and register tools
        mapper.discover_tool_classes()
        mapper.register_tools_from_classes()
        
        # Get tool schemas and implementations
        self.tools = mapper.get_tool_schemas()
        self.tool_implementations = mapper.get_tool_implementations()
        
        print(f"Loaded {len(self.tools)} tools and {len(self.tool_implementations)} implementations")
    
    def load_tool_schemas_from_dir(self, schemas_dir: str) -> int:
        """
        Load tool schemas from JSON files in the specified directory.
        
        Args:
            schemas_dir: Directory containing tool schema JSON files.
            
        Returns:
            int: Number of tools loaded.
        """
        count = 0
        
        for file in os.listdir(schemas_dir):
            if not file.endswith(".json"):
                continue
                
            file_path = os.path.join(schemas_dir, file)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    schemas = json.load(f)
                    
                for name, schema in schemas.items():
                    self.tools[name] = schema
                    count += 1
                    
                print(f"Loaded {len(schemas)} tools from {file}")
            except Exception as e:
                print(f"Error loading tool schemas from {file}: {e}")
        
        return count
    
    def load_tool_implementations_from_dir(self, tools_dir: str) -> int:
        """
        Load tool implementations from Python modules in the specified directory.
        
        Args:
            tools_dir: Directory containing tool implementation modules.
            
        Returns:
            int: Number of tool implementations loaded.
        """
        count = 0
        
        # Add tools directory to path
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        
        # Load all modules in the tools directory
        for file in os.listdir(tools_dir):
            if not file.endswith(".py") or file.startswith("__"):
                continue
                
            module_name = file[:-3]  # Remove .py extension
            
            try:
                module = importlib.import_module(module_name)
                
                # Find all functions in the module
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if name.startswith("_"):
                        continue
                        
                    self.tool_implementations[name] = obj
                    count += 1
                    
                print(f"Loaded functions from {module_name}")
            except Exception as e:
                print(f"Error loading tool implementations from {module_name}: {e}")
        
        return count
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of available tools.
        
        Returns:
            List[Dict[str, Any]]: List of tool schemas
        """
        return list(self.tools.values())
    
    def _parse_user_input(self, state: AgentState) -> AgentState:
        """
        Parse the user input and add it to the conversation history.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state.
        """
        # The last message should be the user input
        last_message = state.messages[-1]
        if last_message.role != "user":
            state.error = "Expected user message"
            return state
        
        # No additional processing needed, just return the state
        return state
    
    def _select_tool(self, state: AgentState) -> AgentState:
        """
        Select a tool to use based on the user input.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state with selected tool.
        """
        # Convert messages to the format expected by OpenAI
        openai_messages = []
        
        # Add system message if not present
        if not state.messages or state.messages[0].role != "system":
            openai_messages.append({"role": "system", "content": self.system_prompt})
        
        # Add the rest of the messages
        for message in state.messages:
            msg_dict = {"role": message.role}
            
            if message.content is not None:
                msg_dict["content"] = message.content
                
            if message.tool_calls:
                msg_dict["tool_calls"] = message.tool_calls
                
            if message.tool_call_id:
                msg_dict["tool_call_id"] = message.tool_call_id
                
            openai_messages.append(msg_dict)
        
        # Call the LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            tools=self.get_available_tools(),
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # Get the response message
        response_message = response.choices[0].message
        
        # Add the assistant's response to the conversation
        assistant_message = Message(
            role="assistant",
            content=response_message.content
        )
        
        # Check if the model wants to call a tool
        if response_message.tool_calls:
            assistant_message.tool_calls = []
            state.current_tool_calls = []
            
            for tool_call in response_message.tool_calls:
                # Extract tool call information
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                # Add to the message
                assistant_message.tool_calls.append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "arguments": tool_call.function.arguments
                    }
                })
                
                # Add to the current tool calls
                state.current_tool_calls.append(
                    ToolCall(
                        name=tool_name,
                        arguments=tool_args,
                        id=tool_call.id
                    )
                )
        
        # Add the assistant's response to the conversation
        state.messages.append(assistant_message)
        
        return state
    
    def _execute_tools(self, state: AgentState) -> AgentState:
        """
        Execute the selected tools.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state with tool results.
        """
        if not state.current_tool_calls:
            # No tools to execute, just return the state
            return state
        
        state.tool_results = []
        
        for tool_call in state.current_tool_calls:
            tool_name = tool_call.name
            tool_args = tool_call.arguments
            
            # Check if the tool exists
            if tool_name not in self.tool_implementations:
                result = {
                    "success": False,
                    "error": f"Tool {tool_name} not found"
                }
            else:
                # Execute the tool
                try:
                    tool_func = self.tool_implementations[tool_name]
                    result = tool_func(**tool_args)
                except Exception as e:
                    result = {
                        "success": False,
                        "error": str(e)
                    }
            
            # Add the result to the state
            state.tool_results.append(
                ToolResult(
                    tool_call_id=tool_call.id,
                    result=result
                )
            )
            
            # Add the tool result to the conversation
            state.messages.append(
                Message(
                    role="tool",
                    tool_call_id=tool_call.id,
                    content=json.dumps(result)
                )
            )
        
        # Clear current tool calls
        state.current_tool_calls = []
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """
        Generate a final response based on the tool results.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state with final response.
        """
        # Convert messages to the format expected by OpenAI
        openai_messages = []
        
        # Add system message if not present
        if not state.messages or state.messages[0].role != "system":
            openai_messages.append({"role": "system", "content": self.system_prompt})
        
        # Add the rest of the messages
        for message in state.messages:
            msg_dict = {"role": message.role}
            
            if message.content is not None:
                msg_dict["content"] = message.content
                
            if message.tool_calls:
                msg_dict["tool_calls"] = message.tool_calls
                
            if message.tool_call_id:
                msg_dict["tool_call_id"] = message.tool_call_id
                
            openai_messages.append(msg_dict)
        
        # Call the LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # Get the response message
        response_message = response.choices[0].message
        
        # Add the final response to the conversation
        state.messages.append(
            Message(
                role="assistant",
                content=response_message.content
            )
        )
        
        # Set the final response
        state.final_response = response_message.content
        
        return state
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Determine whether to continue the conversation or end it.
        
        Args:
            state: Current agent state.
            
        Returns:
            str: Next node to execute.
        """
        if state.error:
            return "generate_response"
        
        if state.current_tool_calls:
            return "execute_tools"
        
        if state.tool_results:
            return "generate_response"
        
        # Check if the last assistant message has tool calls
        for message in reversed(state.messages):
            if message.role == "assistant" and message.tool_calls:
                return "execute_tools"
            elif message.role == "assistant":
                break
        
        return END
    
    def _build_graph(self) -> StateGraph:
        """
        Build the agent graph.
        
        Returns:
            StateGraph: The agent graph.
        """
        # Create the graph
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("parse_user_input", self._parse_user_input)
        graph.add_node("select_tool", self._select_tool)
        graph.add_node("execute_tools", self._execute_tools)
        graph.add_node("generate_response", self._generate_response)
        
        # Add edges
        graph.add_edge("parse_user_input", "select_tool")
        graph.add_edge("select_tool", self._should_continue)
        graph.add_edge("execute_tools", "generate_response")
        graph.add_edge("generate_response", END)
        
        # Set the entry point
        graph.set_entry_point("parse_user_input")
        
        return graph
    
    def process_message(self, user_message: str) -> str:
        """
        Process a user message and generate a response, potentially calling tools.
        
        Args:
            user_message: User's message.
            
        Returns:
            str: Agent's response.
        """
        # Create initial state
        state = AgentState(
            messages=[
                Message(role="system", content=self.system_prompt),
                Message(role="user", content=user_message)
            ]
        )
        
        # Run the graph
        final_state = self.graph.invoke(state)
        
        # Return the final response
        return final_state.final_response or "I couldn't generate a response."
    
    def reset_conversation(self):
        """Reset the conversation history."""
        # No need to do anything, as we create a new state for each conversation
        pass
        
    def get_robot_status(self) -> Dict[str, Any]:
        """
        Get the current status of the robot.
        
        Returns:
            Dict[str, Any]: Robot status information
        """
        status = {
            "status": "connected",
            "last_update": time.time(),
            "arms": {
                "left": {"position": [0.0] * 7, "gripper_opening": 0.0},
                "right": {"position": [0.0] * 7, "gripper_opening": 0.0}
            },
            "head": {"position": [0.0, 0.0, 0.0]},
            "base": {"position": [0.0, 0.0, 0.0]},
            "last_action": None
        }
        
        # Try to get actual robot status if available
        try:
            if "get_robot_info" in self.tool_implementations:
                info_result = self.tool_implementations["get_robot_info"]()
                if info_result.get("success", False):
                    status.update(info_result.get("result", {}))
            
            # Get arm positions if available
            if "get_arm_position" in self.tool_implementations:
                for side in ["left", "right"]:
                    try:
                        arm_result = self.tool_implementations["get_arm_position"](side=side)
                        if arm_result.get("success", False):
                            status["arms"][side]["position"] = arm_result.get("result", {}).get("positions", [0.0] * 7)
                    except:
                        pass
            
            # Get head position if available
            if "get_head_position" in self.tool_implementations:
                try:
                    head_result = self.tool_implementations["get_head_position"]()
                    if head_result.get("success", False):
                        status["head"]["position"] = head_result.get("result", {}).get("positions", [0.0, 0.0, 0.0])
                except:
                    pass
            
            # Get base position if available
            if "get_base_position" in self.tool_implementations:
                try:
                    base_result = self.tool_implementations["get_base_position"]()
                    if base_result.get("success", False):
                        base_pos = base_result.get("result", {})
                        status["base"]["position"] = [
                            base_pos.get("x", 0.0),
                            base_pos.get("y", 0.0),
                            base_pos.get("theta", 0.0)
                        ]
                except:
                    pass
                    
        except Exception as e:
            status["error"] = str(e)
        
        return status


# Example usage
if __name__ == "__main__":
    import os
    
    # Create agent
    agent = ReachyLangGraphAgent(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Process a message
    response = agent.process_message("Can you move the robot's right arm up?")
    print(response) 