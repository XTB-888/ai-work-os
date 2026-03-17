import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatDateTime(date: string): string {
  return new Date(date).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    draft: 'bg-gray-100 text-gray-800',
    planning: 'bg-blue-100 text-blue-800',
    executing: 'bg-yellow-100 text-yellow-800',
    reviewing: 'bg-purple-100 text-purple-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    cancelled: 'bg-gray-100 text-gray-800',
    pending: 'bg-gray-100 text-gray-800',
    in_progress: 'bg-blue-100 text-blue-800',
    blocked: 'bg-orange-100 text-orange-800',
    review: 'bg-purple-100 text-purple-800',
    approved: 'bg-green-100 text-green-800',
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

export function getTaskTypeIcon(taskType: string): string {
  const icons: Record<string, string> = {
    research: '🔬',
    product_design: '🎨',
    software_development: '💻',
    business_analysis: '📊',
    startup_planning: '🚀',
  }
  return icons[taskType] || '📋'
}

export function getAgentTypeIcon(agentType: string): string {
  const icons: Record<string, string> = {
    coordinator: '👔',
    planner: '📋',
    specialist: '🔧',
  }
  return icons[agentType] || '🤖'
}
