#!/bin/bash
# Script to test the Reachy Function Calling application locally (without Docker)

echo "Testing Reachy Function Calling locally..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
else
    echo "✅ Python 3 is installed."
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
else
    echo "✅ Node.js is installed."
    
    # Check Node.js version
    NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo "⚠️ Node.js version is less than 18. Some features may not work correctly."
    else
        echo "✅ Node.js version is 18 or higher."
    fi
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️ .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file from .env.example. Please edit it to add your OpenAI API key."
    else
        echo "❌ .env.example file not found. Please create a .env file manually."
        exit 1
    fi
else
    echo "✅ .env file exists."
fi

# Check if OpenAI API key is set in .env
if grep -q "OPENAI_API_KEY=your_api_key_here" .env || grep -q "OPENAI_API_KEY=$" .env; then
    echo "⚠️ OpenAI API key not set in .env file. Please edit the .env file to add your API key."
else
    echo "✅ OpenAI API key is set in .env file."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️ Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Created virtual environment."
else
    echo "✅ Virtual environment exists."
fi

# Check if required directories exist
for dir in "data/raw_docs" "data/external_docs"; do
    if [ ! -d "$dir" ]; then
        echo "⚠️ Directory $dir not found. Creating..."
        mkdir -p "$dir"
        touch "$dir/.gitkeep"
        echo "✅ Created directory $dir."
    else
        echo "✅ Directory $dir exists."
    fi
done

echo ""
echo "Local setup verification complete."
echo ""
echo "To start the backend:"
echo "source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "pip install -r requirements.txt"
echo "python api/server.py"
echo ""
echo "To start the frontend (in a separate terminal):"
echo "cd frontend"
echo "npm install"
echo "npm run dev"
echo ""
echo "Then access the application at:"
echo "http://localhost:3000"
echo "" 