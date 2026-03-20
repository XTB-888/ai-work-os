'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'

export default function ProjectDetailPage() {
  const params = useParams()
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setTimeout(() => {
      setLoading(false)
    }, 1000)
  }, [])

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

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <Link href="/projects" className="text-blue-600 hover:underline text-sm">
                ← Back to Projects
              </Link>
              <h1 className="text-2xl font-bold text-gray-900 mt-1">Sample Project</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {['overview', 'agents', 'tasks', 'messages'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'overview' && (
              <div>
                <h2 className="text-lg font-semibold mb-4">Project Overview</h2>
                <p className="text-gray-600">This is a sample project for demonstration.</p>
              </div>
            )}
            {activeTab === 'agents' && (
              <div>
                <h2 className="text-lg font-semibold mb-4">AI Agents</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-medium">Coordinator Agent</h3>
                    <p className="text-sm text-gray-600">Manages the project team</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-medium">Planner Agent</h3>
                    <p className="text-sm text-gray-600">Creates task breakdowns</p>
                  </div>
                </div>
              </div>
            )}
            {activeTab === 'tasks' && (
              <div>
                <h2 className="text-lg font-semibold mb-4">Tasks</h2>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span>Design API Architecture</span>
                    <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Completed</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span>Implement Database Models</span>
                    <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">In Progress</span>
                  </div>
                </div>
              </div>
            )}
            {activeTab === 'messages' && (
              <div>
                <h2 className="text-lg font-semibold mb-4">Agent Messages</h2>
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm font-medium text-blue-900">Coordinator → Planner</p>
                    <p className="text-sm text-blue-800 mt-1">Please create a task breakdown for this project.</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
