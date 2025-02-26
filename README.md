# Reachy Function Calling with Transparent Execution

## ⚠️ Current Development Status

**Note: This project is currently under active development and is not yet stable.**

The LangGraph agent implementation is being developed to replace the previous agent architecture. Several issues are currently being addressed:

- Tool discovery is not working correctly (0 tools loaded)
- The agent is running in mock mode by default
- Testing infrastructure is being set up to allow isolated testing

Please see the [TODO.md](TODO.md) file for a detailed list of current issues and planned work.

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
- **Modern Web Interface**: Clean, responsive UI for interacting with the robot

## System Requirements

- **Python**: 3.8+ (3.10 recommended)
- **Node.js**: v18.0.0+ (for frontend development)
- **OpenAI API key**: Required for natural language processing
- **Reachy 2 robot**: Optional - a mock robot is provided for testing

## Environment Requirements

- Python 3.10 or higher
- Virtual environment (created automatically by the setup process)

## Setup

The project requires Python 3.10 or higher. The setup process will automatically create a virtual environment with the correct Python version.

```bash
# Clone the repository
git clone https://github.com/yourusername/reachy-function-calling.git
cd reachy-function-calling

# Set up the environment (creates venv_py310 and installs dependencies)
make setup

# Activate the virtual environment
source venv_py310/bin/activate
```

If you're using pyenv to manage Python versions, the included `.python-version` file will automatically select Python 3.10.12.

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reachy_function_calling.git
cd reachy_function_calling
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

Or create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4-turbo
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Docker Setup

The application can be run using Docker for both development and production environments.

### Prerequisites

- Docker and Docker Compose installed on your system
- OpenAI API key

### Development with Docker

1. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

2. Start the development environment:
```bash
docker-compose up
```

This will:
- Start the backend server with hot-reloading
- Start the frontend development server with hot-reloading
- Mount your local code into the containers for real-time development

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api

### Production Deployment with Docker

1. Create a `.env` file with your production settings:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4-turbo
USE_MOCK=true  # Set to false if connecting to a real robot
REACHY_HOST=your_robot_ip  # If using a real robot
```

2. Build and start the production containers:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Access the production application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api

### Docker Configuration Options

You can customize the Docker deployment by setting these environment variables:

- `API_PORT`: Port for the backend API (default: 8000)
- `FRONTEND_PORT`: Port for the frontend (default: 3000)
- `MODEL`: OpenAI model to use (default: gpt-4-turbo)
- `REACHY_HOST`: Hostname or IP of the Reachy robot
- `USE_MOCK`: Whether to use a mock robot implementation
- `USE_VIRTUAL`: Whether to use a virtual robot with the real SDK

## Running the Application

### Option 1: Running the Full Stack (Backend + Frontend)

1. Start the backend server:
```bash
python api/server.py --api-port 8000 --ws-port 8000
```

2. In a separate terminal, start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

### Option 2: Using the HTML Preview (No Node.js Required)

If you don't have Node.js v18+ installed, you can still view the UI:

1. Start the backend server:
```bash
python api/server.py --api-port 8000 --ws-port 8000
```

2. Open `frontend/preview.html` directly in your browser

### Option 3: Running the Backend Only

```bash
# Start the API server
python api/server.py

# Start with custom ports
python api/server.py --api-port 5000 --ws-port 8765

# Start with a specific model
python api/server.py --model gpt-4-turbo
```

### Option 4: Simple Demo (Command Line)

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

## Error Handling

The application includes robust error handling:

- **Robot Connection**: If the physical Reachy robot is not available, the system automatically falls back to a mock implementation
- **WebSocket Reconnection**: The frontend automatically attempts to reconnect if the WebSocket connection is lost
- **API Error Handling**: All API endpoints include proper error handling and return appropriate status codes
- **User Feedback**: Errors are displayed to the user in the UI with clear messages

## Security Considerations

- **Function Call Approval**: All function calls require explicit user approval before execution
- **Input Validation**: All inputs are validated before being processed
- **Error Logging**: Errors are logged for debugging but sensitive information is not exposed
- **CORS Protection**: The API server includes CORS protection to prevent unauthorized access

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

#### Thinking Process
```json
{
  "type": "thinking",
  "content": "Reasoning process..."
}
```

#### Function Call
```json
{
  "type": "function_call",
  "name": "function_name",
  "parameters": {...},
  "id": "call_id"
}
```

#### Function Approval
```json
{
  "type": "function_approval",
  "id": "call_id",
  "approved": true
}
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Ensure the backend server is running
   - Check that the WebSocket port is not blocked by a firewall
   - Verify the WebSocket URL in the frontend configuration

2. **OpenAI API Key Issues**
   - Ensure your API key is correctly set in the `.env` file or as an environment variable
   - Check that your API key has sufficient credits

3. **Node.js Version**
   - The frontend requires Node.js v18.0.0 or higher
   - If you can't install Node.js v18+, use the HTML preview option

4. **Robot Connection Issues**
   - If connecting to a physical Reachy robot, ensure it's powered on and accessible
   - Check the IP address or hostname is correct
   - The system will automatically fall back to a mock implementation if the robot is unavailable

5. **Docker Issues**
   - If you encounter permission issues, try running Docker commands with `sudo`
   - For volume mounting issues, ensure your Docker has permission to access the local directories
   - If containers can't communicate, check that they're on the same Docker network

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Pollen Robotics](https://www.pollen-robotics.com/) for creating the Reachy robot
- [OpenAI](https://openai.com/) for their function calling API
- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent framework 