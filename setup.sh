#!/bin/bash

# Setup script for Reachy Code Generation project
# This script checks Python version, creates a virtual environment, and installs dependencies

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.10"
VENV_NAME="venv_py310"

echo -e "${GREEN}Setting up Reachy Code Generation environment...${NC}"

# Check if venv exists and remove it
if [ -d "$VENV_NAME" ]; then
    echo -e "${YELLOW}Removing existing virtual environment: $VENV_NAME${NC}"
    rm -rf "$VENV_NAME"
fi

# Clean up package installation artifacts
echo -e "${YELLOW}Cleaning package installation artifacts...${NC}"
rm -rf build/ dist/ *.egg-info
find . -type d -name __pycache__ 2>/dev/null | xargs rm -rf 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -type d -name ".pytest_cache" 2>/dev/null | xargs rm -rf 2>/dev/null
find . -name "*.so" -delete 2>/dev/null
find . -name "*.o" -delete 2>/dev/null
find . -name ".coverage" -delete 2>/dev/null
echo -e "${GREEN}Cleanup complete.${NC}"

# Check for Python 3.10 specifically
echo -e "${YELLOW}Checking for Python ${PYTHON_VERSION}...${NC}"
if command -v python3.10 &>/dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python${PYTHON_VERSION} &>/dev/null; then
    PYTHON_CMD="python${PYTHON_VERSION}"
elif command -v /usr/local/bin/python3.10 &>/dev/null; then
    PYTHON_CMD="/usr/local/bin/python3.10"
else
    echo -e "${RED}Error: Python ${PYTHON_VERSION} not found.${NC}"
    echo -e "${YELLOW}Please install Python ${PYTHON_VERSION} and make sure it's in your PATH.${NC}"
    echo -e "${YELLOW}On macOS, you can install it with: brew install python@${PYTHON_VERSION}${NC}"
    echo -e "${YELLOW}On Ubuntu, you can install it with: sudo apt install python${PYTHON_VERSION}${NC}"
    exit 1
fi

# Verify Python version
echo -e "${YELLOW}Verifying Python version...${NC}"
$PYTHON_CMD --version
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to run Python ${PYTHON_VERSION}.${NC}"
    exit 1
fi

echo -e "${GREEN}Python version check passed: $($PYTHON_CMD --version)${NC}"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment with Python ${PYTHON_VERSION}...${NC}"
$PYTHON_CMD -m venv $VENV_NAME
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to create virtual environment.${NC}"
    exit 1
fi
echo -e "${GREEN}Virtual environment created: ${VENV_NAME}${NC}"

# Activate virtual environment and install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
if [ -f "$VENV_NAME/bin/activate" ]; then
    source $VENV_NAME/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install dependencies.${NC}"
        exit 1
    fi
    
    # Install Reachy2 SDK with editable mode
    echo -e "${YELLOW}Installing Reachy2 SDK in editable mode...${NC}"
    pip install reachy2-sdk -e .
    if [ $? -ne 0 ]; then
        echo -e "${RED}Warning: Failed to install Reachy2 SDK in editable mode. Some functionality may be limited.${NC}"
        echo -e "${YELLOW}You may need to manually install it later with: pip install reachy2-sdk -e .${NC}"
    else
        echo -e "${GREEN}Reachy2 SDK installed successfully.${NC}"
    fi
    
    echo -e "${GREEN}Dependencies installed successfully.${NC}"
else
    echo -e "${RED}Error: Virtual environment activation script not found.${NC}"
    exit 1
fi

# Setup complete
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}Activating the virtual environment...${NC}"
source ${VENV_NAME}/bin/activate
echo -e "${GREEN}Virtual environment ${VENV_NAME} is now active.${NC}"
echo -e "${YELLOW}To run the Gradio interface:${NC}"
echo -e "    python launch_code_gen.py" 