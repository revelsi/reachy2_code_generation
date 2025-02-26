#!/usr/bin/env python
"""
WebSocket server for real-time updates from the Reachy robot.

This module provides a WebSocket server that sends real-time updates about
the robot's status, actions, and sensor data to connected clients.
"""

import os
import sys
import json
import asyncio
import threading
import time
from typing import Dict, Any, List, Set
import websockets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class WebSocketServer:
    """WebSocket server for real-time updates from the Reachy robot."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        """
        Initialize the WebSocket server.
        
        Args:
            host: Host to run the server on.
            port: Port to run the server on.
        """
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.running = False
        self.server = None
        self.update_thread = None
        
        # Robot state
        self.robot_state = {
            "status": "disconnected",
            "arms": {
                "left": {"position": [0.0] * 7, "gripper_opening": 0.0},
                "right": {"position": [0.0] * 7, "gripper_opening": 0.0}
            },
            "head": {"position": [0.0, 0.0, 0.0]},
            "base": {"position": [0.0, 0.0, 0.0]},
            "last_action": None,
            "last_update": time.time()
        }
    
    async def register(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Register a new client.
        
        Args:
            websocket: WebSocket connection to register.
        """
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send initial state
        await websocket.send(json.dumps({
            "type": "state",
            "data": self.robot_state
        }))
    
    async def unregister(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Unregister a client.
        
        Args:
            websocket: WebSocket connection to unregister.
        """
        self.clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def send_to_clients(self, message: Dict[str, Any]) -> None:
        """
        Send a message to all connected clients.
        
        Args:
            message: Message to send.
        """
        if not self.clients:
            return
        
        # Convert message to JSON
        message_json = json.dumps(message)
        
        # Send to all clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.unregister(client)
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """
        Handle a client connection.
        
        Args:
            websocket: WebSocket connection.
            path: Connection path.
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                # Process incoming messages (if needed)
                try:
                    data = json.loads(message)
                    if data.get("type") == "ping":
                        await websocket.send(json.dumps({"type": "pong"}))
                except json.JSONDecodeError:
                    pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    def update_robot_state(self, new_state: Dict[str, Any]) -> None:
        """
        Update the robot state and notify clients.
        
        Args:
            new_state: New robot state.
        """
        # Update the state
        self.robot_state.update(new_state)
        self.robot_state["last_update"] = time.time()
        
        # Notify clients
        asyncio.run(self.send_to_clients({
            "type": "state",
            "data": self.robot_state
        }))
    
    def notify_action(self, action: Dict[str, Any]) -> None:
        """
        Notify clients about a robot action.
        
        Args:
            action: Action details.
        """
        # Update last action
        self.robot_state["last_action"] = action
        
        # Notify clients
        asyncio.run(self.send_to_clients({
            "type": "action",
            "data": action
        }))
    
    async def update_loop(self) -> None:
        """Periodic update loop for robot state."""
        while self.running:
            # In a real implementation, you would get the actual robot state here
            # For now, we'll just send a heartbeat
            await self.send_to_clients({
                "type": "heartbeat",
                "timestamp": time.time()
            })
            
            # Wait for next update
            await asyncio.sleep(1.0)
    
    async def start_server(self) -> None:
        """Start the WebSocket server."""
        self.running = True
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket server started at ws://{self.host}:{self.port}")
        
        # Start update loop
        asyncio.create_task(self.update_loop())
        
        # Keep the server running
        await self.server.wait_closed()
    
    def start(self) -> None:
        """Start the WebSocket server in a separate thread."""
        def run_server():
            asyncio.run(self.start_server())
        
        self.update_thread = threading.Thread(target=run_server)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def stop(self) -> None:
        """Stop the WebSocket server."""
        self.running = False
        if self.server:
            self.server.close()
        
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)


# Global WebSocket server instance
websocket_server = None


def get_websocket_server(host: str = "0.0.0.0", port: int = 8765) -> WebSocketServer:
    """
    Get the WebSocket server instance.
    
    Args:
        host: Host to run the server on.
        port: Port to run the server on.
        
    Returns:
        WebSocketServer: WebSocket server instance.
    """
    global websocket_server
    
    if websocket_server is None:
        websocket_server = WebSocketServer(host=host, port=port)
        websocket_server.start()
    
    return websocket_server


def update_robot_state(new_state: Dict[str, Any]) -> None:
    """
    Update the robot state and notify clients.
    
    Args:
        new_state: New robot state.
    """
    server = get_websocket_server()
    server.update_robot_state(new_state)


def notify_action(action: Dict[str, Any]) -> None:
    """
    Notify clients about a robot action.
    
    Args:
        action: Action details.
    """
    server = get_websocket_server()
    server.notify_action(action)


if __name__ == "__main__":
    # Parse command-line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="Reachy WebSocket Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8765, help="Port to run the server on")
    
    args = parser.parse_args()
    
    # Start the WebSocket server
    server = WebSocketServer(host=args.host, port=args.port)
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("Server stopped") 