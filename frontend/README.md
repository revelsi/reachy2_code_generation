# Reachy Function Calling Frontend

This is the frontend application for the Reachy Function Calling project. It provides a user interface for interacting with the Reachy robot through natural language commands.

## Features

- Real-time chat interface for sending commands to the robot
- WebSocket connection for live updates from the robot
- Function call visualization and approval system
- Code output display
- Responsive design for desktop and mobile devices

## Technologies Used

- React
- TypeScript
- Tailwind CSS
- Vite
- WebSockets

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Start the development server:

```bash
npm run dev
# or
yarn dev
```

3. Open your browser and navigate to `http://localhost:3000`

## Building for Production

```bash
npm run build
# or
yarn build
```

The build artifacts will be stored in the `dist/` directory.

## Project Structure

- `src/components/` - React components
- `src/hooks/` - Custom React hooks
- `src/types/` - TypeScript type definitions
- `src/lib/` - Utility functions
- `public/` - Static assets

## WebSocket Communication

The frontend communicates with the backend using WebSockets. The following message types are supported:

- `message` - User message to be processed by the AI
- `thinking` - AI thinking process (intermediate steps)
- `function_call` - Function call that requires user approval
- `function_approval` - User approval or rejection of a function call
- `code_output` - Code output from function execution

## Configuration

The WebSocket endpoint and API proxy settings can be configured in the `vite.config.ts` file.

## UI Preview

Here's what the frontend interface looks like:

### Desktop View
The desktop view features a two-panel layout with the chat interface on the left and code output on the right.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Reachy Function Calling                                         GitHub  │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────┐ ┌───────────────────────────────────┐ │
│ │ Chat with Reachy              │ │ Code Output                     ┐ │ │
│ ├───────────────────────────────┤ ├───────────────────────────────────┤ │
│ │                               │ │                                   │ │
│ │ ┌─────────────────────────┐   │ │                                   │ │
│ │ │ You                     │   │ │                                   │ │
│ │ │ Move the right arm up   │   │ │                                   │ │
│ │ └─────────────────────────┘   │ │                                   │ │
│ │                               │ │                                   │ │
│ │ ┌─────────────────────────┐   │ │                                   │ │
│ │ │ Reachy Assistant        │   │ │                                   │ │
│ │ │ I'll move the right arm │   │ │                                   │ │
│ │ │ upward. Let me do that  │   │ │                                   │ │
│ │ │ for you.                │   │ │                                   │ │
│ │ │                         │   │ │                                   │ │
│ │ │ Function Call: move_arm │   │ │                                   │ │
│ │ │ ┌───────┐ ┌───────┐    │   │ │                                   │ │
│ │ │ │Approve│ │Reject │    │   │ │                                   │ │
│ │ │ └───────┘ └───────┘    │   │ │                                   │ │
│ │ │ {"arm": "right",       │   │ │                                   │ │
│ │ │  "direction": "up",    │   │ │                                   │ │
│ │ │  "distance": 0.2}      │   │ │                                   │ │
│ │ │                         │   │ │                                   │ │
│ │ │ Show thinking          │   │ │                                   │ │
│ │ └─────────────────────────┘   │ │                                   │ │
│ │                               │ │                                   │ │
│ ├───────────────────────────────┤ │                                   │ │
│ │ ┌───────────────────────────┐ │ │                                   │ │
│ │ │Ask something about Reachy..│ │ │                                   │ │
│ │ └───────────────────────────┘ │ │                                   │ │
│ └───────────────────────────────┘ └───────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│ © 2023 Reachy Function Calling   Built with React, TailwindCSS, Reachy 2│
└─────────────────────────────────────────────────────────────────────────┘
```

### Mobile View
On mobile devices, the layout switches to a stacked view with the chat panel on top and code panel below.

```
┌───────────────────────────────┐
│ Reachy Function Calling       │
├───────────────────────────────┤
│ ┌───────────────────────────┐ │
│ │ Chat with Reachy          │ │
│ ├───────────────────────────┤ │
│ │                           │ │
│ │ ┌───────────────────────┐ │ │
│ │ │ You                   │ │ │
│ │ │ What's your status?   │ │ │
│ │ └───────────────────────┘ │ │
│ │                           │ │
│ │ ┌───────────────────────┐ │ │
│ │ │ Reachy Assistant      │ │ │
│ │ │ I'll check my status  │ │ │
│ │ │ for you.              │ │ │
│ │ │                       │ │ │
│ │ │ Function Call:        │ │ │
│ │ │ get_robot_status      │ │ │
│ │ │ ┌───────┐ ┌───────┐  │ │ │
│ │ │ │Approve│ │Reject │  │ │ │
│ │ │ └───────┘ └───────┘  │ │ │
│ │ │ {}                    │ │ │
│ │ └───────────────────────┘ │ │
│ │                           │ │
│ ├───────────────────────────┤ │
│ │ ┌─────────────────────┐   │ │
│ │ │Ask something...     │   │ │
│ │ └─────────────────────┘   │ │
│ └───────────────────────────┘ │
│                               │
│ ┌───────────────────────────┐ │
│ │ Code Output               │ │
│ ├───────────────────────────┤ │
│ │                           │ │
│ │ No code to display yet.   │ │
│ │ Ask a question to         │ │
│ │ generate code.            │ │
│ │                           │ │
│ └───────────────────────────┘ │
│                               │
└───────────────────────────────┘
```

### Key UI Components

1. **Chat Messages**: Each message shows the sender (You or Reachy Assistant), content, and timestamp.

2. **Function Calls**: When the AI suggests a function call, it displays:
   - Function name
   - Parameters in JSON format
   - Approve and Reject buttons

3. **Thinking Process**: Users can toggle the visibility of the AI's thinking process.

4. **Code Output**: The right panel (or bottom panel on mobile) displays code output from function execution.

5. **Input Area**: A text input field with a send button for typing messages to the robot. 