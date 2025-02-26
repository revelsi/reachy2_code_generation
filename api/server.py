#!/usr/bin/env python
"""
Combined server for the Reachy function calling system.

This module provides a combined server that runs both the REST API and WebSocket server.
"""

import os
import sys
import threading
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import server modules
from api.app import app, initialize_agent
from api.websocket import get_websocket_server


def run_flask_app(host: str, port: int, debug: bool) -> None:
    """
    Run the Flask app.
    
    Args:
        host: Host to run the server on.
        port: Port to run the server on.
        debug: Whether to run in debug mode.
    """
    app.run(host=host, port=port, debug=debug)


def main() -> None:
    """Main entry point for the combined server."""
    parser = argparse.ArgumentParser(description="Reachy Agent Server")
    parser.add_argument("--api-host", default="0.0.0.0", help="Host to run the API server on")
    parser.add_argument("--api-port", type=int, default=5000, help="Port to run the API server on")
    parser.add_argument("--ws-host", default="0.0.0.0", help="Host to run the WebSocket server on")
    parser.add_argument("--ws-port", type=int, default=8765, help="Port to run the WebSocket server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--model", help="LLM model to use")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate tool definitions")
    
    args = parser.parse_args()
    
    print(f"Starting Reachy Agent Server")
    print(f"API server: http://{args.api_host}:{args.api_port}")
    print(f"WebSocket server: ws://{args.ws_host}:{args.ws_port}")
    
    # Initialize the agent
    initialize_agent(
        model=args.model,
        regenerate_tools=args.regenerate,
    )
    
    # Start the WebSocket server
    ws_server = get_websocket_server(host=args.ws_host, port=args.ws_port)
    
    # Start the Flask app in the main thread
    run_flask_app(host=args.api_host, port=args.api_port, debug=args.debug)


if __name__ == "__main__":
    main() 