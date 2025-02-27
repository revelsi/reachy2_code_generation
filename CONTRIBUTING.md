# Contributing to Reachy Function Calling

Thank you for your interest in contributing to the Reachy Function Calling project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/reachy_function_calling.git`
3. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`
4. Set up your development environment (see below)
5. Make your changes
6. Run tests to ensure your changes don't break existing functionality: `python -m pytest`
7. Commit your changes: `git commit -m "Add your meaningful commit message"`
8. Push to your fork: `git push origin feature/your-feature-name`
9. Create a pull request

## Development Environment Setup

We provide setup scripts that ensure you're working in the correct environment with all necessary dependencies.

### Using the Setup Scripts (Recommended)

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
# Create a virtual environment with Python 3.10+
python3.10 -m venv venv_py310

# Activate the virtual environment
source venv_py310/bin/activate  # On Windows: venv_py310\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify tools
python verify_tools.py
```

## Project Structure

- `agent/`: Core agent implementation
  - `tools/`: Tool implementations for the Reachy robot
  - `utils/`: Utility functions and classes
  - `schemas/`: JSON schemas for tools
  - `docs/`: API documentation
- `tests/`: Test suite
  - `unit/`: Unit tests
  - `integration/`: Integration tests
- `frontend/`: Web interface

## Tool Development

When developing new tools for the Reachy robot:

1. Tools should inherit from `BaseTool` in `agent/tools/base_tool.py`
2. Use the `register_tool` method to register tools
3. Implement the `register_all_tools` class method
4. Follow the standard return format: `{"success": bool, "result": Any, "error": Optional[str]}`
5. Add appropriate error handling with try/except blocks

## Testing

All new features and bugfixes should include tests. We use pytest for testing:

```bash
# Run all tests
python -m pytest

# Run specific tests
python -m pytest tests/unit/tools/test_tools.py

# Run tests with verbose output
python -m pytest -v
```

## Documentation

Please document your code using docstrings. We follow the Google docstring format:

```python
def function_name(param1, param2):
    """Short description of the function.
    
    Longer description explaining the function in detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When and why this exception is raised
    """
    # Function implementation
```

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation if necessary
3. Add your changes to the CHANGELOG.md file
4. Make sure your code follows the project's style guidelines
5. Request a review from a maintainer

## Generating Tools

If you need to regenerate the tools after making changes to the tool mapper:

```bash
python -m agent.utils.integrate_tools
```

This will:
1. Clean existing tool files
2. Load API documentation
3. Map API to tools
4. Generate tool implementations

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License. 