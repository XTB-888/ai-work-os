/* ── API client for AI Work OS backend ── */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

/* ── Auth ── */
export const api = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    request<any>("/api/v1/auth/register", { method: "POST", body: JSON.stringify(data) }),

  login: (data: { email: string; password: string }) =>
    request<any>("/api/v1/auth/login", { method: "POST", body: JSON.stringify(data) }),

  me: () => request<any>("/api/v1/auth/me"),

  /* ── Projects ── */
  createProject: (data: { name: string; description?: string; goal: string }) =>
    request<any>("/api/v1/projects", { method: "POST", body: JSON.stringify(data) }),

  listProjects: () => request<any[]>("/api/v1/projects"),

  getProject: (id: string) => request<any>(`/api/v1/projects/${id}`),

  /* ── Project sub-resources ── */
  getAgents: (projectId: string) => request<any[]>(`/api/v1/projects/${projectId}/agents`),
  getTasks: (projectId: string) => request<any[]>(`/api/v1/projects/${projectId}/tasks`),
  getMessages: (projectId: string) => request<any[]>(`/api/v1/projects/${projectId}/messages`),
  getDecisions: (projectId: string) => request<any[]>(`/api/v1/projects/${projectId}/decisions`),
  getOutputs: (projectId: string) => request<any[]>(`/api/v1/projects/${projectId}/outputs`),
};
