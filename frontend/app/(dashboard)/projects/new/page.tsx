"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api/client";

export default function NewProjectPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const project = await api.createProject({ name, goal });
      router.push(`/projects/${project.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl px-4 py-10">
      <h1 className="text-3xl font-bold mb-8">New Project</h1>

      <form onSubmit={handleSubmit} className="space-y-6 rounded-xl border bg-white p-8 shadow-sm">
        {error && <p className="text-sm text-red-600 bg-red-50 rounded p-3">{error}</p>}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Project Name</label>
          <input
            type="text" required value={name} onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Task Management API"
            className="w-full rounded-lg border px-4 py-2.5 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Goal</label>
          <textarea
            required value={goal} onChange={(e) => setGoal(e.target.value)} rows={5}
            placeholder="Describe what you want to achieve in natural language…&#10;&#10;e.g. Build a REST API for task management with FastAPI and PostgreSQL. It should support user authentication, CRUD operations for tasks, and team collaboration features."
            className="w-full rounded-lg border px-4 py-2.5 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 outline-none resize-none"
          />
          <p className="mt-1 text-xs text-gray-400">
            The system will automatically parse your goal, assemble an AI team, and start working.
          </p>
        </div>

        <button
          type="submit" disabled={loading || goal.length < 10}
          className="w-full rounded-lg bg-brand-600 py-3 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50 transition"
        >
          {loading ? "Creating project & assembling AI team…" : "Create Project"}
        </button>
      </form>
    </div>
  );
}
