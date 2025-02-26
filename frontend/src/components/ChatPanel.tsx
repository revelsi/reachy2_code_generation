import React from "react";
import { Message } from "@/types/chat";
import { Loader2 } from "lucide-react";
import { ChatMessage } from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";

interface ChatPanelProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isProcessing: boolean;
  chatEndRef: React.RefObject<HTMLDivElement>;
  onApproveFunction?: (functionId: string) => void;
  onRejectFunction?: (functionId: string) => void;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({
  messages,
  onSendMessage,
  isProcessing,
  chatEndRef,
  onApproveFunction,
  onRejectFunction
}) => {
  return (
    <div className="flex flex-col h-full rounded-xl bg-card/80 backdrop-blur-sm shadow-sm">
      {/* Header */}
      <div className="p-4 border-b border-border/30 bg-card/80 backdrop-blur-sm rounded-t-xl">
        <h2 className="text-lg font-medium text-card-foreground">Chat with Reachy</h2>
      </div>
      
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8">
            <div className="max-w-md space-y-4">
              <h3 className="text-xl font-semibold">Welcome to Reachy Function Calling</h3>
              <p className="text-muted-foreground">
                Ask questions or give commands to control the Reachy robot. You'll see function calls that require your approval before execution.
              </p>
              <div className="text-sm text-muted-foreground border-t border-border/50 pt-4 mt-6">
                <p>Example commands:</p>
                <ul className="mt-2 space-y-1 list-disc list-inside">
                  <li>"What's the current status of the robot?"</li>
                  <li>"Move the right arm to a relaxed position"</li>
                  <li>"Turn the robot's head to look at me"</li>
                  <li>"Move the robot forward 0.5 meters"</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="divide-y divide-border/30">
            {messages.map((message) => (
              <ChatMessage 
                key={message.id} 
                message={message} 
                onApproveFunction={onApproveFunction}
                onRejectFunction={onRejectFunction}
              />
            ))}
          </div>
        )}
        
        {/* Processing animation */}
        {isProcessing && (
          <div className="flex items-center justify-center p-4">
            <Loader2 className="h-6 w-6 animate-spin text-primary/70" />
          </div>
        )}
        
        {/* Invisible element for scrolling to bottom */}
        <div ref={chatEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="p-4 border-t border-border/30 bg-card/80 backdrop-blur-sm rounded-b-xl">
        <ChatInput onSendMessage={onSendMessage} isProcessing={isProcessing} />
      </div>
    </div>
  );
}; 