import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Copy, Check, Play } from "lucide-react";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";

interface CodePanelProps {
  code: string;
  onExecuteCode?: (code: string) => void;
  isExecuting?: boolean;
}

export const CodePanel: React.FC<CodePanelProps> = ({ 
  code, 
  onExecuteCode,
  isExecuting = false
}) => {
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();
  
  const copyToClipboard = () => {
    if (!code) return;
    
    navigator.clipboard.writeText(code)
      .then(() => {
        setCopied(true);
        toast({
          title: "Copied!",
          description: "Code copied to clipboard",
        });
        
        // Reset copied state after 2 seconds
        setTimeout(() => {
          setCopied(false);
        }, 2000);
      })
      .catch((error) => {
        console.error("Failed to copy code:", error);
        toast({
          title: "Error",
          description: "Failed to copy code to clipboard",
          variant: "destructive",
        });
      });
  };

  const handleExecuteCode = () => {
    if (!code || !onExecuteCode) return;
    onExecuteCode(code);
  };
  
  return (
    <div className="flex flex-col h-full rounded-xl bg-card/80 backdrop-blur-sm shadow-sm">
      {/* Header */}
      <div className="p-4 border-b border-border/30 bg-card/80 backdrop-blur-sm rounded-t-xl flex justify-between items-center">
        <h2 className="text-lg font-medium text-card-foreground">Code Output</h2>
        
        <div className="flex gap-2">
          {code && onExecuteCode && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleExecuteCode}
              className="h-8 px-2 text-xs"
              disabled={isExecuting}
            >
              <Play className="h-3.5 w-3.5 mr-1" />
              {isExecuting ? "Executing..." : "Execute"}
            </Button>
          )}
          
          {code && (
            <Button
              variant="ghost"
              size="sm"
              onClick={copyToClipboard}
              className="h-8 px-2 text-xs"
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5 mr-1" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5 mr-1" />
                  Copy
                </>
              )}
            </Button>
          )}
        </div>
      </div>
      
      {/* Code Area */}
      <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
        {code ? (
          <pre className={cn(
            "whitespace-pre-wrap overflow-x-auto p-4 rounded-md bg-secondary/10 border border-border/50",
            "text-sm font-mono"
          )}>
            {code}
          </pre>
        ) : (
          <div className="h-full flex items-center justify-center text-muted-foreground text-sm">
            <p>No code to display yet. Ask a question to generate code.</p>
          </div>
        )}
      </div>
    </div>
  );
}; 