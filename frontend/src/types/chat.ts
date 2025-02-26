export type MessageType = "user" | "system";

export interface Message {
  id: string;
  content: string;
  type: MessageType;
  timestamp: Date;
  thinking: string | null;
  codeOutput: string | null;
  toolCalls?: ToolCall[];
}

export interface ToolCall {
  name: string;
  arguments: Record<string, any>;
  result?: any;
  approved?: boolean;
} 