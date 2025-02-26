#!/usr/bin/env python
"""
REST API for the Reachy function calling system.

This module provides a Flask-based REST API for interacting with the Reachy agent.
It allows frontend applications to send commands, get robot status, and manage conversations.
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import agent modules
from agent.langgraph_agent import ReachyLangGraphAgent
from agent.cli import setup_agent, DEFAULT_MODULES

# Create Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Global agent instance
agent = None


def initialize_agent(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    focus_modules: List[str] = None,
    regenerate_tools: bool = False,
) -> None:
    """
    Initialize the Reachy agent.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
        model: LLM model to use. If None, will use MODEL environment variable or default to gpt-4-turbo.
        focus_modules: Optional list of module names to focus on (default: parts, orbita, utils).
        regenerate_tools: Whether to regenerate tool definitions and implementations.
    """
    global agent
    
    # Use model from environment variable if not provided
    if model is None:
        model = os.environ.get("MODEL", "gpt-4-turbo")
    
    print(f"Initializing agent with model: {model}")
    
    # Initialize the agent
    agent = setup_agent(
        api_key=api_key,
        model=model,
        focus_modules=focus_modules,
        regenerate_tools=regenerate_tools,
    )


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/api/chat", methods=["POST"])
def chat() -> Response:
    """
    Process a chat message and return the agent's response.
    
    Request body:
        {
            "message": "User message"
        }
    
    Returns:
        JSON response with the agent's reply and tool calls
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        try:
            initialize_agent()
        except Exception as e:
            return jsonify({"error": f"Failed to initialize agent: {str(e)}"}), 500
    
    # Get message from request
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        
        if "message" not in data:
            return jsonify({"error": "Missing 'message' field in request body"}), 400
        
        message = data["message"]
        
        # Process the message
        try:
            response = agent.process_message(message)
            
            # Extract tool calls for visualization
            tool_calls = []
            for msg in agent.state.messages:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        # Find the corresponding result if available
                        result = None
                        if hasattr(agent.state, "tool_results"):
                            for tool_result in agent.state.tool_results:
                                if tool_result.tool_call_id == tool_call.get("id"):
                                    result = tool_result.result
                                    break
                        
                        # Add to tool calls
                        tool_calls.append({
                            "name": tool_call.get("function", {}).get("name", "unknown"),
                            "arguments": tool_call.get("function", {}).get("arguments", {}),
                            "result": result
                        })
            
            return jsonify({
                "response": response,
                "tool_calls": tool_calls
            })
        
        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            print(f"Error in chat endpoint: {error_message}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": error_message}), 500
            
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400


@app.route("/api/reset", methods=["POST"])
def reset() -> Response:
    """
    Reset the conversation with the agent.
    
    Returns:
        JSON response confirming the reset
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        initialize_agent()
    else:
        # Reset the conversation
        agent.reset_conversation()
    
    return jsonify({"status": "Conversation reset successfully"})


@app.route("/api/tools", methods=["GET"])
def get_tools() -> Response:
    """
    Get the list of available tools.
    
    Returns:
        JSON response with the available tools
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        initialize_agent()
    
    # Get available tools
    tools = agent.get_available_tools()
    
    return jsonify({"tools": tools})


@app.route("/api/status", methods=["GET"])
def get_status() -> Response:
    """
    Get the status of the robot and agent.
    
    Returns:
        JSON response with the status information
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        return jsonify({"status": "Agent not initialized"}), 404
    
    # Get agent status
    status = {
        "agent_initialized": agent is not None,
        "model": os.environ.get("MODEL", "gpt-4-turbo"),
    }
    
    # Try to get robot status if available
    try:
        # This assumes the agent has a method to get robot status
        # You may need to adjust this based on your actual implementation
        robot_status = agent.get_robot_status()
        status["robot"] = robot_status
    except:
        status["robot"] = {"status": "Unknown"}
    
    return jsonify(status)


@app.route("/api/config", methods=["GET", "POST"])
def config() -> Response:
    """
    Get or update the agent configuration.
    
    For GET:
        Returns the current configuration
        
    For POST:
        Request body:
            {
                "model": "Model name",
                "focus_modules": ["module1", "module2"],
                "regenerate_tools": true/false
            }
        
        Returns the updated configuration
    """
    global agent
    
    if request.method == "GET":
        # Return current configuration
        config = {
            "model": os.environ.get("MODEL", "gpt-4-turbo"),
            "focus_modules": DEFAULT_MODULES,
        }
        return jsonify(config)
    
    elif request.method == "POST":
        # Update configuration
        data = request.json
        if not data:
            return jsonify({"error": "Missing configuration data"}), 400
        
        # Extract configuration values
        model = data.get("model", os.environ.get("MODEL", "gpt-4-turbo"))
        focus_modules = data.get("focus_modules", DEFAULT_MODULES)
        regenerate_tools = data.get("regenerate_tools", False)
        
        # Reinitialize the agent with new configuration
        initialize_agent(
            model=model,
            focus_modules=focus_modules,
            regenerate_tools=regenerate_tools,
        )
        
        return jsonify({
            "status": "Configuration updated",
            "model": model,
            "focus_modules": focus_modules,
        })


if __name__ == "__main__":
    # Parse command-line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="Reachy Agent API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--model", help="LLM model to use")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions")
    
    args = parser.parse_args()
    
    # Initialize the agent
    initialize_agent(
        model=args.model,
        regenerate_tools=args.regenerate,
    )
    
    # Run the Flask app
    app.run(host=args.host, port=args.port, debug=args.debug) 