export interface RobotStatus {
  connection_status: string;
  last_update: string;
  arms?: {
    left?: ArmPosition;
    right?: ArmPosition;
  };
  head?: HeadPosition;
  base?: BasePosition;
  last_action?: any;
  error?: string;
}

export interface ArmPosition {
  position: number[];
  gripper_opening: number;
}

export interface HeadPosition {
  position: number[];
}

export interface BasePosition {
  position: number[];
}

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, any>;
} 