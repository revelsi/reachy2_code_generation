#!/bin/bash
# Script to verify Docker setup for Reachy Function Calling

echo "Verifying Docker setup for Reachy Function Calling..."
echo "======================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
else
    echo "✅ Docker is installed."
fi

# Check if Docker Compose is installed (either standalone or as docker compose)
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose (standalone) is installed."
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    echo "✅ Docker Compose (plugin) is installed."
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
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
echo "Docker setup verification complete."
echo "To start the application in development mode, run:"
if [ "$COMPOSE_CMD" = "docker-compose" ]; then
    echo "docker-compose up --build"
    echo ""
    echo "To start the application in production mode, run:"
    echo "docker-compose -f docker-compose.prod.yml up --build"
else
    echo "docker compose up --build"
    echo ""
    echo "To start the application in production mode, run:"
    echo "docker compose -f docker-compose.prod.yml up --build"
fi
echo "" 