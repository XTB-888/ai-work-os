import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">
          AI Work OS
        </h1>
        <p className="text-2xl text-gray-600 mb-8">
          Transform Goals into Results with AI Agent Teams
        </p>
        <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
          An AI-powered work operating system that assembles specialized AI agents
          to collaborate and complete complex tasks automatically.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Get Started
          </Link>
          <Link
            href="/register"
            className="px-8 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition"
          >
            Sign Up
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold mb-2">Multi-Agent Teams</h3>
            <p className="text-gray-600">
              Specialized AI agents collaborate like a real team
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4">👁️</div>
            <h3 className="text-xl font-semibold mb-2">Observable Execution</h3>
            <p className="text-gray-600">
              Watch your AI team work in real-time
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Clear Accountability</h3>
            <p className="text-gray-600">
              Track who did what and why
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
