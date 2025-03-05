#!/bin/bash

# Setup script for Reachy Function Calling project
# This script checks Python version, creates a virtual environment, and installs dependencies

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.10"
VENV_NAME="venv_py310"

echo -e "${GREEN}Setting up Reachy Function Calling environment...${NC}"

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
if [ ! -d "$VENV_NAME" ]; then
    $PYTHON_CMD -m venv $VENV_NAME
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment created: ${VENV_NAME}${NC}"
else
    echo -e "${YELLOW}Virtual environment ${VENV_NAME} already exists.${NC}"
fi

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
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "    source ${VENV_NAME}/bin/activate"
echo -e "${YELLOW}To run the CLI:${NC}"
echo -e "    python agent/cli.py"
echo -e "${YELLOW}To run the web interface:${NC}"
echo -e "    python agent/web_interface.py" 