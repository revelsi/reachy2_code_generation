# Reachy Code Generation

A Gradio-based interface for generating Python code to control the Reachy 2 robot.

## Overview

This project provides a simple, intuitive interface for generating Python code to control the Reachy 2 robot. Using natural language instructions, you can create code that leverages the robot's capabilities without needing to understand the full API.

## Features

- **Code Generation**: Generate Python code based on natural language instructions
- **Code Validation**: Automatically validate generated code for errors and best practices
- **Code Execution**: Execute the generated code directly on the Reachy robot
- **Intuitive Interface**: Simple Gradio-based web UI for easy interaction
- **Model Flexibility**: Support for various OpenAI models including GPT-4o-mini and more cost-effective options 

## System Requirements

- Python 3.10+
- OpenAI API key
- Reachy 2 robot (physical or virtual)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reachy_function_calling.git
cd reachy_function_calling
```

2. Install dependencies (choose one method):

**Using the setup script (recommended):**
```bash
# Source the script to automatically activate the virtual environment
source ./setup.sh
```

**OR using Make:**
```bash
make setup
# Then activate the virtual environment
source venv_py310/bin/activate
```

> **Note:** 
> - The setup script, when sourced (using `source ./setup.sh`), will automatically activate the virtual environment in your current shell.
> - The Make command cannot automatically activate the environment due to how Make works with subshells.
> - Both methods will create a fresh installation from scratch.

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```
Or create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4o-mini
```

## Advanced Setup

### Refreshing the SDK Documentation

If you need to update the Reachy 2 SDK documentation:

```bash
make refresh-sdk
```

This command will:
1. Pull the latest SDK documentation from the repository
2. Extract SDK API documentation
3. Collect SDK examples
4. Save the documentation for use by the code generation system

### Available Make Commands

The project includes several useful make commands:

```bash
make setup         # Set up the development environment
make clean         # Clean generated files and cache
make lint          # Run the linter on the codebase
make test          # Run code generation tests
make run-gradio    # Run the Gradio interface
make refresh-sdk   # Refresh the SDK documentation
```

## Project Focus

This project is focused on code generation for the Reachy 2 robot. It provides a user-friendly interface for generating Python code to control the robot based on natural language instructions. The code generation system uses the Reachy 2 SDK documentation to inform the AI model about available functions and their usage.

Previous functionality related to function calling and LangGraph agents has been deprecated in favor of the more flexible code generation approach.

## Usage

### Launch the Code Generation Interface

Run one of the following commands to start the Gradio interface:

```bash
# Using the launcher script
python launch_code_gen.py

# OR using make
make run-gradio
```

This will start a web server at http://localhost:7860 where you can:
- Enter natural language instructions
- See generated code with validation results
- Execute code directly on the robot
- Receive real-time feedback

### Command Line Options

The launcher supports several options:

```bash
python launch_code_gen.py --temperature 0.3 --max-tokens 5000 --port 7861
```

Available options:
- `--temperature`: Controls randomness (0.0 to 1.0, default: 0.2)
- `--max-tokens`: Maximum tokens to generate (default: 4000)
- `--port`: Web server port (default: 7860)
- `--share`: Create a public share link

## Example Usage

1. **Simple movement**: "Move the robot's right arm to position x=0.3, y=0.2, z=0.1"
2. **Complex motion**: "Make the robot wave its right hand for 3 seconds"
3. **Environmental interaction**: "Make the robot pick up an object in front of it"
4. **Combined actions**: "Turn the robot's head to face me, then wave with its right arm"

## Project Structure

- `agent/`: Code generation agent implementation
- `launch_code_gen.py`: Main launcher for the Gradio interface
- `config.py`: Configuration settings and model parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.