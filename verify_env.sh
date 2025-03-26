#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Configuration
VENV_NAME="venv_py310"
REQUIRED_PYTHON_VERSION="3.10"

echo -e "${YELLOW}Verifying Python environment...${NC}"

# Check if virtual environment exists
if [ ! -d "$VENV_NAME" ]; then
    echo -e "${RED}Error: Virtual environment $VENV_NAME not found.${NC}"
    echo -e "${YELLOW}Please run setup.sh or 'make setup' first.${NC}"
    exit 1
fi

# Activate virtual environment
source $VENV_NAME/bin/activate

# Check Python version
echo -e "${YELLOW}Python version in virtual environment:${NC}"
python --version

# Get Python version details
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

# Compare versions
if [[ "$PYTHON_VERSION" == "$REQUIRED_PYTHON_VERSION"* ]]; then
    echo -e "${GREEN}✓ Python version $PYTHON_VERSION meets the requirement ($REQUIRED_PYTHON_VERSION).${NC}"
else
    echo -e "${RED}✗ Python version $PYTHON_VERSION does not meet the requirement ($REQUIRED_PYTHON_VERSION).${NC}"
    echo -e "${YELLOW}Please recreate the virtual environment with Python $REQUIRED_PYTHON_VERSION:${NC}"
    echo -e "    rm -rf $VENV_NAME"
    echo -e "    ./setup.sh"
    exit 1
fi

# Check key packages
echo -e "${YELLOW}Checking key packages:${NC}"

# Check OpenAI
OPENAI_VERSION=$(pip show openai 2>/dev/null | grep Version | awk '{print $2}')
if [ -n "$OPENAI_VERSION" ]; then
    echo -e "${GREEN}✓ openai: $OPENAI_VERSION${NC}"
else
    echo -e "${RED}✗ openai not installed${NC}"
fi

# Check reachy2-sdk
REACHY_VERSION=$(pip show reachy2-sdk 2>/dev/null | grep Version | awk '{print $2}')
if [ -n "$REACHY_VERSION" ]; then
    echo -e "${GREEN}✓ reachy2-sdk: $REACHY_VERSION${NC}"
else
    echo -e "${RED}✗ reachy2-sdk not installed${NC}"
fi

# Check gradio
GRADIO_VERSION=$(pip show gradio 2>/dev/null | grep Version | awk '{print $2}')
if [ -n "$GRADIO_VERSION" ]; then
    echo -e "${GREEN}✓ gradio: $GRADIO_VERSION${NC}"
else
    echo -e "${RED}✗ gradio not installed${NC}"
fi

echo -e "${GREEN}Environment verification complete.${NC}" 