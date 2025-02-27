#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_NAME="venv_py310"
PYTHON_VERSION="3.10"
REQUIRED_PYTHON_MAJOR=3
REQUIRED_PYTHON_MINOR=10

echo -e "${BLUE}=== Reachy Function Calling Development Environment Setup ===${NC}"

# Function to check if we're in the correct virtual environment
check_venv() {
    if [[ "$VIRTUAL_ENV" == *"$VENV_NAME"* ]]; then
        echo -e "${GREEN}✓ Already in the correct virtual environment: $VENV_NAME${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Not in the correct virtual environment.${NC}"
        return 1
    fi
}

# Function to activate the virtual environment
activate_venv() {
    if [ -d "$VENV_NAME" ]; then
        echo -e "${YELLOW}Activating virtual environment: $VENV_NAME${NC}"
        if [ -f "$VENV_NAME/bin/activate" ]; then
            source "$VENV_NAME/bin/activate"
            echo -e "${GREEN}✓ Virtual environment activated${NC}"
            return 0
        else
            echo -e "${RED}✗ Could not find activation script in $VENV_NAME/bin/activate${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Virtual environment directory not found: $VENV_NAME${NC}"
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        create_venv
        return $?
    fi
}

# Function to create the virtual environment
create_venv() {
    # Check Python version
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}✗ Python not found. Please install Python ${PYTHON_VERSION} or higher.${NC}"
        return 1
    fi

    # Check Python version
    PYTHON_VERSION_OUTPUT=$($PYTHON_CMD --version)
    if [[ $PYTHON_VERSION_OUTPUT =~ Python\ ([0-9]+)\.([0-9]+) ]]; then
        PYTHON_MAJOR=${BASH_REMATCH[1]}
        PYTHON_MINOR=${BASH_REMATCH[2]}
        
        if [ "$PYTHON_MAJOR" -lt "$REQUIRED_PYTHON_MAJOR" ] || ([ "$PYTHON_MAJOR" -eq "$REQUIRED_PYTHON_MAJOR" ] && [ "$PYTHON_MINOR" -lt "$REQUIRED_PYTHON_MINOR" ]); then
            echo -e "${RED}✗ Python ${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR}+ is required. Found: $PYTHON_VERSION_OUTPUT${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Could not determine Python version.${NC}"
        return 1
    fi

    echo -e "${YELLOW}Creating virtual environment with $PYTHON_CMD...${NC}"
    $PYTHON_CMD -m venv $VENV_NAME
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to create virtual environment.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Virtual environment created: $VENV_NAME${NC}"
    activate_venv
    return $?
}

# Function to check and install dependencies
check_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    
    # Check if pip is available
    if ! command -v pip &>/dev/null; then
        echo -e "${RED}✗ pip not found in the virtual environment.${NC}"
        return 1
    fi
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}✗ requirements.txt not found.${NC}"
        return 1
    fi
    
    # Check if all dependencies are installed
    pip freeze > .installed_packages.tmp
    MISSING_DEPS=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and empty lines
        [[ "$line" =~ ^#.*$ ]] && continue
        [[ -z "$line" ]] && continue
        
        # Extract package name (before == or >=)
        PKG_NAME=$(echo "$line" | sed -E 's/([^=<>!~]+)[=<>!~].*/\1/')
        
        # Check if package is installed
        if ! grep -q "^$PKG_NAME==" .installed_packages.tmp && ! grep -q "^$PKG_NAME @" .installed_packages.tmp; then
            echo -e "${RED}✗ Missing dependency: $PKG_NAME${NC}"
            MISSING_DEPS=1
        fi
    done < "requirements.txt"
    
    rm .installed_packages.tmp
    
    if [ $MISSING_DEPS -eq 1 ]; then
        echo -e "${YELLOW}Installing missing dependencies...${NC}"
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}✗ Failed to install dependencies.${NC}"
            return 1
        fi
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    else
        echo -e "${GREEN}✓ All dependencies are installed${NC}"
    fi
    
    return 0
}

# Function to verify tools
verify_tools() {
    echo -e "${YELLOW}Verifying tools...${NC}"
    
    # Check if the verification script exists
    if [ ! -f "verify_tools.py" ]; then
        echo -e "${RED}✗ verify_tools.py not found.${NC}"
        return 1
    fi
    
    # Run the verification script
    python verify_tools.py
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Tool verification failed.${NC}"
        echo -e "${YELLOW}Would you like to regenerate the tools? (y/n)${NC}"
        read -r REGENERATE
        
        if [[ "$REGENERATE" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Regenerating tools...${NC}"
            python -m agent.utils.integrate_tools
            
            if [ $? -ne 0 ]; then
                echo -e "${RED}✗ Tool regeneration failed.${NC}"
                return 1
            fi
            
            echo -e "${GREEN}✓ Tools regenerated successfully${NC}"
            python verify_tools.py
            
            if [ $? -ne 0 ]; then
                echo -e "${RED}✗ Tool verification still failing after regeneration.${NC}"
                return 1
            fi
        else
            return 1
        fi
    fi
    
    echo -e "${GREEN}✓ Tools verified successfully${NC}"
    return 0
}

# Function to check environment variables
check_env_vars() {
    echo -e "${YELLOW}Checking environment variables...${NC}"
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠ .env file not found. Creating from .env.example...${NC}"
        
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${GREEN}✓ Created .env file from .env.example${NC}"
            echo -e "${YELLOW}⚠ Please edit .env file to set your OpenAI API key and other settings.${NC}"
        else
            echo -e "${RED}✗ .env.example not found. Creating minimal .env file...${NC}"
            echo "OPENAI_API_KEY=your_api_key_here" > .env
            echo "MODEL=gpt-4-turbo" >> .env
            echo "USE_MOCK=true" >> .env
            echo -e "${GREEN}✓ Created minimal .env file${NC}"
            echo -e "${YELLOW}⚠ Please edit .env file to set your OpenAI API key.${NC}"
        fi
    else
        # Check if OPENAI_API_KEY is set in .env
        if ! grep -q "OPENAI_API_KEY=" .env || grep -q "OPENAI_API_KEY=your_api_key_here" .env; then
            echo -e "${YELLOW}⚠ OPENAI_API_KEY not set in .env file.${NC}"
            echo -e "${YELLOW}⚠ Please edit .env file to set your OpenAI API key.${NC}"
        else
            echo -e "${GREEN}✓ OPENAI_API_KEY is set in .env file${NC}"
        fi
    fi
    
    return 0
}

# Function to display helpful commands
show_help() {
    echo -e "\n${BLUE}=== Helpful Commands ===${NC}"
    echo -e "${GREEN}Run the verification script:${NC}"
    echo -e "  python verify_tools.py"
    echo -e "${GREEN}Regenerate tools:${NC}"
    echo -e "  python -m agent.utils.integrate_tools"
    echo -e "${GREEN}Run tests:${NC}"
    echo -e "  python -m pytest tests/unit/tools/test_tools.py -v"
    echo -e "${GREEN}Run the CLI:${NC}"
    echo -e "  python agent/cli.py"
    echo -e "${GREEN}Run the web interface:${NC}"
    echo -e "  python agent/web_interface.py"
    echo -e "${GREEN}Run the demo:${NC}"
    echo -e "  python agent/demo.py"
    echo -e "\n${YELLOW}For more information, see the README.md, CONTRIBUTING.md, and TODO.md files.${NC}"
}

# Main script
main() {
    # Check if we're in the correct virtual environment
    if ! check_venv; then
        # Try to activate the virtual environment
        if ! activate_venv; then
            echo -e "${RED}✗ Failed to activate or create the virtual environment.${NC}"
            return 1
        fi
    fi
    
    # Check dependencies
    if ! check_dependencies; then
        echo -e "${RED}✗ Dependency check failed.${NC}"
        return 1
    fi
    
    # Check environment variables
    check_env_vars
    
    # Verify tools
    if ! verify_tools; then
        echo -e "${YELLOW}⚠ Tool verification failed. You may need to regenerate the tools.${NC}"
        echo -e "${YELLOW}⚠ Run: python -m agent.utils.integrate_tools${NC}"
    fi
    
    # Show help
    show_help
    
    echo -e "\n${GREEN}✓ Development environment setup complete!${NC}"
    echo -e "${GREEN}✓ You are now ready to work on the Reachy Function Calling project.${NC}"
    return 0
}

# Run the main function
main 