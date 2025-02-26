import { Tool } from "@/types/robot";

// Use the correct API base URL
const API_BASE_URL = process.env.NODE_ENV === 'production' ? "/api" : "http://localhost:5001/api";

export async function sendChatMessage(message: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to send message");
    }

    return await response.json();
  } catch (error) {
    console.error("Error sending chat message:", error);
    throw error;
  }
}

export async function resetConversation() {
  try {
    const response = await fetch(`${API_BASE_URL}/reset`, {
      method: "POST",
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to reset conversation");
    }

    return await response.json();
  } catch (error) {
    console.error("Error resetting conversation:", error);
    throw error;
  }
}

export async function getTools(): Promise<Tool[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/tools`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to get tools");
    }

    const data = await response.json();
    return data.tools;
  } catch (error) {
    console.error("Error getting tools:", error);
    throw error;
  }
}

export async function getRobotStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/status`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to get robot status");
    }

    return await response.json();
  } catch (error) {
    console.error("Error getting robot status:", error);
    throw error;
  }
}

export async function updateConfig(config: {
  model?: string;
  focus_modules?: string[];
  regenerate_tools?: boolean;
}) {
  try {
    const response = await fetch(`${API_BASE_URL}/config`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to update config");
    }

    return await response.json();
  } catch (error) {
    console.error("Error updating config:", error);
    throw error;
  }
} 