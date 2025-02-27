#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up a fresh virtual environment for Reachy Function Calling...${NC}"

# Check Python version
python_version=$(python3 --version)
echo -e "${GREEN}Using $python_version${NC}"

# Determine the Python command to use
PYTHON_CMD="python3"

# Check if Python version is at least 3.10
if [[ $python_version != *"3.10"* && $python_version != *"3.11"* && $python_version != *"3.12"* ]]; then
    echo -e "${RED}Warning: This project requires Python 3.10 or newer.${NC}"
    echo -e "${YELLOW}Checking if python3.10 is available...${NC}"
    
    if command -v python3.10 &> /dev/null; then
        PYTHON_CMD="python3.10"
    else
        echo -e "${RED}Python 3.10+ not found. Please install Python 3.10 or newer.${NC}"
        exit 1
    fi
fi

# Remove existing virtual environment if it exists
if [ -d "venv_fresh" ]; then
    echo -e "${YELLOW}Removing existing virtual environment...${NC}"
    rm -rf venv_fresh
fi

# Create a new virtual environment
echo -e "${YELLOW}Creating a new virtual environment...${NC}"
$PYTHON_CMD -m venv venv_fresh

# Activate the virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv_fresh/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Verify installations
echo -e "${YELLOW}Verifying installations...${NC}"
pip list | grep -E "langchain|langgraph|openai|pydantic|gradio"

# Create a test script to verify dependencies
cat > test_dependencies.py << 'EOF'
#!/usr/bin/env python
"""
Test script to verify that all dependencies are working correctly together.
"""

import os
import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report success/failure."""
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"✅ Successfully imported {module_name}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        print(f"   Try reinstalling with: pip install {package_name}")
        return False

def main():
    """Main function to test dependencies."""
    print(f"Python version: {sys.version}")
    print("Testing imports...\n")
    
    # Core dependencies
    imports = [
        ("openai", "openai"),
        ("dotenv", "python-dotenv"),
        ("flask", "flask"),
        ("flask_cors", "flask-cors"),
        ("websockets", "websockets"),
        ("psutil", "psutil"),
        
        # LangChain ecosystem
        ("langchain", "langchain"),
        ("langgraph", "langgraph"),
        ("langchain_openai", "langchain-openai"),
        ("pydantic", "pydantic"),
        
        # Optional dependencies
        ("gradio", "gradio"),
        
        # Visualization and data processing
        ("matplotlib", "matplotlib"),
        ("networkx", "networkx"),
        ("numpy", "numpy"),
        ("pyquaternion", "pyquaternion"),
    ]
    
    # Try to import each module
    failures = 0
    for module_name, package_name in imports:
        if not check_import(module_name, package_name):
            failures += 1
    
    # Try to import and use LangChain components
    try:
        from langchain.schema import Document
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
        from langgraph.graph import StateGraph
        
        print("\n✅ Successfully imported and initialized LangChain components")
    except Exception as e:
        print(f"\n❌ Failed to initialize LangChain components: {e}")
        failures += 1
    
    # Summary
    print("\nTest Summary:")
    if failures == 0:
        print("✅ All dependencies are working correctly!")
    else:
        print(f"❌ {failures} dependencies failed to import correctly.")
    
    return failures

if __name__ == "__main__":
    sys.exit(main())
EOF

# Run the test script
echo -e "${YELLOW}Running dependency test...${NC}"
python test_dependencies.py

# Check if the test was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Setup complete! All dependencies are working correctly.${NC}"
    echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
    echo -e "${GREEN}source venv_fresh/bin/activate${NC}"
else
    echo -e "${RED}Setup completed with errors. Please check the output above.${NC}"
    exit 1
fi 