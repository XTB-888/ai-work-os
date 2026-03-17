'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api'
import { formatDateTime, getStatusColor, getAgentTypeIcon } from '@/lib/utils'
import type { Project, Agent, Task, Message, Decision, Output } from '@/types/api'

export default function ProjectDetailPage() {
  const params = useParams()
  const router = useRouter()
  const projectId = params.id as string

  const [project, setProject] = useState<Project | null>(null)
  const [agents, setAgents] = useState<Agent[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [decisions, setDecisions] = useState<Decision[]>([])
  const [outputs, setOutputs] = useState<Output[]>([])
  const [activeTab, setActiveTab] = useState<'overview' | 'agents' | 'tasks' | 'messages' | 'decisions' | 'outputs'>('overview')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!apiClient.isAuthenticated()) {
      router.push('/login')
      return
    }

    loadProjectData()
    // Poll for updates every 5 seconds
    const interval = setInterval(loadProjectData, 5000)
    return () => clearInterval(interval)
  }, [projectId, router])

  const loadProjectData = async () => {
    try {
      const [projectData, agentsData, tasksData, messagesData, decisionsData, outputsData] = await Promise.all([
        apiClient.getProject(projectId),
        apiClient.getAgents(projectId),
        apiClient.getTasks(projectId),
        apiClient.getMessages(projectId),
        apiClient.getDecisions(projectId),
        apiClient.getOutputs(projectId),
      ])

      setProject(projectData)
      setAgents(agentsData)
      setTasks(tasksData)
      setMessages(messagesData)
      setDecisions(decisionsData)
      setOutputs(outputsData)
      setError('')
    } catch (err: any) {
      if (err.response?.status === 401) {
        router.push('/login')
      } else {
        setError('Failed to load project data')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading project...</p>
        </div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-600">Project not found</p>
          <Link href="/projects">
            <Button className="mt-4">← Back to Projects</Button>
          </Link>
        </div>
      </div>
    )
  }

  const progressPercentage = project.total_tasks > 0 
    ? Math.round((project.completed_tasks / project.total_tasks) * 100) 
    : 0

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <Link href="/projects">
                  <Button variant="outline" size="sm">← Back</Button>
                </Link>
                <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(project.status)}`}>
                  {project.status}
                </span>
              </div>
              <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
              <p className="text-sm text-gray-600 mt-1">{project.description || project.goal_raw}</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-600">Progress</div>
              <div className="text-3xl font-bold text-blue-600">{progressPercentage}%</div>
              <div className="text-xs text-gray-500">
                {project.completed_tasks}/{project.total_tasks} tasks
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', count: null },
              { id: 'agents', label: 'Agents', count: agents.length },
              { id: 'tasks', label: 'Tasks', count: tasks.length },
              { id: 'messages', label: 'Messages', count: messages.length },
              { id: 'decisions', label: 'Decisions', count: decisions.length },
              { id: 'outputs', label: 'Outputs', count: outputs.length },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
                {tab.count !== null && (
                  <span className="ml-2 py-0.5 px-2 rounded-full bg-gray-100 text-gray-600 text-xs">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
            {error}
          </div>
        )}

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Project Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className="font-medium">{project.status}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Task Type:</span>
                  <span className="font-medium">{project.task_type.replace('_', ' ')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Tasks:</span>
                  <span className="font-medium">{project.total_tasks}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Completed:</span>
                  <span className="font-medium">{project.completed_tasks}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Messages:</span>
                  <span className="font-medium">{project.total_messages}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Decisions:</span>
                  <span className="font-medium">{project.total_decisions}</span>
                </div>
                <div className="pt-3 border-t border-gray-200">
                  <div className="text-xs text-gray-500">
                    Created: {formatDateTime(project.created_at)}
                  </div>
                  {project.started_at && (
                    <div className="text-xs text-gray-500 mt-1">
                      Started: {formatDateTime(project.started_at)}
                    </div>
                  )}
                  {project.completed_at && (
                    <div className="text-xs text-gray-500 mt-1">
                      Completed: {formatDateTime(project.completed_at)}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="text-lg">Goal</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 whitespace-pre-wrap">{project.goal_raw}</p>
                {project.goal_parsed && Object.keys(project.goal_parsed).length > 0 && (
                  <div className="mt-4 p-4 bg-gray-50 rounded-md">
                    <p className="text-sm font-medium text-gray-700 mb-2">Parsed Requirements:</p>
                    <pre className="text-xs text-gray-600 overflow-auto">
                      {JSON.stringify(project.goal_parsed, null, 2)}
                    </pre>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Agents Tab */}
        {activeTab === 'agents' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <Card key={agent.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-2xl">{getAgentTypeIcon(agent.agent_type)}</span>
                        <CardTitle className="text-lg">{agent.name}</CardTitle>
                      </div>
                      <CardDescription>{agent.role}</CardDescription>
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(agent.status)}`}>
                      {agent.status}
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-gray-600">{agent.description}</p>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Authority:</span>
                      <span className="font-medium">Level {agent.authority_level}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Tasks:</span>
                      <span className="font-medium">
                        {agent.tasks_completed}/{agent.tasks_assigned}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Messages:</span>
                      <span className="font-medium">{agent.messages_sent}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Decisions:</span>
                      <span className="font-medium">{agent.decisions_made}</span>
                    </div>
                  </div>
                  {agent.capabilities.length > 0 && (
                    <div className="pt-3 border-t border-gray-200">
                      <p className="text-xs font-medium text-gray-700 mb-2">Capabilities:</p>
                      <div className="flex flex-wrap gap-1">
                        {agent.capabilities.map((cap, idx) => (
                          <span key={idx} className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded">
                            {cap}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Tasks Tab */}
        {activeTab === 'tasks' && (
          <div className="space-y-4">
            {tasks.map((task) => (
              <Card key={task.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <CardTitle className="text-lg">{task.title}</CardTitle>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(task.status)}`}>
                          {task.status}
                        </span>
                      </div>
                      {task.description && (
                        <CardDescription>{task.description}</CardDescription>
                      )}
                    </div>
                    <div className="text-right text-sm">
                      <div className="text-gray-600">Priority: {task.priority}</div>
                      {task.estimated_duration && (
                        <div className="text-gray-500 text-xs">~{task.estimated_duration}min</div>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Type:</span>
                      <p className="font-medium">{task.task_type}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Owner:</span>
                      <p className="font-medium text-xs">
                        {agents.find(a => a.id === task.owner_agent_id)?.name || 'N/A'}
                      </p>
                    </div>
                    {task.started_at && (
                      <div>
                        <span className="text-gray-600">Started:</span>
                        <p className="font-medium text-xs">{formatDateTime(task.started_at)}</p>
                      </div>
                    )}
                    {task.completed_at && (
                      <div>
                        <span className="text-gray-600">Completed:</span>
                        <p className="font-medium text-xs">{formatDateTime(task.completed_at)}</p>
                      </div>
                    )}
                  </div>
                  {task.error_message && (
                    <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-600">
                      {task.error_message}
                    </div>
                  )}
                  {task.output_data && Object.keys(task.output_data).length > 0 && (
                    <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-md">
                      <p className="text-sm font-medium text-green-800 mb-1">Output:</p>
                      <pre className="text-xs text-green-700 overflow-auto">
                        {JSON.stringify(task.output_data, null, 2)}
                      </pre>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
            {tasks.length === 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <p className="text-gray-600">No tasks yet. Workflow is starting...</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Messages Tab */}
        {activeTab === 'messages' && (
          <div className="space-y-4">
            {messages.map((message) => (
              <Card key={message.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded">
                          {message.message_type}
                        </span>
                        {message.is_important && (
                          <span className="text-red-500">⚠️</span>
                        )}
                        <CardTitle className="text-base">{message.subject}</CardTitle>
                      </div>
                      <CardDescription className="text-xs">
                        From: {agents.find(a => a.id === message.sender_agent_id)?.name || 'System'} →
                        To: {agents.find(a => a.id === message.receiver_agent_id)?.name || 'All'}
                      </CardDescription>
                    </div>
                    <span className="text-xs text-gray-500">
                      {formatDateTime(message.created_at)}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{message.content}</p>
                </CardContent>
              </Card>
            ))}
            {messages.length === 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <p className="text-gray-600">No messages yet</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Decisions Tab */}
        {activeTab === 'decisions' && (
          <div className="space-y-4">
            {decisions.map((decision) => (
              <Card key={decision.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <CardTitle className="text-lg">{decision.title}</CardTitle>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(decision.status)}`}>
                          {decision.status}
                        </span>
                      </div>
                      <CardDescription>
                        By: {agents.find(a => a.id === decision.made_by_agent_id)?.name || 'Unknown'}
                      </CardDescription>
                    </div>
                    <span className="text-xs text-gray-500">
                      {formatDateTime(decision.created_at)}
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-gray-700">{decision.description}</p>
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded-md">
                    <p className="text-sm font-medium text-blue-900 mb-1">Rationale:</p>
                    <p className="text-sm text-blue-800">{decision.rationale}</p>
                  </div>
                  {decision.options_considered.length > 0 && (
                    <div className="p-3 bg-gray-50 rounded-md">
                      <p className="text-sm font-medium text-gray-700 mb-2">Options Considered:</p>
                      <pre className="text-xs text-gray-600 overflow-auto">
                        {JSON.stringify(decision.options_considered, null, 2)}
                      </pre>
                    </div>
                  )}
                  <div className="p-3 bg-green-50 border border-green-200 rounded-md">
                    <p className="text-sm font-medium text-green-900 mb-1">Chosen Option:</p>
                    <pre className="text-xs text-green-800 overflow-auto">
                      {JSON.stringify(decision.chosen_option, null, 2)}
                    </pre>
                  </div>
                </CardContent>
              </Card>
            ))}
            {decisions.length === 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <p className="text-gray-600">No decisions yet</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Outputs Tab */}
        {activeTab === 'outputs' && (
          <div className="space-y-4">
            {outputs.map((output) => (
              <Card key={output.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <CardTitle className="text-lg">{output.title}</CardTitle>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(output.status)}`}>
                          {output.status}
                        </span>
                        {output.is_latest && (
                          <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                            Latest
                          </span>
                        )}
                      </div>
                      <CardDescription>
                        Type: {output.output_type} | Version: {output.version} |
                        By: {agents.find(a => a.id === output.author_agent_id)?.name || 'Unknown'}
                      </CardDescription>
                    </div>
                    <span className="text-xs text-gray-500">
                      {formatDateTime(output.created_at)}
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  {output.description && (
                    <p className="text-sm text-gray-700">{output.description}</p>
                  )}
                  {output.file_path && (
                    <div className="text-sm">
                      <span className="text-gray-600">File:</span>
                      <code className="ml-2 px-2 py-1 bg-gray-100 rounded text-xs">
                        {output.file_path}
                      </code>
                    </div>
                  )}
                  {output.content && (
                    <div className="p-3 bg-gray-900 rounded-md overflow-auto">
                      <pre className="text-xs text-green-400">
                        {output.content.substring(0, 500)}
                        {output.content.length > 500 && '...'}
                      </pre>
                    </div>
                  )}
                  {output.quality_score && (
                    <div className="text-sm">
                      <span className="text-gray-600">Quality Score:</span>
                      <span className="ml-2 font-medium">{output.quality_score}/1.00</span>
                    </div>
                  )}
                  {output.review_comments && (
                    <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                      <p className="text-sm font-medium text-yellow-900 mb-1">Review Comments:</p>
                      <p className="text-sm text-yellow-800">{output.review_comments}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
            {outputs.length === 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <p className="text-gray-600">No outputs yet</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
