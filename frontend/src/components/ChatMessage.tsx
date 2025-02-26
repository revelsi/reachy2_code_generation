import React, { useState } from "react";
import { Message } from "@/types/chat";
import { formatDate } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { MessageCircle, User, Code, ThumbsUp, ThumbsDown, ChevronDown, ChevronUp } from "lucide-react";

interface ChatMessageProps {
  message: Message;
  onApproveFunction?: (functionId: string) => void;
  onRejectFunction?: (functionId: string) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ 
  message, 
  onApproveFunction, 
  onRejectFunction 
}) => {
  const [showThinking, setShowThinking] = useState(false);
  const [showCodeOutput, setShowCodeOutput] = useState(false);
  
  const toggleThinking = () => {
    setShowThinking(!showThinking);
  };
  
  const toggleCodeOutput = () => {
    setShowCodeOutput(!showCodeOutput);
  };
  
  return (
    <div className={`flex flex-col p-4 ${message.type === 'user' ? 'bg-secondary/20' : 'bg-background'}`}>
      <div className="flex items-start gap-3">
        {/* Avatar */}
        <div className="w-8 h-8 rounded-full flex items-center justify-center bg-primary/10">
          {message.type === 'user' ? (
            <User className="h-4 w-4 text-primary" />
          ) : (
            <MessageCircle className="h-4 w-4 text-primary" />
          )}
        </div>
        
        {/* Message content */}
        <div className="flex-1 space-y-2">
          <div className="flex justify-between items-center">
            <div className="font-medium">
              {message.type === 'user' ? 'You' : 'Reachy Assistant'}
            </div>
            <div className="text-xs text-muted-foreground">
              {formatDate(message.timestamp)}
            </div>
          </div>
          
          {message.content && (
            <div className="text-sm leading-relaxed whitespace-pre-wrap">
              {message.content}
            </div>
          )}
          
          {/* Function call */}
          {message.functionCall && (
            <div className="mt-2 p-3 border border-border rounded-md bg-secondary/10">
              <div className="flex justify-between items-center mb-2">
                <div className="font-medium text-sm">
                  Function Call: <span className="font-bold">{message.functionCall.name}</span>
                </div>
                
                {/* Approval buttons */}
                {onApproveFunction && onRejectFunction && (
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="h-7 px-2 text-xs bg-green-500/10 hover:bg-green-500/20 border-green-500/30"
                      onClick={() => onApproveFunction(message.functionCall?.id || '')}
                    >
                      <ThumbsUp className="h-3.5 w-3.5 mr-1" />
                      Approve
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="h-7 px-2 text-xs bg-destructive/10 hover:bg-destructive/20 border-destructive/30"
                      onClick={() => onRejectFunction(message.functionCall?.id || '')}
                    >
                      <ThumbsDown className="h-3.5 w-3.5 mr-1" />
                      Reject
                    </Button>
                  </div>
                )}
              </div>
              
              {/* Parameters */}
              <div className="text-xs font-mono bg-secondary/20 p-2 rounded overflow-x-auto">
                <pre>{JSON.stringify(message.functionCall.parameters, null, 2)}</pre>
              </div>
            </div>
          )}
          
          {/* Thinking toggle */}
          {message.thinking && (
            <div className="mt-2">
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-7 px-2 text-xs"
                onClick={toggleThinking}
              >
                {showThinking ? (
                  <>
                    <ChevronUp className="h-3.5 w-3.5 mr-1" />
                    Hide thinking
                  </>
                ) : (
                  <>
                    <ChevronDown className="h-3.5 w-3.5 mr-1" />
                    Show thinking
                  </>
                )}
              </Button>
              
              {showThinking && (
                <div className="mt-2 p-3 border border-border rounded-md bg-secondary/10 text-xs font-mono whitespace-pre-wrap">
                  {message.thinking}
                </div>
              )}
            </div>
          )}
          
          {/* Code output toggle */}
          {message.codeOutput && (
            <div className="mt-2">
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-7 px-2 text-xs"
                onClick={toggleCodeOutput}
              >
                {showCodeOutput ? (
                  <>
                    <ChevronUp className="h-3.5 w-3.5 mr-1" />
                    Hide code output
                  </>
                ) : (
                  <>
                    <Code className="h-3.5 w-3.5 mr-1" />
                    Show code output
                  </>
                )}
              </Button>
              
              {showCodeOutput && (
                <div className="mt-2 p-3 border border-border rounded-md bg-secondary/10 text-xs font-mono whitespace-pre-wrap overflow-x-auto">
                  {message.codeOutput}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}; 