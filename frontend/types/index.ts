/* ── Shared TypeScript types for AI Work OS ── */

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  avatar_url?: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  task_type: string;
  status: string;
  priority: number;
  goal_raw: string;
  goal_parsed?: Record<string, any>;
  started_at?: string;
  completed_at?: string;
  estimated_duration?: number;
  actual_duration?: number;
  total_tasks: number;
  completed_tasks: number;
  total_messages: number;
  total_decisions: number;
  created_at: string;
  updated_at: string;
}

export interface Agent {
  id: string;
  project_id: string;
  role: string;
  name: string;
  description?: string;
  agent_type: string; // coordinator | planner | specialist
  capabilities: string[];
  tools: string[];
  authority_level: number;
  can_approve: boolean;
  can_delegate: boolean;
  status: string;
  tasks_assigned: number;
  tasks_completed: number;
  messages_sent: number;
  decisions_made: number;
  created_at: string;
}

export interface Task {
  id: string;
  project_id: string;
  title: string;
  description?: string;
  task_type: string;
  owner_agent_id?: string;
  reviewer_agent_id?: string;
  approver_agent_id?: string;
  status: string;
  priority: number;
  depends_on: string[];
  estimated_duration?: number;
  actual_duration?: number;
  started_at?: string;
  completed_at?: string;
  output_data?: Record<string, any>;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  project_id: string;
  task_id?: string;
  sender_agent_id?: string;
  receiver_agent_id?: string;
  message_type: string;
  subject?: string;
  content: string;
  thread_id?: string;
  is_important: boolean;
  requires_response: boolean;
  created_at: string;
}

export interface Decision {
  id: string;
  project_id: string;
  task_id?: string;
  decision_type: string;
  title: string;
  description: string;
  made_by_agent_id?: string;
  approved_by_agent_id?: string;
  options_considered: Record<string, any>[];
  chosen_option: Record<string, any>;
  rationale: string;
  impact_scope?: string;
  status: string;
  created_at: string;
}

export interface Output {
  id: string;
  project_id: string;
  task_id?: string;
  output_type: string;
  title: string;
  description?: string;
  author_agent_id?: string;
  reviewed_by_agent_id?: string;
  approved_by_agent_id?: string;
  content?: string;
  file_path?: string;
  file_format?: string;
  version: string;
  is_latest: boolean;
  status: string;
  quality_score?: number;
  review_comments?: string;
  created_at: string;
}
