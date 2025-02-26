# Quick Start Guide: Reachy 2 Agent Web Interface

This guide will help you quickly get started with the Reachy 2 Agent web interface on MacOS, Windows, or Linux.

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (set in `.env` file or environment variables)
- Virtual environment with dependencies installed
- Git installed on your system

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/reachy_function_calling.git
cd reachy_function_calling
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4-turbo
```

### 3. Set Up Virtual Environment

#### MacOS/Linux
```bash
# Create virtual environment
python3.10 -m venv venv_py310

# Activate virtual environment
source venv_py310/bin/activate

# Install dependencies with fixed versions
pip install -r requirements-fixed.txt
```

#### Windows
```batch
# Create virtual environment
python -m venv venv_py310

# Activate virtual environment
venv_py310\Scripts\activate

# Install dependencies with fixed versions
pip install -r requirements-fixed.txt
```

## Running the Web Interface

### Option 1: Using Make (MacOS/Linux)

```bash
make run-web
```

### Option 2: Using Python Directly (All Platforms)

1. Activate the virtual environment:

   **MacOS/Linux:**
   ```bash
   source venv_py310/bin/activate
   ```

   **Windows:**
   ```batch
   venv_py310\Scripts\activate
   ```

2. Run the web interface:
   ```bash
   python agent/web_interface.py --model gpt-4-turbo
   ```

3. Open your browser and go to:
   ```
   http://127.0.0.1:7860
   ```

## Using the Interface

1. **Chat Interface**
   - Type your commands in the text box at the bottom
   - Click "Send" or press Enter to submit
   - View responses in the chat window
   - Use "Reset Chat" to start a new conversation

2. **Tool Calls Panel**
   - View active tool calls and their results in the right panel
   - Monitor the execution of robot commands

## Example Commands

Try these commands to get started:

- "What tools do you have available?"
- "Can you move the robot's head up?"
- "What's the current position of the right arm?"
- "Take a picture with the camera"

## Advanced Options

The web interface supports several command-line options:

```bash
python agent/web_interface.py [OPTIONS]

Options:
  --model MODEL       LLM model to use (default: gpt-4-turbo)
  --share            Create a public link to share the interface
  --port PORT        Run on a specific port (default: 7860)
  --focus [MODULES]  Focus on specific tool modules (e.g., parts utils)
  --regenerate       Regenerate tool definitions
```

## Platform-Specific Troubleshooting

### MacOS
1. If you get SSL certificate errors:
   ```bash
   pip install --upgrade certifi
   ```
2. If you have multiple Python versions, use `python3.10` explicitly

### Windows
1. If `python` command not found:
   - Add Python to your PATH during installation
   - Or use full path: `C:\Python310\python.exe`
2. If you get permission errors, run Command Prompt as Administrator

### Linux
1. If you get module not found errors:
   ```bash
   sudo apt-get update
   sudo apt-get install python3.10-dev
   ```
2. If you get display errors, ensure X11 forwarding is enabled

### Common Errors

#### Pydantic/FastAPI Error
If you see an error like:
```
pydantic.errors.PydanticSchemaGenerationError: Unable to generate pydantic-core schema for <class 'starlette.requests.Request'>
```

Try these solutions:

1. Install specific versions of dependencies:
   ```bash
   pip install "fastapi<0.100.0" "pydantic<2.0.0"
   ```

2. If the error persists, try cleaning and reinstalling:
   ```bash
   # Deactivate and remove virtual environment
   deactivate
   rm -rf venv_py310  # (on Windows: rmdir /s /q venv_py310)
   
   # Create new environment and install dependencies
   python3.10 -m venv venv_py310
   source venv_py310/bin/activate  # (on Windows: venv_py310\Scripts\activate)
   pip install "fastapi<0.100.0" "pydantic<2.0.0" "gradio==4.13.0"
   pip install -r requirements.txt
   ```

3. If you're still having issues, try running with debug mode:
   ```bash
   python agent/web_interface.py --model gpt-4-turbo --debug
   ```

## Getting Help

If you encounter issues:
1. Check the error messages in the terminal
2. Refer to the full documentation in README.md
3. Open an issue on the GitHub repository

For more detailed information, refer to the full documentation in the project's README.md file. 