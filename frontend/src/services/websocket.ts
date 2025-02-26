import { RobotStatus } from "@/types/robot";

type MessageHandler = (data: any) => void;
type StatusHandler = (status: RobotStatus) => void;
type ActionHandler = (action: any) => void;
type ErrorHandler = (error: Event) => void;

class WebSocketService {
  private socket: WebSocket | null = null;
  private reconnectTimer: number | null = null;
  private messageHandlers: MessageHandler[] = [];
  private statusHandlers: StatusHandler[] = [];
  private actionHandlers: ActionHandler[] = [];
  private errorHandlers: ErrorHandler[] = [];
  private connected = false;

  constructor() {
    this.connect();
  }

  private connect() {
    // Use relative URL for WebSocket connection
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    try {
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.connected = true;
        if (this.reconnectTimer) {
          clearTimeout(this.reconnectTimer);
          this.reconnectTimer = null;
        }
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          // Handle different message types
          switch (data.type) {
            case 'state':
              this.statusHandlers.forEach(handler => handler(data.data));
              break;
            case 'action':
              this.actionHandlers.forEach(handler => handler(data.data));
              break;
            default:
              this.messageHandlers.forEach(handler => handler(data));
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.errorHandlers.forEach(handler => handler(error));
      };

      this.socket.onclose = () => {
        console.log('WebSocket disconnected, attempting to reconnect...');
        this.connected = false;
        
        // Attempt to reconnect after 3 seconds
        this.reconnectTimer = window.setTimeout(() => {
          this.connect();
        }, 3000);
      };
    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
      
      // Attempt to reconnect after 3 seconds
      this.reconnectTimer = window.setTimeout(() => {
        this.connect();
      }, 3000);
    }
  }

  public onMessage(handler: MessageHandler) {
    this.messageHandlers.push(handler);
    return () => {
      this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
    };
  }

  public onStatus(handler: StatusHandler) {
    this.statusHandlers.push(handler);
    return () => {
      this.statusHandlers = this.statusHandlers.filter(h => h !== handler);
    };
  }

  public onAction(handler: ActionHandler) {
    this.actionHandlers.push(handler);
    return () => {
      this.actionHandlers = this.actionHandlers.filter(h => h !== handler);
    };
  }

  public onError(handler: ErrorHandler) {
    this.errorHandlers.push(handler);
    return () => {
      this.errorHandlers = this.errorHandlers.filter(h => h !== handler);
    };
  }

  public isConnected() {
    return this.connected;
  }

  public disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }
}

// Create a singleton instance
const websocketService = new WebSocketService();

export default websocketService; 