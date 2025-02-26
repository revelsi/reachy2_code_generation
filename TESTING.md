# Testing Guide for Reachy Function Calling

This guide provides step-by-step instructions for testing the entire application from a fresh start.

## Prerequisites

- Docker and Docker Compose installed
- Git
- OpenAI API key

## Option 1: Testing with Docker (Recommended)

This is the cleanest approach as it isolates everything in containers.

### 1. Clone the repository (if you haven't already)

```zsh
git clone https://github.com/yourusername/reachy_function_calling.git
cd reachy_function_calling
```

### 2. Create a .env file with your OpenAI API key

```zsh
cp .env.test .env
```

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4-turbo
USE_MOCK=true
USE_VIRTUAL=true
DEBUG=true
```

### 3. Build and start the development containers

```zsh
docker compose up --build
```

This will:
- Build the backend container
- Start the backend server
- Start the frontend development server
- Mount your local code into the containers for real-time development

### 4. Access the application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api

### 5. Test the application

1. Open the frontend in your browser
2. Try sending a message like "What can you do?"
3. Try a command like "Wave your right arm"
4. Approve the function call when prompted
5. Verify that the response and code output are displayed correctly

### 6. Test the production build

```zsh
# Stop the development containers
docker compose down

# Build and start the production containers
docker compose -f docker-compose.prod.yml up --build
```

Access the production application at http://localhost:3000

## Option 1A: Step-by-Step Guide for Docker Desktop

If you're using Docker Desktop, follow these detailed steps:

### 1. Ensure Docker Desktop is installed and running

- Download Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) if you haven't already
- Install and launch Docker Desktop
- Verify Docker Desktop is running by checking for the Docker icon in your system tray/menu bar

### 2. Clone the repository and set up environment

1. Open a terminal (Terminal on macOS with zsh, or Command Prompt/PowerShell on Windows)
2. Clone the repository:
   ```zsh
   git clone https://github.com/yourusername/reachy_function_calling.git
   cd reachy_function_calling
   ```

3. Create your `.env` file from the test template:
   ```zsh
   cp .env.test .env
   ```

4. Edit the `.env` file with your favorite text editor and replace `your_api_key_here` with your actual OpenAI API key

### 3. Run the verification script

```zsh
./verify_docker.sh
```

This script will:
- Verify Docker and Docker Compose are installed
- Check if your `.env` file exists and has an API key
- Create necessary directories if they don't exist
- Provide instructions for the next steps

### 4. Build and run the application with Docker Desktop

1. Open Docker Desktop
2. Click on the "Containers" tab in the left sidebar
3. Click the "Run" button in the top right
4. In the "Run a new container" dialog:
   - Leave the "Image" field blank (we'll use docker-compose)
   - Click "Cancel" to exit this dialog

5. Return to your terminal and run:
   ```zsh
   docker compose up --build
   ```

6. In Docker Desktop, you should now see:
   - A new container group for your project
   - Two containers running (backend and frontend)
   - Green status indicators showing they're running

### 5. Monitor container logs in Docker Desktop

1. In Docker Desktop, click on your container group
2. You'll see both containers listed
3. Click on each container to view its logs
4. Look for:
   - Backend: "Application startup complete" message
   - Frontend: "Local: http://localhost:3000" message

### 6. Access and test the application

1. Open your web browser and navigate to:
   - Frontend: http://localhost:3000

2. Test basic functionality:
   - Send a message: "What can you do?"
   - Try a command: "Wave your right arm"
   - Approve the function call when prompted
   - Verify the response and code output

### 7. Stop the containers when finished

1. In Docker Desktop:
   - Click on your container group
   - Click the "Stop" button (square icon)

2. Or in your terminal:
   ```zsh
   docker compose down
   ```

### 8. Test the production build (optional)

1. In your terminal:
   ```zsh
   docker compose -f docker-compose.prod.yml up --build
   ```

2. In Docker Desktop, you'll see new production containers running
3. Access the production application at http://localhost:3000
4. Test functionality as before
5. Stop the containers when finished

## Option 2: Testing Without Docker

If you prefer to test without Docker, you can run the backend and frontend separately.

### 1. Set up the backend

```zsh
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Note: On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
export OPENAI_API_KEY=your_api_key_here  # Note: On Windows use: set OPENAI_API_KEY=your_api_key_here

# Start the backend server
python api/server.py
```

### 2. Set up the frontend

```zsh
# In a separate terminal
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm run dev
```

### 3. Access the application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api

## Testing Specific Components

### Testing the WebSocket Connection

1. Open the browser console (F12)
2. Look for WebSocket connection messages
3. Send a message and verify that the WebSocket receives a response

### Testing Function Calls

1. Send a message like "Move your right arm to position [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]"
2. Verify that a function call is displayed with the correct parameters
3. Approve the function call
4. Verify that the function executes and returns a result

### Testing Error Handling

1. Disconnect the backend (stop the server)
2. Try sending a message from the frontend
3. Verify that an error message is displayed
4. Restart the backend and verify that the connection is restored

## Troubleshooting

### Docker Issues

- If you encounter permission issues, try running Docker commands with `sudo`
- For volume mounting issues, ensure your Docker has permission to access the local directories
- If containers can't communicate, check that they're on the same Docker network

### Backend Issues

- Check that your OpenAI API key is correctly set
- Verify that the required ports (8000) are not in use
- Check the logs for any error messages

### Frontend Issues

- Make sure Node.js v18+ is installed
- Check for any build errors in the terminal
- Verify that the WebSocket URL is correctly configured

## Automated Tests

You can also run the automated tests:

```zsh
# Run backend tests
pytest agent/test_*.py

# Run linting
flake8 agent/ agent/tools/scrape_sdk_docs.py
```

## Shell Compatibility Notes

- This guide uses zsh syntax, which is the default shell on macOS since Catalina
- If you're using bash, the commands should work the same way
- For Windows users, use PowerShell or Command Prompt with the noted Windows-specific commands
- The verification and test scripts (`verify_docker.sh` and `test_local.sh`) are compatible with zsh, bash, and sh 