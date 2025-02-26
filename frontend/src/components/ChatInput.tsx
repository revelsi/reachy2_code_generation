import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isProcessing: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isProcessing }) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isProcessing) {
      onSendMessage(message);
      setMessage("");
    }
  };
  
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };
  
  // Auto resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <form 
      onSubmit={handleSubmit}
      className="relative w-full"
    >
      <div className="relative flex items-center w-full">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask something about Reachy 2..."
          rows={1}
          disabled={isProcessing}
          className={cn(
            "w-full resize-none rounded-xl border border-input/50 bg-background/50 backdrop-blur-sm px-4 py-3 pr-12",
            "focus:outline-none focus:ring-1 focus:ring-primary/30 focus:border-primary/30",
            "placeholder:text-muted-foreground/70 transition-all duration-200",
            "disabled:opacity-70 disabled:cursor-not-allowed",
            "text-base min-h-[3rem] max-h-32 shadow-sm"
          )}
        />
        <Button
          type="submit"
          variant="ghost"
          size="icon"
          disabled={!message.trim() || isProcessing}
          className={cn(
            "absolute right-2 h-9 w-9 rounded-full",
            "transition-all duration-200 hover:bg-primary/10",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
        >
          <Send 
            className={cn(
              "h-5 w-5", 
              message.trim() && !isProcessing ? "text-primary" : "text-muted-foreground/50"
            )} 
          />
        </Button>
      </div>
      <p className="text-xs text-muted-foreground/70 pt-2 text-center">
        {isProcessing ? "Processing your request..." : "Shift+Enter for new line, Enter to send"}
      </p>
    </form>
  );
};

export default ChatInput; 