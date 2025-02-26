# Reachy Function Calling System Architecture

## System Overview

The Reachy Function Calling system is a comprehensive application that enables users to interact with a Reachy 2 robot through natural language. The system consists of three main components:

1. **Frontend**: A React-based web application that provides a user interface for interacting with the robot
2. **Backend API**: A Flask-based REST API that handles HTTP requests and manages the agent
3. **LangGraph Agent**: The core intelligence that processes natural language, makes decisions, and controls the robot

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        CLIENT BROWSER                                           │
│                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                    REACT FRONTEND                                        │   │
│  │                                                                                          │   │
│  │  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                  │   │
│  │  │  Chat Panel   │         │  Code Panel   │         │ Status Display │                  │   │
│  │  └───────────────┘         └───────────────┘         └───────────────┘                  │   │
│  │           │                        │                         │                           │   │
│  │           └────────────────────────┼─────────────────────────┘                           │   │
│  │                                    │                                                      │   │
│  │                            ┌───────────────┐                                              │   │
│  │                            │  API Service  │                                              │   │
│  │                            └───────────────┘                                              │   │
│  │                                    │                                                      │   │
│  │                                    │                                                      │   │
│  │                            ┌───────────────┐                                              │   │
│  │                            │  WebSocket    │                                              │   │
│  │                            │  Connection   │                                              │   │
│  │                            └───────────────┘                                              │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                │                                           │
                │ HTTP Requests                             │ WebSocket Connection
                │ (REST API)                                │ (Real-time updates)
                ▼                                           ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         BACKEND SERVER                                         │
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                     FLASK API                                            │  │
│  │                                                                                          │  │
│  │  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                  │  │
│  │  │ /api/chat     │         │ /api/reset    │         │ /api/tools    │                  │  │
│  │  │ Endpoint      │         │ Endpoint      │         │ Endpoint      │                  │  │
│  │  └───────────────┘         └───────────────┘         └───────────────┘                  │  │
│  │           │                        │                         │                           │  │
│  │           └────────────────────────┼─────────────────────────┘                           │  │
│  │                                    │                                                      │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                                        │
│                                       │                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                 WEBSOCKET SERVER                                         │  │
│  │                                                                                          │  │
│  │  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                  │  │
│  │  │ Client        │         │ Message       │         │ Notification  │                  │  │
│  │  │ Management    │         │ Handling      │         │ Methods       │                  │  │
│  │  └───────────────┘         └───────────────┘         └───────────────┘                  │  │
│  │                                                                                          │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                                        │
│                                       │                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                               LANGGRAPH AGENT                                            │  │
│  │                                                                                          │  │
│  │  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                  │  │
│  │  │ State         │         │ Graph         │         │ Tool          │                  │  │
│  │  │ Management    │         │ Execution     │         │ Execution     │                  │  │
│  │  └───────────────┘         └───────────────┘         └───────────────┘                  │  │
│  │           │                        │                         │                           │  │
│  │           └────────────────────────┼─────────────────────────┘                           │  │
│  │                                    │                                                      │  │
│  │                            ┌───────────────┐                                              │  │
│  │                            │  Tool Mapper  │                                              │  │
│  │                            └───────────────┘                                              │  │
│  │                                    │                                                      │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                                        │
│                                       │                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                  ROBOT TOOLS                                             │  │
│  │                                                                                          │  │
│  │  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                  │  │
│  │  │ Arm Tools     │         │ Head Tools    │         │ Utility Tools │                  │  │
│  │  └───────────────┘         └───────────────┘         └───────────────┘                  │  │
│  │                                                                                          │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │ OpenAI API
                                          ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      OPENAI API                                               │
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                  GPT-4 TURBO                                             │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (React Application)

The frontend is a React application that provides a user interface for interacting with the Reachy robot. It consists of:

- **Chat Panel**: Allows users to send messages to the robot and view responses
- **Code Panel**: Displays code output from tool executions
- **Status Display**: Shows the current status of the robot
- **API Service**: Handles HTTP requests to the backend API
- **WebSocket Connection**: Maintains a real-time connection for updates

Key files:
- `frontend/src/App.tsx`: Main application component
- `frontend/src/services/api.ts`: API service for HTTP requests
- `frontend/src/components/ChatPanel.tsx`: Chat interface
- `frontend/src/components/CodePanel.tsx`: Code output display

### 2. Backend API (Flask Application)

The backend API is a Flask application that handles HTTP requests from the frontend and manages the LangGraph agent. It consists of:

- **API Endpoints**: 
  - `/api/chat`: Processes chat messages
  - `/api/reset`: Resets the conversation
  - `/api/tools`: Returns available tools
  - `/api/status`: Returns robot status
  - `/api/config`: Updates agent configuration

- **WebSocket Server**: Provides real-time updates to the frontend
  - Client management (connect/disconnect)
  - Message handling
  - Notification methods for different types of updates

Key files:
- `api/app.py`: Flask application with API endpoints
- `api/websocket.py`: WebSocket server implementation

### 3. LangGraph Agent

The LangGraph agent is the core intelligence of the system. It processes natural language, makes decisions, and controls the robot. It consists of:

- **State Management**: Manages the conversation state
- **Graph Execution**: Executes the LangGraph workflow
- **Tool Execution**: Executes robot tools
- **Tool Mapper**: Maps tool definitions to implementations

Key files:
- `agent/langgraph_agent.py`: LangGraph agent implementation
- `agent/tool_mapper.py`: Tool mapping functionality
- `agent/tools/`: Directory containing tool implementations

### 4. Robot Tools

The robot tools are Python functions that control the Reachy robot. They are organized into categories:

- **Arm Tools**: Control the robot's arms
- **Head Tools**: Control the robot's head
- **Utility Tools**: Provide utility functions

Key files:
- `agent/tools/arm_tools.py`: Arm control functions
- `agent/tools/head_tools.py`: Head control functions
- `agent/tools/utility_tools.py`: Utility functions

## Data Flow

1. **User Input**:
   - User sends a message through the Chat Panel
   - Frontend sends an HTTP request to `/api/chat`
   - Backend processes the request and passes it to the LangGraph agent

2. **Agent Processing**:
   - LangGraph agent creates an initial state with the user message
   - Agent sends "thinking" notifications via WebSocket
   - Agent executes the graph workflow:
     - Parse user input
     - Call LLM (GPT-4 Turbo) to decide what to do
     - Execute tools if needed
     - Generate a final response

3. **Real-time Updates**:
   - During processing, the agent sends notifications via WebSocket:
     - Thinking updates
     - Function call notifications
     - Error notifications
     - Completion notifications
   - Frontend receives these notifications and updates the UI accordingly

4. **Response Delivery**:
   - Agent generates a final response
   - Response is sent back to the frontend via WebSocket
   - Frontend displays the response in the Chat Panel

## Deployment Architecture

The system is deployed using Docker Compose with two main services:

1. **API Service**:
   - Runs the Flask API and WebSocket server
   - Exposes ports 5000 (HTTP) and 8765 (WebSocket)
   - Mounts the application code and data volumes

2. **Frontend Service**:
   - Runs the React application
   - Exposes port 3000
   - Communicates with the API service

## Key Interactions

1. **HTTP Communication**:
   - Frontend → Backend: REST API calls for chat, reset, tools, status
   - Backend → OpenAI: API calls for language model inference

2. **WebSocket Communication**:
   - Backend → Frontend: Real-time updates (thinking, function calls, errors, completion)
   - Frontend → Backend: Direct message processing (optional)

3. **Agent → Tools**:
   - Agent calls tool functions based on LLM decisions
   - Tools execute robot actions or utility functions
   - Tool results are returned to the agent for further processing

## Error Handling

1. **Frontend**:
   - WebSocket reconnection logic with exponential backoff
   - Error toasts for connection issues
   - Error display in the chat interface

2. **Backend**:
   - Exception handling in API endpoints
   - Error notifications via WebSocket
   - Logging of errors for debugging

3. **Agent**:
   - Error handling in tool execution
   - Error state management in the graph workflow
   - Error reporting back to the frontend 