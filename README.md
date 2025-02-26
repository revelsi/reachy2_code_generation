# Reachy Function Calling with Transparent Execution

This repository contains a framework for transparent function calling with the Reachy 2 robot. It demonstrates how to create a system that:

1. Shows the reasoning behind each function call
2. Displays the function call with parameters
3. Requests user permission before execution
4. Shows execution results

## Features

- **Transparent Execution**: See the reasoning and parameters for each function call before it executes
- **User Approval**: Approve or reject each function call before it executes
- **OpenAI Integration**: Control the robot using natural language with OpenAI's function calling
- **Mock Robot**: Test the system without a physical robot
- **REST API**: Control the robot through a REST API
- **WebSocket Updates**: Receive real-time updates about the robot's status and actions

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key (for natural language control)
- Reachy 2 robot (optional - a mock robot is provided for testing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Reachy_function_calling.git
cd Reachy_function_calling
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

Or create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4-turbo
```

## Usage

### Simple Demo

The `simple_demo.py` script demonstrates the transparent function calling framework with minimal dependencies.

```bash
# Run with example commands
python agent/simple_demo.py --examples

# Run with natural language control
python agent/simple_demo.py --prompt "Make the robot wave its right arm"

# Run in interactive mode
python agent/simple_demo.py --interactive

# Auto-approve all function calls
python agent/simple_demo.py --auto-approve
```

### API Server

The API server provides both REST API and WebSocket endpoints for controlling the robot and receiving real-time updates.

```bash
# Start the API server
python api/server.py

# Start with custom ports
python api/server.py --api-port 5000 --ws-port 8765

# Start with a specific model
python api/server.py --model gpt-4-turbo
```

### API Client

The API client provides a simple way to interact with the API server.

```bash
# Run the API client example
python api/client_example.py

# Run only the REST API example
python api/client_example.py --rest

# Run only the WebSocket example
python api/client_example.py --ws
```

### Command-line Arguments

#### Simple Demo
- `--examples`: Run example commands
- `--prompt TEXT`: Natural language prompt for the robot
- `--interactive`: Run in interactive mode
- `--auto-approve`: Automatically approve all function calls
- `--model MODEL`: OpenAI model to use (default: gpt-4-turbo or value from MODEL env var)
- `--api-key KEY`: OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)

#### API Server
- `--api-host HOST`: Host to run the API server on (default: 0.0.0.0)
- `--api-port PORT`: Port to run the API server on (default: 5000)
- `--ws-host HOST`: Host to run the WebSocket server on (default: 0.0.0.0)
- `--ws-port PORT`: Port to run the WebSocket server on (default: 8765)
- `--debug`: Run in debug mode
- `--model MODEL`: OpenAI model to use
- `--regenerate`: Regenerate tool definitions

## API Reference

### REST API Endpoints

#### Chat
- **URL**: `/api/chat`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "message": "User message"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Agent's response",
    "tool_calls": [
      {
        "name": "function_name",
        "arguments": {"arg1": "value1"},
        "result": {"success": true, "result": "..."}
      }
    ]
  }
  ```

#### Reset Conversation
- **URL**: `/api/reset`
- **Method**: `POST`
- **Response**:
  ```json
  {
    "status": "Conversation reset successfully"
  }
  ```

#### Get Tools
- **URL**: `/api/tools`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "function_name",
          "description": "Function description",
          "parameters": {...}
        }
      }
    ]
  }
  ```

#### Get Status
- **URL**: `/api/status`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "agent_initialized": true,
    "model": "gpt-4-turbo",
    "robot": {...}
  }
  ```

#### Get/Update Configuration
- **URL**: `/api/config`
- **Method**: `GET`/`POST`
- **Request Body** (for POST):
  ```json
  {
    "model": "Model name",
    "focus_modules": ["module1", "module2"],
    "regenerate_tools": true
  }
  ```
- **Response**:
  ```json
  {
    "status": "Configuration updated",
    "model": "Model name",
    "focus_modules": ["module1", "module2"]
  }
  ```

### WebSocket Messages

#### State Update
```json
{
  "type": "state",
  "data": {
    "status": "connected",
    "arms": {...},
    "head": {...},
    "base": {...},
    "last_action": {...},
    "last_update": 1234567890
  }
}
```

#### Action Notification
```json
{
  "type": "action",
  "data": {
    "name": "action_name",
    "parameters": {...},
    "result": {...}
  }
}
```

#### Heartbeat
```json
{
  "type": "heartbeat",
  "timestamp": 1234567890
}
```

## Architecture

### SimpleTransparentExecutor

The `SimpleTransparentExecutor` class wraps functions to provide a transparent execution flow:

```python
executor = SimpleTransparentExecutor(auto_approve=False)
function = executor.register_function(my_function)
result = function(param1="value", reasoning="This is why I'm calling the function")
```

### MockReachy

The `MockReachy` class provides a simple mock implementation of the Reachy 2 robot for testing:

```python
reachy = MockReachy()
reachy.get_info()
reachy.move_arm("right", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
reachy.look_at(0.5, 0.3, 0.2)
reachy.move_base(1.0, 0.5, 45.0)
```

### ReachyLangGraphAgent

The `ReachyLangGraphAgent` class implements a graph-based agent using LangGraph:

```python
agent = ReachyLangGraphAgent(model="gpt-4-turbo")
response = agent.process_message("Can you move the robot's right arm up?")
```

### API Server

The API server provides both REST API and WebSocket endpoints:

```python
# Start the API server
from api.server import main
main()
```

### API Client

The API client provides a simple way to interact with the API server:

```python
from api.client_example import ReachyClient

client = ReachyClient()
response = client.send_message("Can you move the robot's right arm up?")
```

## Frontend Integration

You can integrate a custom frontend with the API server. Here are some options:

1. **Use the REST API and WebSocket endpoints**: Build a custom frontend that communicates with the API server.
2. **Embed in the existing Gradio interface**: Use the Gradio HTML component to embed custom components.
3. **Generate with Lovable**: Use Lovable to generate a modern, responsive frontend.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Reachy 2 SDK](https://github.com/pollen-robotics/reachy2-sdk)
- [OpenAI API](https://platform.openai.com/docs/api-reference) 