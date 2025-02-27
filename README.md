# Reachy Function Calling with Transparent Execution

## ⚠️ Current Development Status

**Note: This project is currently under active development.**

The LangGraph agent implementation has been significantly improved with the following updates:

- ✅ Tool discovery and generation is now working correctly (208 tools loaded)
- ✅ API documentation extraction from the Reachy 2 SDK is functioning
- ✅ Tool implementations are generated with proper error handling and consistent return formats
- ✅ Comprehensive test suite has been implemented to verify tool functionality

The agent uses real tool definitions from the Reachy 2 SDK but can operate with mock implementations when no physical robot is available.

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
- **Automatic Tool Generation**: Tools are automatically generated from the Reachy 2 SDK documentation

## LangGraph Agent Integration

The project uses LangGraph to implement a sophisticated agent architecture that can handle complex interactions with the Reachy 2 robot. The LangGraph agent provides:

- **State Management**: Maintains conversation history and tool execution state
- **Tool Integration**: Dynamically loads and executes tools based on the Reachy 2 SDK
- **Flexible Implementation**: Can use either mock implementations or real robot connections
- **Error Handling**: Robust error handling for tool execution failures

### Real Tools with Mock Mode

The agent is designed with a flexible approach to robot control:

1. **Tool Definitions**: Always uses real tool definitions from the Reachy 2 SDK, ensuring compatibility with the actual robot API
2. **Implementation Mode**: Can operate in two modes:
   - **Mock Mode** (default): Uses mock implementations that simulate robot behavior without requiring physical hardware
   - **Real Robot Mode**: Connects to a physical Reachy 2 robot for actual hardware control

To configure the mode:

- Set the `USE_MOCK` environment variable to `true` or `false` in your `.env` file
- Set the `REACHY_HOST` environment variable to specify the robot's IP address or hostname when using real robot mode

Example `.env` configuration:
```
# Use mock implementations (no physical robot required)
USE_MOCK=true
REACHY_HOST=localhost

# OR: Connect to a real robot
# USE_MOCK=false
# REACHY_HOST=192.168.1.100
```

## System Requirements

- **Python**: 3.8+ (3.10 recommended)
- **Node.js**: v18.0.0+ (for frontend development)
- **OpenAI API key**: Required for natural language processing
- **Reachy 2 robot**: Optional - a mock robot is provided for testing

## Environment Requirements

- Python 3.10 or higher
- Virtual environment (created automatically by the setup process)

## Development Environment Setup

For a consistent development experience, we provide setup scripts that ensure you're working in the correct environment with all necessary dependencies.

### Using the Setup Scripts

#### On macOS/Linux:
```bash
# Run the setup script
./start_dev.sh
```

#### On Windows:
```batch
# Run the setup script
start_dev.bat
```

These scripts will:
1. Check if you're in the correct virtual environment and activate/create it if needed
2. Verify all dependencies are installed
3. Check environment variables and create a `.env` file if needed
4. Verify that tools are properly generated
5. Provide helpful commands to get started

### Manual Setup

If you prefer to set up the environment manually:

```bash
# Clone the repository
git clone https://github.com/yourusername/reachy-function-calling.git
cd reachy-function-calling

# Set up the environment (creates venv_py310 and installs dependencies)
make setup

# Activate the virtual environment
source venv_py310/bin/activate  # On Windows: venv_py310\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate tools from API documentation
make generate-tools

# Verify tools
python verify_tools.py
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

2. Open `