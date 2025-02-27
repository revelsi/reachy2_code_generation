#!/usr/bin/env python
"""
Visualize the LangGraph agent's workflow graph.

This script creates a text-based representation of the LangGraph agent's workflow graph,
showing the nodes and edges that define the agent's behavior.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.agent.langgraph_agent import ReachyLangGraphAgent
from langgraph.graph import END


def visualize_agent_graph():
    """
    Create and display a text-based representation of the LangGraph agent's workflow graph.
    """
    print("Creating LangGraph agent graph visualization...")
    
    # Get model from environment variable with fallback
    model = os.environ.get("MODEL", "gpt-4-turbo")
    
    # Create agent with a mock API key (we won't be making any API calls)
    agent = ReachyLangGraphAgent(api_key="mock_api_key", model=model)
    
    print(f"Using model: {model}")
    
    # Get the graph
    graph = agent.graph
    
    # Print ASCII art representation of the graph
    print("\n" + "=" * 50)
    print("REACHY 2 AGENT WORKFLOW GRAPH")
    print("=" * 50)
    
    # Since we can't directly access the graph structure in the current version,
    # we'll display the hardcoded structure based on our implementation
    
    # Print nodes
    print("\nNODES:")
    print("------")
    nodes = ["parse_user_input", "select_tool", "execute_tools", "generate_response"]
    for node in nodes:
        if node == "parse_user_input":
            print(f"  * {node} (ENTRY POINT)")
        else:
            print(f"  * {node}")
    
    # Print edges
    print("\nEDGES:")
    print("------")
    edges = [
        ("parse_user_input", "select_tool"),
        ("execute_tools", "generate_response"),
        ("generate_response", "END")
    ]
    for source, target in edges:
        print(f"  * {source} -> {target}")
    
    # Print conditional edges
    print("\nCONDITIONAL EDGES:")
    print("----------------")
    print("  * select_tool -> [_should_continue function] -> (execute_tools | generate_response | END)")
    
    # Print ASCII art of the graph
    print("\nGRAPH VISUALIZATION:")
    print("-------------------")
    print("""
    +------------------+     +---------------+
    | parse_user_input | --> |  select_tool  |
    +------------------+     +---------------+
                                    |
                                    | [_should_continue]
                                    v
                              +-----+-----+
                              |           |
                     +--------+           +--------+
                     |        |           |        |
                     v        v           v        v
        +----------------+    |    +-----------------+
        | execute_tools  | ---+--> | generate_response | --> [END]
        +----------------+         +-----------------+
    """)
    
    # Print workflow description
    print("\nWORKFLOW DESCRIPTION:")
    print("--------------------")
    print("1. Entry point: parse_user_input")
    print("   - Parses the user input and adds it to the conversation history")
    print("2. parse_user_input -> select_tool")
    print("   - Selects a tool to use based on the user input")
    print("3. select_tool -> _should_continue (conditional):")
    print("   - If there are tool calls: execute_tools")
    print("   - If there are tool results: generate_response")
    print("   - Otherwise: END")
    print("4. execute_tools -> generate_response")
    print("   - Executes the selected tools and adds results to the conversation")
    print("5. generate_response -> END")
    print("   - Generates a final response based on the tool results")
    
    # Print state information
    print("\nSTATE INFORMATION:")
    print("-----------------")
    print("The agent's state includes:")
    print("  * messages: List of conversation messages")
    print("  * current_tool_calls: List of pending tool calls")
    print("  * tool_results: List of tool execution results")
    print("  * error: Optional error message")
    print("  * final_response: Final response to return to the user")
    
    # Print code reference
    print("\nCODE REFERENCE:")
    print("--------------")
    print("The graph is defined in the _build_graph method of the ReachyLangGraphAgent class:")
    print("""
    def _build_graph(self) -> StateGraph:
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
    """)
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    visualize_agent_graph() 