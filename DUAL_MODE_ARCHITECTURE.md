# Dual-Mode Architecture and Model Configuration

This document provides an overview of the dual-mode architecture and model configuration implementation in the Reachy Function Calling project.

## Dual-Mode Architecture

The dual-mode architecture allows users to interact with the Reachy 2 robot in two different ways:

### 1. Function Calling Mode

In this mode, the agent uses OpenAI's function calling capability to:
- Analyze user requests and determine the appropriate robot functions to call
- Display the reasoning behind each function call
- Show the function call with parameters
- Request user permission before execution
- Display execution results

This mode is ideal for users who want to control the robot with natural language commands and see exactly what functions are being called.

### 2. Code Generation Mode

In this mode, the agent:
- Generates Python code based on natural language requests
- Validates the generated code for basic syntax and structure
- Displays the code with explanations
- Allows users to review and modify the code before execution

This mode is ideal for users who want to learn how to program the robot or who need more complex control sequences that can be saved and reused.

## Implementation Details

### Agent Router

The `AgentRouter` class (`agent/agent_router.py`) is the central component of the dual-mode architecture. It:
- Manages the current mode (function calling or code generation)
- Routes user messages to the appropriate agent based on the current mode
- Maintains state across mode switches
- Handles model configuration updates

### Code Generation Agent

The `ReachyCodeGenerationAgent` class (`agent/code_generation_agent.py`) is responsible for:
- Generating Python code based on natural language requests
- Validating the generated code for basic syntax and structure
- Providing explanations for the generated code
- Using the OpenAI API to generate high-quality code

### Web Interface

The web interface (`agent/web_interface.py`) has been updated to support both modes:
- Added a mode toggle to switch between function calling and code generation
- Implemented a code editor with syntax highlighting for code generation mode
- Added UI components for configuring model parameters
- Dynamically updates the UI based on the current mode

### CLI Interface

The CLI interface (`agent/cli.py`) has been updated to support both modes:
- Added command-line options for selecting the mode
- Implemented commands for switching modes during a session
- Enhanced output formatting for both modes
- Added support for model configuration updates

### API Endpoints

The API endpoints (`api/app.py`) have been updated to support both modes:
- Added endpoints for switching modes
- Enhanced response formatting for both modes
- Added endpoints for updating model configuration
- Improved error handling for both modes

## Model Configuration

The centralized model configuration system allows users to customize the behavior of the language models used by the agents.

### Configuration Options

The following configuration options are available:
- `model`: The OpenAI model to use (e.g., gpt-4-turbo, gpt-4o, gpt-3.5-turbo)
- `temperature`: Controls the randomness of the model's output (0.0 to 1.0)
- `max_tokens`: The maximum number of tokens to generate
- `top_p`: Controls the diversity of the model's output (0.0 to 1.0)
- `frequency_penalty`: Reduces repetition of token sequences (0.0 to 2.0)
- `presence_penalty`: Reduces repetition of topics (0.0 to 2.0)

### Implementation Details

The model configuration is centralized in the `config.py` file, which provides:
- Default configuration values
- Functions for getting and updating the configuration
- A list of available models
- Validation for configuration updates

The configuration can be updated through:
- The web interface
- The CLI interface
- The API endpoints

## Testing

A test script (`test_model_config.py`) has been created to verify the functionality of the model configuration system. It tests:
- The configuration module functions
- The `AgentRouter` model configuration functionality
- The `ReachyCodeGenerationAgent` model configuration functionality
- The agent mode switching functionality

## Future Enhancements

Planned enhancements for the dual-mode architecture and model configuration include:
- Advanced code validation with static analysis
- Code execution functionality
- Code templates for common operations
- Performance monitoring for model configuration
- Support for multi-step operations
- Code history and versioning
- Enhanced error recovery mechanisms 