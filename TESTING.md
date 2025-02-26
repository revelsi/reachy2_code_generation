# Testing Guide for Reachy Function Calling

This guide provides step-by-step instructions for testing the entire application from a fresh start.

## Prerequisites

- Docker and Docker Compose installed
- Git
- OpenAI API key

## Option 1: Testing with Docker (Recommended)

This is the cleanest approach as it isolates everything in containers.

### 1. Clone the repository (if you haven't already)

```bash
git clone https://github.com/yourusername/reachy_function_calling.git
cd reachy_function_calling
```

### 2. Create a .env file with your OpenAI API key

```bash
cp .env.example .env
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

```bash
docker-compose up --build
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

```bash
# Stop the development containers
docker-compose down

# Build and start the production containers
docker-compose -f docker-compose.prod.yml up --build
```

Access the production application at http://localhost:3000

## Option 2: Testing Without Docker

If you prefer to test without Docker, you can run the backend and frontend separately.

### 1. Set up the backend

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
export OPENAI_API_KEY=your_api_key_here  # On Windows: set OPENAI_API_KEY=your_api_key_here

# Start the backend server
python api/server.py
```

### 2. Set up the frontend

```bash
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

```bash
# Run backend tests
pytest agent/test_*.py

# Run linting
flake8 agent/ agent/tools/scrape_sdk_docs.py
``` 