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
import traceback
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
            "head": {"position": [0.0] * 3},
            "base": {"position": [0.0, 0.0, 0.0]},
            "last_action": None,
            "last_update": time.time()
        }
        
        # Start the server
        self.start()
    
    def start(self) -> None:
        """Start the WebSocket server."""
        if self.running:
            print("WebSocket server is already running")
            return
        
        # Start the server in a separate thread
        self.update_thread = threading.Thread(target=self._run_server)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        self.running = True
    
    def stop(self) -> None:
        """Stop the WebSocket server."""
        if not self.running:
            print("WebSocket server is not running")
            return
        
        # Stop the server
        if self.server:
            asyncio.run(self.server.close())
            self.server = None
        
        self.running = False
        print("WebSocket server stopped")
    
    def _run_server(self) -> None:
        """Run the WebSocket server in a separate thread."""
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Define the coroutine to start the server
            async def start_server_async():
                self.server = await websockets.serve(
                    self.handle_client,
                    self.host,
                    self.port
                )
                # Keep the server running
                await asyncio.Future()  # Run forever
            
            # Run the coroutine in the event loop
            loop.run_until_complete(start_server_async())
        except Exception as e:
            print(f"Error running WebSocket server: {e}")
            traceback.print_exc()
            self.running = False
    
    async def register(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Register a new client.
        
        Args:
            websocket: WebSocket connection.
        """
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address} (total: {len(self.clients)})")
        
        # Send initial state
        try:
            await websocket.send(json.dumps({
                "type": "state",
                "data": self.robot_state
            }))
        except Exception as e:
            print(f"Error sending initial state: {e}")
    
    async def unregister(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Unregister a client.
        
        Args:
            websocket: WebSocket connection.
        """
        if websocket in self.clients:
            self.clients.remove(websocket)
            print(f"Client disconnected: {websocket.remote_address} (total: {len(self.clients)})")
    
    async def send_to_clients(self, message: Dict[str, Any]) -> None:
        """
        Send a message to all connected clients.
        
        Args:
            message: Message to send.
        """
        if not self.clients:
            return
        
        # Convert message to JSON
        try:
            message_json = json.dumps(message)
        except Exception as e:
            print(f"Error converting message to JSON: {e}")
            return
        
        # Send message to all clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                print(f"Error sending message to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.unregister(client)
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path=None) -> None:
        """
        Handle a client connection.
        
        Args:
            websocket: WebSocket connection.
            path: Connection path (optional).
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                # Process incoming messages (if needed)
                try:
                    data = json.loads(message)
                    if data.get("type") == "ping":
                        await websocket.send(json.dumps({"type": "pong"}))
                    elif data.get("type") == "get_state":
                        await websocket.send(json.dumps({
                            "type": "state",
                            "data": self.robot_state
                        }))
                    elif data.get("type") == "message":
                        # Get the agent instance
                        from api.app import agent
                        if agent is None:
                            await websocket.send(json.dumps({
                                "type": "error",
                                "message": "Agent not initialized"
                            }))
                            continue
                        
                        # Process the message
                        try:
                            response = agent.process_message(data.get("content"))
                            
                            # Send the response
                            await websocket.send(json.dumps({
                                "type": "complete",
                                "content": response.get("message"),
                                "tool_calls": response.get("tool_calls", [])
                            }))
                        except Exception as e:
                            error_msg = f"Error processing message: {str(e)}"
                            print(error_msg)
                            traceback.print_exc()
                            await websocket.send(json.dumps({
                                "type": "error",
                                "message": error_msg
                            }))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON message"
                    }))
                except Exception as e:
                    print(f"Error processing message: {e}")
                    traceback.print_exc()
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error processing message: {str(e)}"
                    }))
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error handling client: {e}")
            traceback.print_exc()
        finally:
            await self.unregister(websocket)
    
    def update_robot_state(self, new_state: Dict[str, Any]) -> None:
        """
        Update the robot state and notify clients.
        
        Args:
            new_state: New robot state.
        """
        # Update the state
        try:
            self.robot_state.update(new_state)
            self.robot_state["last_update"] = time.time()
            
            # Create a task to notify clients
            if self.clients:
                message = {
                    "type": "state",
                    "data": self.robot_state
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error updating robot state: {e}")
            traceback.print_exc()
    
    def notify_action(self, action: Dict[str, Any]) -> None:
        """
        Notify clients about a robot action.
        
        Args:
            action: Action details.
        """
        try:
            # Update last action
            self.robot_state["last_action"] = action
            
            # Create a task to notify clients
            if self.clients:
                message = {
                    "type": "action",
                    "data": action
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying action: {e}")
            traceback.print_exc()
    
    def notify_thinking(self, content: str) -> None:
        """
        Notify clients about the agent's thinking process.
        
        Args:
            content: Thinking content.
        """
        try:
            if self.clients:
                message = {
                    "type": "thinking",
                    "content": content
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying thinking: {e}")
            traceback.print_exc()
    
    def notify_complete(self, content: str) -> None:
        """
        Notify clients about completion.
        
        Args:
            content: Completion content.
        """
        try:
            if self.clients:
                message = {
                    "type": "complete",
                    "content": content
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying completion: {e}")
            traceback.print_exc()
    
    def notify_function_call(self, name: str, parameters: Dict[str, Any], call_id: str) -> None:
        """
        Notify clients about a function call.
        
        Args:
            name: Function name.
            parameters: Function parameters.
            call_id: Function call ID.
        """
        try:
            if self.clients:
                message = {
                    "type": "function_call",
                    "name": name,
                    "parameters": parameters,
                    "id": call_id
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying function call: {e}")
            traceback.print_exc()
    
    def notify_tool_execution_result(self, call_id: str, result: Dict[str, Any]) -> None:
        """
        Notify clients about a tool execution result.
        
        Args:
            call_id: Function call ID.
            result: Tool execution result.
        """
        try:
            if self.clients:
                message = {
                    "type": "tool_result",
                    "id": call_id,
                    "result": result
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying tool execution result: {e}")
            traceback.print_exc()
    
    def notify_code_output(self, content: str) -> None:
        """
        Notify clients about code output.
        
        Args:
            content: Code output content.
        """
        try:
            if self.clients:
                message = {
                    "type": "code_output",
                    "content": content
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying code output: {e}")
            traceback.print_exc()
    
    def notify_error(self, message: str) -> None:
        """
        Notify clients about an error.
        
        Args:
            message: Error message.
        """
        try:
            if self.clients:
                message = {
                    "type": "error",
                    "message": message
                }
                self._schedule_task(self.send_to_clients(message))
        except Exception as e:
            print(f"Error notifying error: {e}")
            traceback.print_exc()

    def _schedule_task(self, coro):
        """
        Schedule a coroutine to run in the event loop.
        
        Args:
            coro: Coroutine to run.
        """
        try:
            # Try to get the current event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # Create a new event loop if none exists
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # If we're not in the event loop's thread, run in executor
            if threading.current_thread() is not threading.main_thread():
                future = asyncio.run_coroutine_threadsafe(coro, loop)
                return future.result()
            
            # We're in the main thread, create a task
            return asyncio.create_task(coro)
        except Exception as e:
            print(f"Error scheduling task: {e}")
            traceback.print_exc()


# Global WebSocket server instance
_WS_SERVER = None


def get_websocket_server(host: str = "0.0.0.0", port: int = 8765) -> WebSocketServer:
    """
    Get the WebSocket server instance.
    
    Args:
        host: Host to run the server on.
        port: Port to run the server on.
    
    Returns:
        WebSocketServer: WebSocket server instance.
    """
    global _WS_SERVER
    
    if _WS_SERVER is None:
        _WS_SERVER = WebSocketServer(host=host, port=port)
    
    return _WS_SERVER


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


def notify_tool_execution_result(call_id: str, result: Dict[str, Any]) -> None:
    """
    Notify clients about a tool execution result.
    
    Args:
        call_id: Function call ID.
        result: Tool execution result.
    """
    server = get_websocket_server()
    server.notify_tool_execution_result(call_id, result)


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