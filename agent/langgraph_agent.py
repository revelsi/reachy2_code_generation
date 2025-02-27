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
import logging
import traceback
from typing import Dict, List, Any, Optional, Literal, TypedDict, Annotated
from dotenv import load_dotenv
import time
import asyncio
import websockets
from openai import OpenAI
import httpx
from pydantic import BaseModel

# Add the project root to the path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import REACHY_HOST, TOOLS_DIR, DEBUG

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("langgraph_agent")

# Load environment variables
load_dotenv()

# Handle Annotated import for different Python versions
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pathlib import Path

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint import CheckpointAt
from langgraph.graph.message import add_messages

# Import LangChain message types
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    BaseMessage
)

from agent.utils.tool_mapper import ReachyToolMapper

# Import WebSocket server for notifications
from api.websocket import get_websocket_server

# Configure OpenAI client with custom settings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,  # Increase timeout
    max_retries=2,  # Add retries
    base_url="https://api.openai.com/v1",  # Explicitly set base URL
    http_client=httpx.Client(
        transport=httpx.HTTPTransport(retries=2),
        timeout=30.0,
        verify=True  # Ensure SSL verification is enabled
    )
)

# Test the client configuration
try:
    test_response = client.models.list()
    logger.debug("Successfully connected to OpenAI API")
except Exception as e:
    logger.error(f"Error testing OpenAI connection: {e}")

# WebSocket server for notifications
websocket_server = get_websocket_server()
websocket_clients = set()

class ToolCall(BaseModel):
    """A tool call made by the agent."""
    name: str
    arguments: Dict[str, Any]
    id: str


class ToolResult(BaseModel):
    """The result of a tool execution."""
    tool_call_id: str
    result: Dict[str, Any]


class AgentState(TypedDict):
    """
    The state of the agent, including conversation history and tool-related information.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    current_tool_calls: List[ToolCall]
    tool_results: List[ToolResult]
    error: Optional[str]
    final_response: Optional[str]


class ReachyLangGraphAgent:
    """
    A LangGraph implementation of the Reachy 2 agent.
    
    This agent uses a graph-based approach to manage the conversation flow,
    tool selection, and execution, providing more flexibility and better error handling.
    """
    
    def __init__(self, model: str = "gpt-4-turbo", api_key: Optional[str] = None):
        self.model = model
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = client  # Use the configured client
        logger.debug(f"Initialized agent with model: {model}")
        self.tool_implementations = {}
        self.tools = []
        self.load_tools()
        
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
        
        # Build the graph after all initialization is complete
        self.graph = self._build_graph()
    
    def load_tools(self):
        """
        Load tools using the ReachyToolMapper.
        
        This method uses real tool definitions from the Reachy SDK,
        connecting to either a physical robot or a virtual one.
        """
        logger.info(f"Loading tools (Reachy host: {REACHY_HOST})")
        
        try:
            # First, verify that we can connect to the Reachy SDK
            from agent.tools.connection_manager import connect_to_reachy, disconnect_reachy
            reachy = connect_to_reachy(host=REACHY_HOST)
            logger.info(f"Successfully connected to Reachy SDK")
            
            # Create tool mapper and discover tools
            mapper = ReachyToolMapper()
            tool_classes = mapper.discover_tool_classes()
            logger.info(f"Discovered {len(tool_classes)} tool classes")
            
            # Register tools from classes
            num_tools = mapper.register_tools_from_classes(tool_classes)
            logger.info(f"Registered {num_tools} tools from classes")
            
            # Get tool schemas and implementations
            self.tools = mapper.get_tool_schemas()
            self.tool_implementations = mapper.get_tool_implementations()
            
            # Validate tool schemas and implementations
            self._validate_and_fix_tool_schemas()
            self._validate_tool_implementations()
            
            logger.info(f"Successfully loaded {len(self.tools)} tools")
            
        except Exception as e:
            logger.error(f"Error loading tools: {e}")
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Failed to load tools: {e}")
    
    def _validate_tool_implementations(self):
        """Validate that all tools have implementations."""
        missing_implementations = []
        for tool in self.tools:
            if isinstance(tool, dict) and "function" in tool and "name" in tool["function"]:
                tool_name = tool["function"]["name"]
                if tool_name not in self.tool_implementations:
                    missing_implementations.append(tool_name)
        
        if missing_implementations:
            logger.warning(f"Missing implementations for tools: {missing_implementations}")
        
        return missing_implementations
    
    def _validate_and_fix_tool_schemas(self):
        """
        Validate that tool schemas are in the correct format for LangChain/LangGraph.
        If not, convert them to the correct format.
        """
        valid_tools = []
        for tool in self.tools:
            # Check if the tool is in the correct format
            if (isinstance(tool, dict) and 
                tool.get("type") == "function" and 
                "function" in tool and 
                "name" in tool["function"] and 
                "description" in tool["function"] and 
                "parameters" in tool["function"]):
                valid_tools.append(tool)
            else:
                # Try to convert to the correct format
                try:
                    name = tool.get("name", "unknown_tool")
                    description = tool.get("description", "")
                    parameters = tool.get("parameters", {})
                    required = parameters.get("required", []) if isinstance(parameters, dict) else []
                    
                    # Create a properly formatted tool
                    fixed_tool = {
                        "type": "function",
                        "function": {
                            "name": name,
                            "description": description,
                            "parameters": {
                                "type": "object",
                                "properties": parameters.get("properties", {}) if isinstance(parameters, dict) else {},
                                "required": required
                            }
                        }
                    }
                    valid_tools.append(fixed_tool)
                    logger.info(f"Fixed tool schema format for {name}")
                except Exception as e:
                    logger.error(f"Could not fix tool schema: {e}")
        
        # Update the tools list with valid tools
        self.tools = valid_tools
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of available tools.
        
        Returns:
            List[Dict[str, Any]]: List of tool schemas
        """
        return self.tools
    
    def _parse_user_input(self, state: AgentState) -> AgentState:
        """
        Parse the user input and add it to the conversation history.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state.
        """
        logger.debug("Entering _parse_user_input")
        
        # Get WebSocket server for notifications
        ws_server = get_websocket_server()
        ws_server.notify_thinking("Parsing your input...")
        
        # The last message should be the user input
        last_message = state["messages"][-1]
        if not isinstance(last_message, HumanMessage):
            state["error"] = f"Expected user message, got {type(last_message).__name__}"
            logger.error(state["error"])
            return state
        
        logger.debug("Successfully parsed user input")
        return state
    
    def _call_llm(self, state: AgentState) -> AgentState:
        """
        Call the LLM to decide what to do next.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state with LLM response.
        """
        logger.debug("Entering _call_llm")
        
        # Get WebSocket server for notifications
        ws_server = get_websocket_server()
        ws_server.notify_thinking("Processing your request...")
        
        try:
            # Check if this is a meta-query about tools
            last_message = state["messages"][-1]
            if isinstance(last_message, HumanMessage) and "tools" in last_message.content.lower():
                # Get list of available tools
                tools = self.get_available_tools()
                tool_descriptions = []
                for tool in tools:
                    name = tool["function"]["name"]
                    desc = tool["function"]["description"].split("\n")[0]  # Get first line
                    tool_descriptions.append(f"- {name}: {desc}")
                
                # Create response
                response = "Here are the available tools:\n\n" + "\n".join(tool_descriptions)
                
                # Add response to conversation and set final response
                state["messages"].append(AIMessage(content=response))
                state["final_response"] = response
                
                # Notify completion
                ws_server.notify_complete(response)
                
                # Clear any pending tool calls to ensure we end the conversation
                state["current_tool_calls"] = []
                state["tool_results"] = []
                return state
            
            # Convert messages to the format expected by OpenAI
            openai_messages = []
            
            # Add the messages in the format OpenAI expects
            for message in state["messages"]:
                if isinstance(message, SystemMessage):
                    openai_messages.append({"role": "system", "content": message.content})
                elif isinstance(message, HumanMessage):
                    openai_messages.append({"role": "user", "content": message.content})
                elif isinstance(message, AIMessage):
                    msg_dict = {"role": "assistant"}
                    if message.content:
                        msg_dict["content"] = message.content
                    if hasattr(message, "tool_calls") and message.tool_calls:
                        msg_dict["tool_calls"] = message.tool_calls
                    openai_messages.append(msg_dict)
                elif isinstance(message, ToolMessage):
                    openai_messages.append({
                        "role": "tool",
                        "content": message.content,
                        "tool_call_id": message.tool_call_id if hasattr(message, "tool_call_id") else None
                    })
            
            logger.debug("Calling OpenAI with %d messages", len(openai_messages))
            
            # Call the LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                tools=self.get_available_tools(),
                temperature=0.2,
                max_tokens=1024
            )
            
            # Get the response message
            response_message = response.choices[0].message
            logger.debug("Got response from OpenAI: %s", response_message)
            
            # Add the assistant's response to the conversation
            assistant_message = AIMessage(content=response_message.content)
            
            # Check if the model wants to call a tool
            if response_message.tool_calls:
                logger.debug("Model wants to call %d tools", len(response_message.tool_calls))
                assistant_message.tool_calls = []
                state["current_tool_calls"] = []
                
                for tool_call in response_message.tool_calls:
                    # Extract tool call information
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    logger.debug("Processing tool call: %s with args %s", tool_name, tool_args)
                    
                    # Notify about the function call
                    ws_server.notify_function_call(tool_name, tool_args, tool_call.id)
                    
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
                    state["current_tool_calls"].append(
                        ToolCall(
                            name=tool_name,
                            arguments=tool_args,
                            id=tool_call.id
                        )
                    )
            
            # Add the assistant's response to the conversation
            state["messages"].append(assistant_message)
            logger.debug("Successfully processed LLM response")
            return state
            
        except Exception as e:
            logger.error("Error in _call_llm: %s", str(e), exc_info=True)
            state["error"] = f"Error calling LLM: {str(e)}"
            return state
    
    def _execute_tools(self, state: AgentState) -> AgentState:
        """
        Execute the selected tools.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state with tool results.
        """
        # Get WebSocket server for notifications
        ws_server = get_websocket_server()
        
        if not state["current_tool_calls"]:
            # No tools to execute, just return the state
            return state
        
        state["tool_results"] = []
        
        for tool_call in state["current_tool_calls"]:
            tool_name = tool_call.name
            tool_args = tool_call.arguments
            
            ws_server.notify_thinking(f"Executing tool: {tool_name}")
            
            # Check if the tool exists
            if tool_name not in self.tool_implementations:
                result = {
                    "success": False,
                    "error": f"Tool {tool_name} not found"
                }
                ws_server.notify_error(f"Tool {tool_name} not found")
            else:
                # Execute the tool
                try:
                    tool_func = self.tool_implementations[tool_name]
                    result = tool_func(**tool_args)
                    if not result.get("success", False):
                        ws_server.notify_error(result.get("error", "Unknown error"))
                except Exception as e:
                    result = {
                        "success": False,
                        "error": str(e)
                    }
                    ws_server.notify_error(str(e))
            
            # Notify clients about the tool execution result
            from api.websocket import notify_tool_execution_result
            notify_tool_execution_result(tool_call.id, result)
            
            # Add the result to the state
            state["tool_results"].append(
                ToolResult(
                    tool_call_id=tool_call.id,
                    result=result
                )
            )
            
            # Add the tool result to the conversation
            tool_message = ToolMessage(content=json.dumps(result))
            tool_message.tool_call_id = tool_call.id
            state["messages"].append(tool_message)
        
        # Clear current tool calls
        state["current_tool_calls"] = []
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """
        Generate a final response based on the tool results.
        
        Args:
            state: Current agent state.
            
        Returns:
            AgentState: Updated agent state with final response.
        """
        # Get WebSocket server for notifications
        ws_server = get_websocket_server()
        ws_server.notify_thinking("Generating final response...")
        
        # Convert messages to the format expected by OpenAI
        openai_messages = []
        
        # Add the messages in the format OpenAI expects
        for message in state["messages"]:
            if isinstance(message, SystemMessage):
                openai_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                openai_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                msg_dict = {"role": "assistant"}
                if message.content:
                    msg_dict["content"] = message.content
                if hasattr(message, "tool_calls") and message.tool_calls:
                    msg_dict["tool_calls"] = message.tool_calls
                openai_messages.append(msg_dict)
            elif isinstance(message, ToolMessage):
                openai_messages.append({
                    "role": "tool",
                    "content": message.content,
                    "tool_call_id": message.tool_call_id if hasattr(message, "tool_call_id") else None
                })
        
        # Call the LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=0.2,
            max_tokens=1024
        )
        
        # Get the response message
        response_message = response.choices[0].message
        
        # Add the final response to the conversation
        state["messages"].append(AIMessage(content=response_message.content))
        
        # Set the final response
        state["final_response"] = response_message.content
        
        # Notify completion
        ws_server.notify_complete(response_message.content)
        
        return state
    
    def _should_continue(self, state: AgentState) -> Literal["call_llm", "execute_tools", "generate_response", END]:
        """
        Determine whether to continue the conversation or end it.
        
        Args:
            state: Current agent state.
            
        Returns:
            str: Next node to execute.
        """
        # If we have a final response, end the conversation
        if state["final_response"] is not None:
            return END
        
        # If there's an error, go to generate_response to provide a response about the error
        if state["error"]:
            return "generate_response"
        
        # If there are tool calls pending execution, execute them
        if state["current_tool_calls"]:
            return "execute_tools"
        
        # If there are tool results and no pending tool calls, generate a response
        if state["tool_results"]:
            return "generate_response"
        
        # Check if the last message was from the assistant
        for message in reversed(state["messages"]):
            if isinstance(message, AIMessage):
                if hasattr(message, "tool_calls") and message.tool_calls:
                    return "execute_tools"
                # If the assistant has responded without tool calls, end the conversation
                return END
        
        # If we haven't seen an assistant message yet, continue to call_llm
        return "call_llm"
    
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
        graph.add_node("call_llm", self._call_llm)
        graph.add_node("execute_tools", self._execute_tools)
        graph.add_node("generate_response", self._generate_response)
        
        # Set the entry point
        graph.add_edge(START, "parse_user_input")
        
        # Add basic edge from parse_user_input to call_llm
        graph.add_edge("parse_user_input", "call_llm")
        
        # Add conditional edges
        graph.add_conditional_edges(
            "call_llm",
            self._should_continue,
            {
                "call_llm": "call_llm",
                "execute_tools": "execute_tools",
                "generate_response": "generate_response",
                END: END
            }
        )
        
        graph.add_conditional_edges(
            "execute_tools",
            self._should_continue,
            {
                "call_llm": "call_llm",
                "execute_tools": "execute_tools",
                "generate_response": "generate_response",
                END: END
            }
        )
        
        graph.add_conditional_edges(
            "generate_response",
            self._should_continue,
            {
                "call_llm": "call_llm",
                "execute_tools": "execute_tools",
                "generate_response": "generate_response",
                END: END
            }
        )
        
        # Compile the graph
        return graph.compile()
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a message using the LangGraph agent."""
        try:
            # Initialize state with system message if needed
            initial_messages = []
            
            # Add system message
            initial_messages.append(SystemMessage(content=self.system_prompt))
            
            # Add user message
            initial_messages.append(HumanMessage(content=message))
            
            # Create initial state
            state = {
                "messages": initial_messages,
                "current_tool_calls": [],
                "tool_results": [],
                "error": None,
                "final_response": None
            }

            # Send initial thinking notification
            ws_server = get_websocket_server()
            ws_server.notify_thinking("Processing your message...")

            # Run the graph
            final_state = self.graph.invoke(state)
            
            # Extract tool calls from messages
            tool_calls = []
            for msg in final_state["messages"]:
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_result = None
                        for tr in final_state["tool_results"]:
                            if tr.tool_call_id == tc.get("id"):
                                tool_result = tr.result
                                break
                                
                        tool_calls.append({
                            "name": tc.get("function", {}).get("name", "unknown"),
                            "arguments": tc.get("function", {}).get("arguments", {}),
                            "result": tool_result
                        })

            # Get final response from the last assistant message
            final_response = None
            for msg in reversed(final_state["messages"]):
                if isinstance(msg, AIMessage):
                    final_response = msg.content
                    break

            # Send completion notification
            if final_state["error"]:
                ws_server.notify_error(final_state["error"])
            elif final_response:
                ws_server.notify_complete(final_response)

            # Return the processed message and tool calls
            return {
                "message": final_response,
                "tool_calls": tool_calls,
                "error": final_state["error"],
            }
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            ws_server = get_websocket_server()
            ws_server.notify_error(error_msg)
            return {"message": None, "tool_calls": [], "error": error_msg}
    
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
    agent = ReachyLangGraphAgent(model="gpt-4-turbo", api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Process a message
    response = agent.process_message("Can you move the robot's right arm up?")
    print(response) 