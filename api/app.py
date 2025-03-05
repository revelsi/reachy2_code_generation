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
from agent.agent_router import AgentRouter, AgentMode
from agent.cli import setup_agent, DEFAULT_MODULES
from config import (
    OPENAI_API_KEY, MODEL, DEBUG, DISABLE_WEBSOCKET, API_HOST, API_PORT,
    get_model_config, update_model_config, AVAILABLE_MODELS
)

# Create Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Global agent instance
agent = None


def initialize_agent(
    api_key: Optional[str] = None,
    model_config: Optional[Dict[str, Any]] = None,
    focus_modules: List[str] = None,
    regenerate_tools: bool = False,
    mode: AgentMode = AgentMode.FUNCTION_CALLING,
) -> None:
    """
    Initialize the Reachy agent.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
        model_config: Model configuration. If None, will use the configuration from config.py.
        focus_modules: Optional list of module names to focus on (default: parts, orbita, utils).
        regenerate_tools: Whether to regenerate tool definitions and implementations.
        mode: The agent mode to use (function_calling or code_generation).
    """
    global agent
    
    # Use model configuration from config.py if not provided
    if model_config is None:
        model_config = get_model_config()
    
    print(f"Initializing agent with model: {model_config.get('model', MODEL)}")
    
    # Initialize the agent
    agent = setup_agent(
        api_key=api_key,
        model_config=model_config,
        focus_modules=focus_modules,
        regenerate_tools=regenerate_tools,
        mode=mode,
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
            "message": "User message",
            "mode": "function_calling" or "code_generation" (optional)
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
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get("message")
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get mode from request (optional)
        mode = data.get("mode")
        if mode:
            try:
                agent.set_mode(AgentMode(mode))
            except ValueError:
                return jsonify({"error": f"Invalid mode: {mode}"}), 400
        
        # Process message
        response = agent.process_message(message)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset() -> Response:
    """
    Reset the conversation state.
    
    Returns:
        JSON response indicating success
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        try:
            initialize_agent()
        except Exception as e:
            return jsonify({"error": f"Failed to initialize agent: {str(e)}"}), 500
    
    # Reset conversation
    agent.reset_conversation()
    
    return jsonify({"status": "success", "message": "Conversation reset"})


@app.route("/api/tools", methods=["GET"])
def get_tools() -> Response:
    """
    Get the list of available tools.
    
    Returns:
        JSON response with the list of tools
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        try:
            initialize_agent()
        except Exception as e:
            return jsonify({"error": f"Failed to initialize agent: {str(e)}"}), 500
    
    # Get tools
    tools = agent.get_available_tools()
    
    return jsonify({"tools": tools})


@app.route("/api/status", methods=["GET"])
def get_status() -> Response:
    """
    Get the status of the agent.
    
    Returns:
        JSON response with the agent status
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        return jsonify({
            "status": "not_initialized",
            "message": "Agent not initialized"
        })
    
    # Get agent status
    status = {
        "status": "ready",
        "mode": agent.get_mode(),
        "model_config": agent.get_model_config(),
        "tools_count": len(agent.get_available_tools())
    }
    
    return jsonify(status)


@app.route("/api/config", methods=["GET", "POST"])
def config() -> Response:
    """
    Get or update the agent configuration.
    
    GET:
        Returns the current configuration.
    
    POST:
        Updates the configuration.
        
        Request body:
            {
                "model": "gpt-4-turbo",
                "temperature": 0.2,
                "max_tokens": 4000,
                "mode": "function_calling" or "code_generation"
            }
    
    Returns:
        JSON response with the updated configuration
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        try:
            initialize_agent()
        except Exception as e:
            return jsonify({"error": f"Failed to initialize agent: {str(e)}"}), 500
    
    if request.method == "GET":
        # Get current configuration
        config = {
            "model_config": agent.get_model_config(),
            "mode": agent.get_mode(),
            "available_models": AVAILABLE_MODELS,
            "available_modes": [mode.value for mode in AgentMode]
        }
        
        return jsonify(config)
    
    elif request.method == "POST":
        # Update configuration
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Update model configuration
            model_config = {}
            if "model" in data:
                model_config["model"] = data["model"]
            if "temperature" in data:
                model_config["temperature"] = float(data["temperature"])
            if "max_tokens" in data:
                model_config["max_tokens"] = int(data["max_tokens"])
            if "top_p" in data:
                model_config["top_p"] = float(data["top_p"])
            if "frequency_penalty" in data:
                model_config["frequency_penalty"] = float(data["frequency_penalty"])
            if "presence_penalty" in data:
                model_config["presence_penalty"] = float(data["presence_penalty"])
            
            if model_config:
                agent.update_model_config(model_config)
            
            # Update mode
            if "mode" in data:
                try:
                    agent.set_mode(AgentMode(data["mode"]))
                except ValueError:
                    return jsonify({"error": f"Invalid mode: {data['mode']}"}), 400
            
            # Get updated configuration
            updated_config = {
                "model_config": agent.get_model_config(),
                "mode": agent.get_mode()
            }
            
            return jsonify(updated_config)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/mode", methods=["GET", "POST"])
def mode() -> Response:
    """
    Get or set the agent mode.
    
    GET:
        Returns the current mode.
    
    POST:
        Sets the mode.
        
        Request body:
            {
                "mode": "function_calling" or "code_generation"
            }
    
    Returns:
        JSON response with the updated mode
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        try:
            initialize_agent()
        except Exception as e:
            return jsonify({"error": f"Failed to initialize agent: {str(e)}"}), 500
    
    if request.method == "GET":
        # Get current mode
        return jsonify({"mode": agent.get_mode()})
    
    elif request.method == "POST":
        # Set mode
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            mode = data.get("mode")
            if not mode:
                return jsonify({"error": "No mode provided"}), 400
            
            try:
                agent.set_mode(AgentMode(mode))
            except ValueError:
                return jsonify({"error": f"Invalid mode: {mode}"}), 400
            
            return jsonify({"mode": agent.get_mode()})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/execute", methods=["POST"])
def execute_code() -> Response:
    """
    Execute code on the virtual Reachy robot.
    
    This endpoint takes Python code as input and executes it on the virtual Reachy robot.
    It returns the execution result, including success status, output, and any errors.
    
    Returns:
        Response: JSON response with execution results
    """
    global agent
    
    # Check if agent is initialized
    if agent is None:
        return jsonify({
            "success": False,
            "message": "Agent not initialized",
            "output": ""
        }), 500
    
    # Get code from request
    data = request.json
    if not data or "code" not in data:
        return jsonify({
            "success": False,
            "message": "No code provided",
            "output": ""
        }), 400
    
    code = data["code"]
    
    try:
        # Check if the agent has a code generation component
        if hasattr(agent, 'code_generator') and agent.code_generator:
            # Execute the code
            result = agent.code_generator.execute_code(code, confirm=False)
            return jsonify(result), 200
        else:
            return jsonify({
                "success": False,
                "message": "Code execution not supported by the current agent",
                "output": ""
            }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error executing code: {str(e)}",
            "output": "",
            "error": str(e)
        }), 500


def main():
    """Run the Flask app."""
    # Initialize agent
    initialize_agent()
    
    # Run app
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)


if __name__ == "__main__":
    main() 