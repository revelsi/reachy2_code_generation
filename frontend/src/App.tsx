import React, { useEffect, useRef, useState } from "react";
import { Message } from "@/types/chat";
import { Layout } from "@/components/Layout";
import { ChatPanel } from "@/components/ChatPanel";
import { CodePanel } from "@/components/CodePanel";
import { useIsMobile } from "@/hooks/use-mobile";
import { Toaster } from "@/components/ui/toaster";
import { useToast } from "@/hooks/use-toast";
import { generateId } from "@/lib/utils";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [codeOutput, setCodeOutput] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);
  const isMobile = useIsMobile();
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const { toast } = useToast();
  const maxReconnectAttempts = 5;
  const reconnectDelay = 3000;

  // Initialize WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      // Use relative URL for WebSocket connection in production
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = process.env.NODE_ENV === 'production' ? window.location.host : 'localhost:8000';
      const wsUrl = `${protocol}//${host}/ws`;
      
      console.log(`Connecting to WebSocket at ${wsUrl}`);
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        console.log("WebSocket connected");
        setIsConnected(true);
        setSocket(ws);
        setReconnectAttempts(0);
        
        // Show success toast if reconnecting after failure
        if (reconnectAttempts > 0) {
          toast({
            title: "Connection Restored",
            description: "Successfully reconnected to the server.",
            variant: "default",
          });
        }
      };
      
      ws.onclose = () => {
        console.log("WebSocket disconnected");
        setIsConnected(false);
        setSocket(null);
        
        // Attempt to reconnect if under max attempts
        if (reconnectAttempts < maxReconnectAttempts) {
          const nextAttempt = reconnectAttempts + 1;
          setReconnectAttempts(nextAttempt);
          
          toast({
            title: "Connection Lost",
            description: `Attempting to reconnect (${nextAttempt}/${maxReconnectAttempts})...`,
            variant: "destructive",
          });
          
          setTimeout(connectWebSocket, reconnectDelay);
        } else {
          toast({
            title: "Connection Failed",
            description: "Could not connect to the server. Please check if the server is running and refresh the page.",
            variant: "destructive",
          });
        }
      };
      
      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        toast({
          title: "Connection Error",
          description: "An error occurred with the WebSocket connection.",
          variant: "destructive",
        });
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === "thinking") {
            // Update the last message with thinking content
            setMessages(prevMessages => {
              const lastMessage = prevMessages[prevMessages.length - 1];
              if (lastMessage && lastMessage.type === "system") {
                return [
                  ...prevMessages.slice(0, -1),
                  { ...lastMessage, thinking: data.content }
                ];
              }
              return prevMessages;
            });
          } 
          else if (data.type === "message") {
            // Add a new message from the system
            const newMessage: Message = {
              id: generateId(),
              content: data.content,
              type: "system",
              timestamp: new Date(),
              thinking: "",
              codeOutput: ""
            };
            
            setMessages(prevMessages => [...prevMessages, newMessage]);
            setIsProcessing(false);
          } 
          else if (data.type === "function_call") {
            // Update the last message with function call details
            setMessages(prevMessages => {
              const lastMessage = prevMessages[prevMessages.length - 1];
              if (lastMessage && lastMessage.type === "system") {
                return [
                  ...prevMessages.slice(0, -1),
                  { 
                    ...lastMessage, 
                    functionCall: {
                      name: data.name,
                      parameters: data.parameters,
                      id: data.id
                    }
                  }
                ];
              }
              return prevMessages;
            });
          } 
          else if (data.type === "code_output") {
            setCodeOutput(data.content);
            
            // Update the last message with code output
            setMessages(prevMessages => {
              const lastMessage = prevMessages[prevMessages.length - 1];
              if (lastMessage && lastMessage.type === "system") {
                return [
                  ...prevMessages.slice(0, -1),
                  { ...lastMessage, codeOutput: data.content }
                ];
              }
              return prevMessages;
            });
          }
          else if (data.type === "error") {
            toast({
              title: "Error",
              description: data.message || "An error occurred",
              variant: "destructive",
            });
            setIsProcessing(false);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
          toast({
            title: "Message Error",
            description: "Failed to parse message from server",
            variant: "destructive",
          });
        }
      };
    };
    
    connectWebSocket();
    
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);
  
  // Handle sending a message
  const handleSendMessage = (content: string) => {
    if (!content.trim()) return;
    
    // Add user message
    const userMessage: Message = {
      id: generateId(),
      content,
      type: "user",
      timestamp: new Date(),
      thinking: "",
      codeOutput: ""
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsProcessing(true);
    
    // Add initial system message
    const systemMessage: Message = {
      id: generateId(),
      content: "",
      type: "system",
      timestamp: new Date(),
      thinking: "Thinking...",
      codeOutput: ""
    };
    
    setMessages(prevMessages => [...prevMessages, systemMessage]);
    
    // Send message to server
    if (socket && isConnected) {
      socket.send(JSON.stringify({
        type: "message",
        content
      }));
    } else {
      console.error("WebSocket not connected");
      toast({
        title: "Connection Error",
        description: "Not connected to the server. Please wait for reconnection or refresh the page.",
        variant: "destructive",
      });
      setIsProcessing(false);
    }
  };
  
  // Handle function call approval
  const handleApproveFunction = (functionId: string) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify({
        type: "function_approval",
        id: functionId,
        approved: true
      }));
      
      toast({
        title: "Function Approved",
        description: "The function call has been approved and will be executed.",
        variant: "default",
      });
    } else {
      toast({
        title: "Connection Error",
        description: "Not connected to the server. Cannot approve function.",
        variant: "destructive",
      });
    }
  };
  
  // Handle function call rejection
  const handleRejectFunction = (functionId: string) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify({
        type: "function_approval",
        id: functionId,
        approved: false
      }));
      
      toast({
        title: "Function Rejected",
        description: "The function call has been rejected.",
        variant: "default",
      });
    } else {
      toast({
        title: "Connection Error",
        description: "Not connected to the server. Cannot reject function.",
        variant: "destructive",
      });
    }
  };
  
  return (
    <Layout>
      <div className="flex flex-col lg:flex-row w-full h-full gap-4 p-4">
        {/* Chat Panel */}
        <div className={isMobile ? "w-full h-1/2" : "w-2/3 h-full"}>
          <ChatPanel 
            messages={messages}
            onSendMessage={handleSendMessage}
            isProcessing={isProcessing}
            chatEndRef={chatEndRef}
            onApproveFunction={handleApproveFunction}
            onRejectFunction={handleRejectFunction}
          />
        </div>
        
        {/* Code Panel */}
        <div className={isMobile ? "w-full h-1/2" : "w-1/3 h-full"}>
          <CodePanel code={codeOutput} />
        </div>
      </div>
      
      {/* Toast notifications */}
      <Toaster />
    </Layout>
  );
} 