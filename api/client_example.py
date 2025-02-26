#!/usr/bin/env python
"""
Example client for the Reachy API.

This module demonstrates how to use the Reachy API from a client application.
"""

import sys
import json
import time
import asyncio
import websockets
import requests
from typing import Dict, Any, List, Optional


class ReachyClient:
    """Client for the Reachy API."""
    
    def __init__(
        self,
        api_url: str = "http://localhost:5000",
        ws_url: str = "ws://localhost:8765"
    ):
        """
        Initialize the Reachy client.
        
        Args:
            api_url: URL of the REST API.
            ws_url: URL of the WebSocket server.
        """
        self.api_url = api_url
        self.ws_url = ws_url
        self.ws = None
        self.ws_connected = False
    
    def send_message(self, message: str) -> Dict[str, Any]:
        """
        Send a message to the agent.
        
        Args:
            message: Message to send.
            
        Returns:
            Dict[str, Any]: Agent's response.
        """
        url = f"{self.api_url}/api/chat"
        data = {"message": message}
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def reset_conversation(self) -> Dict[str, Any]:
        """
        Reset the conversation with the agent.
        
        Returns:
            Dict[str, Any]: Response from the server.
        """
        url = f"{self.api_url}/api/reset"
        
        response = requests.post(url)
        response.raise_for_status()
        
        return response.json()
    
    def get_tools(self) -> Dict[str, Any]:
        """
        Get the list of available tools.
        
        Returns:
            Dict[str, Any]: Available tools.
        """
        url = f"{self.api_url}/api/tools"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of the robot and agent.
        
        Returns:
            Dict[str, Any]: Status information.
        """
        url = f"{self.api_url}/api/status"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the agent configuration.
        
        Returns:
            Dict[str, Any]: Agent configuration.
        """
        url = f"{self.api_url}/api/config"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def update_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the agent configuration.
        
        Args:
            config: New configuration.
            
        Returns:
            Dict[str, Any]: Updated configuration.
        """
        url = f"{self.api_url}/api/config"
        
        response = requests.post(url, json=config)
        response.raise_for_status()
        
        return response.json()
    
    async def connect_websocket(self) -> None:
        """Connect to the WebSocket server."""
        if self.ws_connected:
            return
        
        try:
            self.ws = await websockets.connect(self.ws_url)
            self.ws_connected = True
            print(f"Connected to WebSocket server at {self.ws_url}")
        except Exception as e:
            print(f"Error connecting to WebSocket server: {e}")
            self.ws_connected = False
    
    async def disconnect_websocket(self) -> None:
        """Disconnect from the WebSocket server."""
        if not self.ws_connected:
            return
        
        try:
            await self.ws.close()
            self.ws_connected = False
            print("Disconnected from WebSocket server")
        except Exception as e:
            print(f"Error disconnecting from WebSocket server: {e}")
    
    async def receive_updates(self, callback) -> None:
        """
        Receive updates from the WebSocket server.
        
        Args:
            callback: Callback function to handle updates.
        """
        if not self.ws_connected:
            await self.connect_websocket()
        
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    callback(data)
                except json.JSONDecodeError:
                    print(f"Received invalid JSON: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
            self.ws_connected = False
    
    async def send_ping(self) -> None:
        """Send a ping message to the WebSocket server."""
        if not self.ws_connected:
            await self.connect_websocket()
        
        try:
            await self.ws.send(json.dumps({"type": "ping"}))
        except Exception as e:
            print(f"Error sending ping: {e}")
            self.ws_connected = False


async def websocket_example() -> None:
    """Example of using the WebSocket client."""
    client = ReachyClient()
    
    # Define a callback function to handle updates
    def handle_update(data):
        print(f"Received update: {json.dumps(data, indent=2)}")
    
    # Connect to the WebSocket server
    await client.connect_websocket()
    
    # Start receiving updates in the background
    asyncio.create_task(client.receive_updates(handle_update))
    
    # Send a ping every 5 seconds
    for _ in range(5):
        await client.send_ping()
        await asyncio.sleep(5)
    
    # Disconnect from the WebSocket server
    await client.disconnect_websocket()


def rest_api_example() -> None:
    """Example of using the REST API client."""
    client = ReachyClient()
    
    # Get the agent status
    print("\n=== Agent Status ===")
    status = client.get_status()
    print(json.dumps(status, indent=2))
    
    # Get the available tools
    print("\n=== Available Tools ===")
    tools = client.get_tools()
    print(f"Number of tools: {len(tools.get('tools', []))}")
    
    # Reset the conversation
    print("\n=== Reset Conversation ===")
    reset = client.reset_conversation()
    print(json.dumps(reset, indent=2))
    
    # Send a message
    print("\n=== Send Message ===")
    response = client.send_message("Can you move the robot's right arm up?")
    print(f"Response: {response.get('response')}")
    print("\nTool Calls:")
    for tool_call in response.get("tool_calls", []):
        print(f"- {tool_call.get('name')}: {tool_call.get('arguments')}")
        print(f"  Result: {tool_call.get('result')}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Reachy API Client Example")
    parser.add_argument("--api-url", default="http://localhost:5000", help="URL of the REST API")
    parser.add_argument("--ws-url", default="ws://localhost:8765", help="URL of the WebSocket server")
    parser.add_argument("--rest", action="store_true", help="Run the REST API example")
    parser.add_argument("--ws", action="store_true", help="Run the WebSocket example")
    
    args = parser.parse_args()
    
    # If no examples specified, run both
    if not args.rest and not args.ws:
        args.rest = True
        args.ws = True
    
    # Run the REST API example
    if args.rest:
        print("=== REST API Example ===")
        rest_api_example()
    
    # Run the WebSocket example
    if args.ws:
        print("\n=== WebSocket Example ===")
        asyncio.run(websocket_example()) 