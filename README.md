# Reachy 2 Code Generation
A powerful interface for generating, evaluating, and optimizing Python code for the Reachy 2 robot.

![Demo](./assets/demo.gif)


**Disclaimer** - This tool is in its early development stage. 
The backbone (code generation from natural language, code evaluation and direct execution on a fake Reachy robot) is functional, but the results can be erratic. As an example, the code generation tool does not yet have a good spatial understanding of Reachy and its surroundings, resulting in movements that don't necessarily align with what a user wants.

## Overview

This project provides an intuitive interface for controlling the Reachy 2 robot through natural language instructions. Simply describe what you want the robot to do, and the system generates, evaluates, and optimizes executable Python code using the Reachy 2 SDK.

## Key Features

- **Natural Language to Code**: Convert plain English instructions into Python code
- **Conversational Interface**: Intuitive chat-based interaction for natural back-and-forth communication
- **Code Generation Pipeline**: Three-stage process for high-quality code creation
  - **Generation**: Creates initial code from user requests using gpt-4.1
  - **Evaluation**: Assesses code quality, safety, and API correctness using gpt-4.1-mini
  - **Optimization**: Refines code based on evaluation feedback
- **Modern Interface**: Clean, responsive Gradio UI with intuitive two-column layout
- **Enhanced Code Editor**: Syntax highlighting with Source Code Pro font for better readability
- **Real-time Status Indicators**: Clear visual feedback for all operations
- **Interactive Gradio Interface**: User-friendly web interface with real-time feedback
- **Automatic Code Validation**: Identifies errors, warnings, and improvement opportunities
- **Direct Code Execution**: Run code on connected Reachy robots from the interface
- **Flexible Model Selection**: Support for various OpenAI models with configurable parameters
  - Supports GPT-family (gpt-4.1, gpt-4o, gpt-3.5-turbo, etc.)
  - Supports O-family reasoning models (o1, o1-mini, o3, o3-mini)

## Generation-Evaluation-Optimization Workflow

Our unique three-stage pipeline ensures robust, safe, and efficient code:

1. **Generation Stage**: Your natural language request is processed by gpt-4.1 to create initial Python code
2. **Evaluation Stage**: The generated code is analyzed by gpt-4.1-mini for:
   - Syntax correctness
   - API usage validity
   - Code safety
   - Best practices
   - Edge case handling
   - Adherence to documented API functions
3. **Optimization Stage**: If the evaluation score is below threshold (or if critical safety rules are violated), the code is automatically improved based on specific feedback

This iterative workflow (with a default of one optimization iteration) continues until reaching quality thresholds or maximum iteration count, ensuring you get the best possible results. The evaluation process uses specific point deductions for common errors, prioritizing safety and API adherence.

## System Requirements

- Python 3.10 or higher
- OpenAI API key
- Reachy 2 robot (physical or simulated) - optional for code execution

## Setup Instructions

### Installation

1. Clone the repository:
```bash
git clone https://github.com/revelsi/reachy2_code_generation.git
cd reachy2_code_generation
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

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```
Or create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4.1-mini
EVALUATOR_MODEL=gpt-4.1-nano
```
**Note on Changing Models:** To change the default generator and evaluator models, update the `MODEL` and `EVALUATOR_MODEL` values in the `.env` file. The system now automatically loads the correct parameters based on the selected model family (GPT vs O-family). See `.env.example` for model-specific parameters like `MODEL_REASONING_EFFORT` and `MODEL_MAX_COMPLETION_TOKENS`.

4. **Important:** Generate the API documentation needed by the agent:
```bash
make refresh-sdk
```
This step clones the Reachy SDK and processes its documentation, which is essential for the code generation agent to understand the available robot functions.

### Starting the Gradio Interface

Launch the Gradio web interface with:

```bash
python launch_code_gen.py --ui
```

This starts a web server at http://localhost:7860 by default.

### Command Line Options

Fine-tune the application behavior with these options:

```bash
python launch_code_gen.py --ui --generator-model gpt-4.1-mini --evaluator-model gpt-4.1-nano --temperature 0.3 --max-tokens 5000 --port 7861 --share
```

Key options:
- `--generator-model`: Model for code generation (default: gpt-4.1-mini)
- `--evaluator-model`: Model for code evaluation (default: gpt-4.1-nano)
- `--temperature`: Controls randomness (0.0 to 1.0, default: 0.2)
- `--max-tokens`: Maximum tokens to generate (default: 4000)
- `--port`: Web server port (default: 7860)
- `--share`: Create a public share link via Gradio
- `--max-iterations`: Maximum optimization cycles (default: 3)
- `--evaluation-threshold`: Quality threshold for acceptance (default: 75.0)

## Using the Gradio Interface

The Gradio interface provides an intuitive way to generate and execute code for the Reachy 2 robot.

### Main Interface Components

1. **Left Column**: 
   - **Chat Interface**: Natural conversation with the AI assistant
   - **Message History**: View previous interactions and context
   - **Message Input**: Type requests, ask questions, or refine code
   - **Status Indicator**: Clear visual feedback on current operation status

2. **Right Column**:
   - **Code Editor**: View and modify generated Python code with syntax highlighting
   - **Execute Button**: Run the code directly on connected Reachy robots
   - **Execution Results**: View output and error messages from code execution

The interface features a modern, clean design with clear separation between conversation and code areas for improved usability.

### Workflow Example

1. **Start a Conversation**: Type "Can you help me make Reachy wave its right arm?" in the message box
2. **Receive Response**: The AI will generate code and explain its approach conversationally
3. **Ask Follow-up Questions**: Refine your request with natural language like "Can you make it wave three times instead?"
4. **Execute Code**: If a robot is connected, click "Execute Code" to run it directly
5. **Iterate and Improve**: Continue the conversation to refine the code based on results

### Tips for Effective Use

- **Be Specific**: Include details like timing, positions, and sequences
- **Start Simple**: Begin with basic movements before complex interactions
- **Review Evaluations**: Pay attention to warnings and suggestions
- **Iterative Refinement**: Use feedback to improve your requests
- **Check Robot Status**: Confirm robot connectivity before execution

## Advanced Configuration

### Refreshing the SDK Documentation

To update the Reachy 2 SDK documentation used by the system:

```bash
make refresh-sdk
```

To include vision capabilities (from pollen-vision):

```bash
make refresh-sdk-with-vision
```

### Available Make Commands

```bash
make setup         # Set up the development environment
make clean         # Clean generated files and cache
make lint          # Run the linter on the codebase
make test          # Run code generation tests
make run-gradio    # Run the Gradio interface
make refresh-sdk   # Refresh the SDK documentation
make refresh-sdk-with-vision  # Refresh SDK documentation including vision capabilities
```

## Troubleshooting

- **Connection Issues**: Ensure robot IP is correctly configured in `.env` file (REACHY_HOST)
- **Model Errors**: Verify your OpenAI API key has access to requested models
- **Execution Failures**: Check robot power and connectivity status
- **Import Errors**: Ensure all dependencies are installed with `make setup`
- **Performance Issues**: Try reducing model complexity or token limits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version History

- **v1.0.3** (16 April 2025): Support of OpenAI o-family models (o1, o1-mini, o3, o3-mini)
- **v1.0.2** (15 April 2025): New conversational chat interface with back-and-forth interactions and performance optimizations.
- **v1.0.1** (14 April 2025): UI modernization with improved layout, code editor enhancements, and better status indicators.
- **v1.0.0** (8 April 2025): Initial public release with the Generation-Evaluation-Optimization pipeline and Gradio interface.

## License

This project is licensed under the MIT License - see the LICENSE file for details.