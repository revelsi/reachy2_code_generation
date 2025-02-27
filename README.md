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