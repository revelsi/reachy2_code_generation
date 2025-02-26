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

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python not found. Please install Python ${PYTHON_VERSION} or higher.${NC}"
    exit 1
fi

# Check Python version
$PYTHON_CMD -c "import sys; v=sys.version_info; exit(0 if v.major==3 and v.minor>=10 else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Python ${PYTHON_VERSION}+ is required. Current version: $($PYTHON_CMD --version)${NC}"
    echo -e "${YELLOW}Please install Python ${PYTHON_VERSION} or higher and try again.${NC}"
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