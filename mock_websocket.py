"""
Mock implementation of the WebSocket server for testing.

This provides a simple mock of the WebSocket server that captures notifications
instead of trying to send them to actual clients.
"""

import logging

logger = logging.getLogger("mock_websocket")


class MockWebSocketServer:
    """
    A mock implementation of the WebSocket server that logs notifications
    instead of sending them to actual clients.
    """
    
    def __init__(self):
        self.messages = []
        self.thinking_messages = []
        self.error_messages = []
        self.function_calls = []
        
    def notify_thinking(self, message: str):
        """Log a thinking notification."""
        logger.info(f"THINKING: {message}")
        self.thinking_messages.append(message)
        
    def notify_error(self, message: str):
        """Log an error notification."""
        logger.error(f"ERROR: {message}")
        self.error_messages.append(message)
        
    def notify_function_call(self, function_name: str, arguments: dict, tool_call_id: str):
        """Log a function call notification."""
        logger.info(f"FUNCTION CALL: {function_name}({arguments})")
        self.function_calls.append({
            "name": function_name,
            "arguments": arguments,
            "id": tool_call_id
        })
        
    def notify_complete(self, message: str):
        """Log a completion notification."""
        logger.info(f"COMPLETE: {message}")
        self.messages.append(message)
        
    def get_all_notifications(self):
        """Get all captured notifications."""
        return {
            "thinking": self.thinking_messages,
            "errors": self.error_messages,
            "function_calls": self.function_calls,
            "completions": self.messages
        }


# Global instance that can be imported and used for testing
_mock_websocket_server = MockWebSocketServer()


def get_websocket_server():
    """Get the mock WebSocket server instance."""
    return _mock_websocket_server 