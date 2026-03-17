'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api'

export default function NewProjectPage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [goal, setGoal] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const project = await apiClient.createProject(name, goal, description || undefined)
      router.push(`/projects/${project.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  const exampleGoals = [
    'Build a REST API for task management with FastAPI and PostgreSQL',
    'Research the impact of AI on healthcare in 2024',
    'Design a mobile app for fitness tracking with user authentication',
    'Analyze the SaaS market for project management tools',
    'Create a business plan for an AI-powered education platform',
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Create New Project</h1>
              <p className="text-sm text-gray-600">Describe your goal and let AI agents work</p>
            </div>
            <Link href="/projects">
              <Button variant="outline">← Back</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Form */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Project Details</CardTitle>
                <CardDescription>
                  Tell us what you want to accomplish
                </CardDescription>
              </CardHeader>
              <form onSubmit={handleSubmit}>
                <CardContent className="space-y-6">
                  {error && (
                    <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                      {error}
                    </div>
                  )}

                  <div className="space-y-2">
                    <label htmlFor="name" className="text-sm font-medium">
                      Project Name *
                    </label>
                    <Input
                      id="name"
                      placeholder="My Awesome Project"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="goal" className="text-sm font-medium">
                      Goal (Natural Language) *
                    </label>
                    <textarea
                      id="goal"
                      className="flex min-h-[120px] w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="Describe what you want to accomplish in natural language..."
                      value={goal}
                      onChange={(e) => setGoal(e.target.value)}
                      required
                    />
                    <p className="text-xs text-gray-500">
                      Be specific about requirements, tech stack, features, and constraints
                    </p>
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="description" className="text-sm font-medium">
                      Description (Optional)
                    </label>
                    <textarea
                      id="description"
                      className="flex min-h-[80px] w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
                      placeholder="Additional context or notes..."
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                    />
                  </div>

                  <div className="flex gap-3">
                    <Button type="submit" disabled={loading} className="flex-1">
                      {loading ? 'Creating...' : 'Create Project'}
                    </Button>
                    <Link href="/projects">
                      <Button type="button" variant="outline">
                        Cancel
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </form>
            </Card>
          </div>

          {/* Examples */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Example Goals</CardTitle>
                <CardDescription>Click to use as template</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {exampleGoals.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => setGoal(example)}
                    className="w-full text-left p-3 text-sm bg-gray-50 hover:bg-gray-100 rounded-md border border-gray-200 transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </CardContent>
            </Card>

            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="text-lg">What Happens Next?</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-gray-600">
                <div className="flex gap-3">
                  <span className="text-xl">🔍</span>
                  <div>
                    <p className="font-medium text-gray-900">Goal Analysis</p>
                    <p>AI analyzes your goal and identifies requirements</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <span className="text-xl">👥</span>
                  <div>
                    <p className="font-medium text-gray-900">Team Assembly</p>
                    <p>System creates specialized AI agents</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <span className="text-xl">📋</span>
                  <div>
                    <p className="font-medium text-gray-900">Task Planning</p>
                    <p>Planner breaks down into actionable tasks</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <span className="text-xl">⚙️</span>
                  <div>
                    <p className="font-medium text-gray-900">Execution</p>
                    <p>Agents collaborate to complete tasks</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
