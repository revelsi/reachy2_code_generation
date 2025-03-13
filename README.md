# Reachy Function Calling with Transparent Execution

## ⚠️ Current Development Status

**Note: This project is currently under active development.**

The LangGraph agent implementation has been significantly improved with the following updates:

- ✅ Tool discovery and generation is now working correctly (208 tools loaded)
- ✅ API documentation extraction from the Reachy 2 SDK is functioning
- ✅ Tool implementations are generated with proper error handling and consistent return formats
- ✅ Comprehensive test suite has been implemented to verify tool functionality
- ✅ Centralized connection management through the new connection manager module
- ✅ Consistent tool implementation patterns across all generated tools
- ✅ Dual-mode architecture supporting both function calling and code generation
- ✅ Centralized model configuration management for easy customization
- ✅ Enhanced API structure with clear type information and usage examples
- ✅ Simplified system prompt with clear initialization and cleanup phases
- ✅ Enhanced API summary generation with detailed parameter information, constraints, and units
- ✅ Direct code execution with validation and user confirmation
- ✅ Improved connection handling with retry mechanisms for virtual Reachy
- ✅ Pollen Vision Integration: Support for Reachy's vision capabilities through pollen-vision library
- ✅ Recursive Code Correction: Automatic correction of validation errors in generated code (up to 3 attempts)
- ✅ Gradio Interface for Code Generation: Dedicated web interface with real-time status updates and feedback
- ✅ Arm Kinematics Understanding: Enhanced spatial awareness through forward and inverse kinematics knowledge, enabling precise 3D positioning and movement planning
- ✅ Reliable Movement Strategies: Improved guidance for joint angle control and proper Cartesian control with orientation matrices
- ✅ Enhanced Workspace Safety: Updated workspace guidelines based on empirical testing to prevent unreachable targets

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
- **Dual-Mode Architecture**: Switch between function calling and code generation modes
- **Centralized Model Configuration**: Easily customize model parameters across the application
- **Direct Code Execution**: Execute generated code directly on the virtual Reachy robot
- **Code Validation**: Validate generated code before execution to ensure safety
- **Connection Retry**: Improved connection handling with retry mechanisms for virtual Reachy
- **Simplified Execution Workflow**: Streamlined code execution with minimal validation steps
- **Model Flexibility**: Support for various OpenAI models including gpt-4o-mini for cost-effective operation
- **Pollen Vision Integration**: Support for Reachy's vision capabilities through pollen-vision library
- **Recursive Code Correction**: Automatic correction of validation errors in generated code (up to 3 attempts)
- **Gradio Interface for Code Generation**: Dedicated web interface with real-time status updates and feedback
- **Arm Kinematics Understanding**: Enhanced spatial awareness through forward and inverse kinematics knowledge, enabling precise 3D positioning and movement planning

## Dual-Mode Architecture

The project implements a dual-mode architecture that allows users to interact with the Reachy 2 robot in two different ways:

### Function Calling Mode

In this mode, the agent uses OpenAI's function calling capability to:
- Analyze user requests and determine the appropriate robot functions to call
- Display the reasoning behind each function call
- Show the function call with parameters
- Request user permission before execution
- Display execution results

### Code Generation Mode

In this mode, the agent:
- Generates Python code based on natural language requests
- Validates the generated code for basic syntax and structure
- Displays the code with explanations
- Allows users to review and modify the code before execution
- Executes the code directly on the virtual Reachy robot with user confirmation

Users can switch between these modes through the web interface or CLI, providing flexibility in how they interact with the robot.

## Code Execution Features

The project now includes robust code execution capabilities:

- **Direct Execution**: Execute generated code directly on the virtual Reachy robot
- **Code Validation**: Validate code before execution to ensure safety
- **Automatic Code Correction**: Recursively correct validation errors in generated code
- **User Confirmation**: Request user confirmation before executing code
- **Safe Execution Wrapper**: Automatically wrap code in try/finally blocks to ensure proper cleanup
- **Execution Results**: Display detailed execution results including output and errors
- **Connection Retry**: Improved connection handling with retry mechanisms for virtual Reachy
- **Force Execution**: Option to force execution even if validation fails (with appropriate warnings)

### Code Execution Flow

1. **Code Generation**: The agent generates Python code based on a natural language request
2. **Code Validation**: The code is validated for syntax, imports, and safety
3. **Automatic Correction**: If validation errors are detected, the code is automatically corrected (up to 3 attempts)
4. **User Confirmation**: The user is asked to confirm execution
5. **Safe Execution**: The code is wrapped in a safe execution wrapper and executed
6. **Result Display**: Execution results are displayed, including output and any errors

## Model Configuration

The project includes a centralized model configuration system that allows users to:
- Select different OpenAI models (e.g., gpt-4-turbo, gpt-4o, gpt-3.5-turbo)
- Adjust model parameters such as temperature, max tokens, and more
- Update model settings at runtime through the web interface or API
- Maintain consistent model settings across different components of the application

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

### Refreshing SDK Documentation and Tools

If the Reachy 2 SDK has been updated, or if you need to regenerate the tool implementations, you can use:

```bash
# To refresh SDK documentation and regenerate tools
make refresh-sdk

# To only regenerate tools from existing documentation
make generate-tools
```

The `generate-tools` command will:
1. Clean existing tool implementations
2. Load the API documentation
3. Generate fresh tool definitions
4. Create tool implementations with consistent patterns
5. Ensure proper connection handling through the connection manager

This is useful when:
- The SDK has been updated
- You've modified the tool generation templates
- You need to ensure all tools follow the latest implementation patterns

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

## Enhanced API Documentation Structure

The project now includes an enhanced API documentation structure that provides clearer type information and usage examples for the Reachy 2 SDK. This improved structure helps the code generation agent produce more accurate and reliable code.

### Key Features of the Enhanced API Structure

- **Clear Type Information**: Explicit distinction between properties and methods
- **Detailed Parameter Descriptions**: Comprehensive information about parameter types and purposes
- **Usage Examples**: Concrete examples for each API component
- **Common Patterns**: Ready-to-use code patterns for common operations
- **Hierarchical Organization**: Structured representation of the API's modules, classes, and methods

The enhanced API structure is stored in `agent/docs/enhanced_api_structure.json` and is used by the code generation agent to generate more accurate code.

### Simplified System Prompt

The code generation agent now uses a simplified system prompt with a clear three-phase structure:

1. **Initialization Phase**: Steps for connecting to the robot and preparing it for use
2. **Main Code Phase**: Guidelines for implementing the core functionality
3. **Cleanup Phase**: Instructions for properly cleaning up resources

This structured approach helps ensure that generated code follows best practices, including:
- Always turning on the robot before use
- Using proper error handling with try/finally blocks
- Always turning off the robot smoothly and disconnecting when done

## Enhanced API Documentation

The project includes an enhanced API documentation system that significantly improves the code generation agent's ability to generate accurate code:

### API Summary Enhancement

The API summary generation has been enhanced to provide more detailed information about function parameters, including:

1. **Parameter Types**: Extracted from function signatures
2. **Parameter Descriptions**: Extracted from function docstrings
3. **Parameter Constraints**: Extracted from docstrings and added manually for known problematic functions
4. **Units Information**: Extracted from docstrings (e.g., degrees vs. radians)

This enhancement addresses issues with improper function definitions and helps prevent common errors in the generated code.

### Arm Kinematics Documentation

The project now includes comprehensive documentation about Reachy2's arm kinematics, focusing on giving the agent a spatial sense of its body through natural language explanation rather than code examples:

1. **Spatial Awareness**: Detailed explanation of Reachy's coordinate system and how its body exists in 3D space
2. **Body Representation**: Description of the arm's structure with 7 degrees of freedom, similar to a human arm
3. **Kinematic Concepts**: Clear explanations of joint space vs. cartesian space, forward and inverse kinematics
4. **Workspace Understanding**: Information about reachability, singularities, and physical limitations
5. **Embodied Cognition**: Guidance on thinking like the robot when planning movements
6. **Movement Guidelines**: Explicit principles for generating kinematically-aware robot movements

The agent is instructed to ALWAYS apply these movement guidelines when generating code:
- Think spatially about the robot's body and targets in 3D space
- Check reachability before attempting movements
- Prefer natural, human-like movement patterns
- Maintain awareness of both position and orientation
- Avoid singularities and problematic configurations
- Consider how starting positions affect movement solutions
- Allow sufficient time for smooth, safe movements

This conceptual understanding enables the agent to reason more effectively about:
- How to position the arm to reach specific points in space
- Natural and efficient ways to move between positions
- Appropriate hand orientations for different tasks
- Limitations of the robot's physical capabilities

The kinematics documentation is available in `agent/docs/reachy2_kinematics_guide.md` and is integrated into the agent's system prompt as natural language explanation with minimal code.

### Implementation Details

The enhanced API summary generation includes:

- **Parameter Details Extraction**: Robust parsing of function signatures and docstrings
- **Special Constraints**: Additional constraints for known problematic functions
- **Improved Format**: Hierarchical organization of API components with detailed parameter information

### Testing

The enhanced API summary generation has been thoroughly tested with:

- **Unit Tests**: Verifying the extraction of parameter details
- **Integration Tests**: Testing the code generation agent with the enhanced API summary

## Quick Start

### Running the Code Generation Interface

To quickly start the code generation interface, run:

```bash
python launch_code_gen.py
```

This will launch a Gradio web interface at http://localhost:7860 where you can:
- Generate Python code for the Reachy robot using natural language
- See real-time status updates during the generation process
- View code validation results and automatic corrections
- Execute the generated code and see detailed feedback

The interface uses GPT-4o-mini, which is optimized for Reachy 2 code generation, providing a good balance between performance and cost efficiency.

#### Code Validation Process

When code is generated, it goes through these validation steps:
1. **Syntax Check**: Ensures the code has valid Python syntax
2. **Import Validation**: Verifies all imports are available
3. **API Usage Check**: Confirms correct usage of the Reachy API
4. **Safety Check**: Looks for potentially harmful operations

When issues are found, the model will attempt to fix them automatically (up to 3 correction attempts). The interface provides transparency about this process, showing:
- What issues were found
- Whether they were successfully fixed
- A detailed correction history

You can customize the interface with command-line arguments:

```bash
python launch_code_gen.py --temperature 0.3 --max-tokens 5000 --port 7861 --websocket-port 8766
```