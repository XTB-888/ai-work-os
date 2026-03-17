import axios, { AxiosInstance } from 'axios'
import type { User, TokenResponse, Project, Agent, Task, Message, Decision, Output } from '@/types/api'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private client: AxiosInstance
  private token: string | null = null

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Load token from localStorage if available
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('token')
      if (this.token) {
        this.setAuthHeader(this.token)
      }
    }
  }

  private setAuthHeader(token: string) {
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  // Auth
  async register(email: string, username: string, password: string, full_name?: string): Promise<TokenResponse> {
    const { data } = await this.client.post<TokenResponse>('/api/v1/auth/register', {
      email,
      username,
      password,
      full_name,
    })
    this.token = data.access_token
    this.setAuthHeader(this.token)
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', this.token)
    }
    return data
  }

  async login(email: string, password: string): Promise<TokenResponse> {
    const { data } = await this.client.post<TokenResponse>('/api/v1/auth/login', {
      email,
      password,
    })
    this.token = data.access_token
    this.setAuthHeader(this.token)
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', this.token)
    }
    return data
  }

  async getCurrentUser(): Promise<User> {
    const { data } = await this.client.get<User>('/api/v1/auth/me')
    return data
  }

  logout() {
    this.token = null
    delete this.client.defaults.headers.common['Authorization']
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token')
    }
  }

  // Projects
  async createProject(name: string, goal: string, description?: string): Promise<Project> {
    const { data } = await this.client.post<Project>('/api/v1/projects', {
      name,
      goal,
      description,
    })
    return data
  }

  async getProjects(): Promise<Project[]> {
    const { data } = await this.client.get<Project[]>('/api/v1/projects')
    return data
  }

  async getProject(id: string): Promise<Project> {
    const { data } = await this.client.get<Project>(`/api/v1/projects/${id}`)
    return data
  }

  // Project Data
  async getAgents(projectId: string): Promise<Agent[]> {
    const { data } = await this.client.get<Agent[]>(`/api/v1/projects/${projectId}/agents`)
    return data
  }

  async getTasks(projectId: string): Promise<Task[]> {
    const { data } = await this.client.get<Task[]>(`/api/v1/projects/${projectId}/tasks`)
    return data
  }

  async getMessages(projectId: string): Promise<Message[]> {
    const { data } = await this.client.get<Message[]>(`/api/v1/projects/${projectId}/messages`)
    return data
  }

  async getDecisions(projectId: string): Promise<Decision[]> {
    const { data } = await this.client.get<Decision[]>(`/api/v1/projects/${projectId}/decisions`)
    return data
  }

  async getOutputs(projectId: string): Promise<Output[]> {
    const { data } = await this.client.get<Output[]>(`/api/v1/projects/${projectId}/outputs`)
    return data
  }

  isAuthenticated(): boolean {
    return !!this.token
  }
}

export const apiClient = new ApiClient()
