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
- **Automatic Tool Generation**: Tools are automatically generated from the Reachy 2 SDK documentation

## LangGraph Agent Integration

The project uses LangGraph to implement a sophisticated agent architecture that can handle complex interactions with the Reachy 2 robot. The LangGraph agent provides:

- **State Management**: Maintains conversation history and tool execution state
- **Tool Integration**: Dynamically loads and executes tools based on the Reachy 2 SDK
- **Flexible Implementation**: Can use either virtual or physical robot connections
- **Error Handling**: Robust error handling for tool execution failures

### Virtual Robot Mode

The agent is designed with a flexible approach to robot control:

1. **Tool Definitions**: Uses real tool definitions from the Reachy 2 SDK, ensuring compatibility with the actual robot API
2. **Implementation Mode**: Can operate in two modes:
   - **Virtual Mode** (default): Connects to a virtual Reachy 2 robot running in a Docker container on localhost. This virtual robot uses the exact same API as a physical robot, making it perfect for development and testing without requiring physical hardware.
   - **Physical Robot Mode**: Connects to a physical Reachy 2 robot for actual hardware control

The key insight is that the virtual robot is not a mock or simulation - it's the real Reachy SDK running in a Docker container, providing identical API behavior to a physical robot. This means code developed with the virtual robot will work seamlessly with a physical robot.

To configure the mode:

- Set the `REACHY_HOST` environment variable in your `.env` file:
  - Use `localhost` for virtual mode (Docker container)
  - Use the IP address of your physical robot for physical mode

Example `.env` configuration:
```
# Use virtual mode (Docker container on localhost)
REACHY_HOST=localhost

# OR: Connect to a physical robot
# REACHY_HOST=192.168.1.100
```

## System Requirements

- **Python**: 3.10+ (recommended)
- **OpenAI API key**: Required for natural language processing

## Setup Instructions

### Quick Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reachy_function_calling.git
cd reachy_function_calling
```

2. Set up the environment:
```bash
make setup
```

3. Activate the virtual environment:
```bash
source venv_py310/bin/activate  # On Windows: venv_py310\Scripts\activate
```

4. Generate tools from the Reachy 2 SDK:
```bash
make generate-tools
```

5. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```
Or create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4-turbo
```

### Refreshing SDK Documentation

If the Reachy 2 SDK has been updated, you can refresh the SDK documentation and regenerate the tools:

```bash
make refresh-sdk
```

This will:
1. Clone or update the Reachy 2 SDK repository
2. Extract the latest API documentation
3. Regenerate the tool definitions and implementations

## Running the Application

### Command Line Interface

To run the application in command line mode:

```bash
make run-cli
```

### Web Interface (Experimental)

To run the application with a basic web interface:

```bash
make run-web
```

## Using Generated Tools

The Reachy Function Calling system automatically generates tools from the Reachy 2 SDK documentation. These tools can be used in both mock mode (for testing without a physical robot) and real robot mode.

### Tool Categories

The generated tools are organized into several categories:

1. **Arm Control**: Tools for controlling the robot's arms (left and right)
2. **Head Control**: Tools for controlling the robot's head movements and expressions
3. **Base Control**: Tools for controlling the robot's mobile base
4. **Sensor Access**: Tools for accessing sensor data from the robot
5. **System Control**: Tools for managing the robot's system settings

### Using Tools via the Web Interface

When using the web interface:

1. Connect to the WebSocket server by clicking the "Connect" button
2. Type your natural language request in the chat input
3. The system will:
   - Process your request using the LangGraph agent
   - Display the agent's reasoning
   - Show any tool calls with their parameters
   - Execute the tools and display the results
   - Provide a final response

### Using Tools via the CLI

When using the command-line interface:

1. Run the application with `make run-cli`
2. Type your natural language request
3. The system will process your request and display:
   - The agent's reasoning
   - Tool calls with parameters
   - Tool execution results
   - Final response

### Example Tool Usage

Here are some examples of natural language requests that use the generated tools:

```
"Move the robot's right arm to position x=0.3, y=0.2, z=0.1"
"Turn the robot's head to look at me"
"What is the current position of the left arm?"
"Move the robot forward 1 meter"
"Make the robot wave its right hand"
```

### Tool Execution Flow

1. **Tool Selection**: The LangGraph agent selects the appropriate tool based on your request
2. **Parameter Extraction**: The agent extracts parameters from your request
3. **Tool Execution**: The system executes the tool with the provided parameters
4. **Result Notification**: The WebSocket server notifies clients about the execution result
5. **Response Generation**: The agent generates a response based on the tool execution result

## Testing with Virtual Reachy

The project includes tools for testing and demonstrating the virtual Reachy functionality without requiring a physical robot.

### Running the Virtual Reachy Tests

To verify that your environment is correctly set up to work with the virtual Reachy:

```bash
make test-virtual
```

This will run a series of tests that:
1. Verify connection to the virtual Reachy
2. Test agent initialization with the virtual robot
3. Execute basic robot commands
4. Test tool execution through the agent

### Interactive Virtual Reachy Demo

For an interactive demonstration of the virtual Reachy capabilities:

```bash
make demo-virtual
```

This launches an interactive command-line interface that allows you to:
- Control the robot's arms
- Move the robot's head
- Operate the grippers
- Access camera feeds
- Get robot information

The demo is a great way to explore the virtual Reachy functionality without using the full agent system.

## Development

### Testing

Run the test suite:

```bash
make test
```

### Linting

Run the linter:

```bash
make lint
```

## Advanced Configuration

For advanced configuration options, please refer to the documentation in the `docs` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.