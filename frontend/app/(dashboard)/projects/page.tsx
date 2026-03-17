"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api/client";
import type { Project } from "@/types";

const STATUS_COLORS: Record<string, string> = {
  draft: "bg-gray-100 text-gray-700",
  planning: "bg-blue-100 text-blue-700",
  executing: "bg-yellow-100 text-yellow-700",
  completed: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
};

export default function ProjectsPage() {
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listProjects().then(setProjects).catch(() => router.push("/login")).finally(() => setLoading(false));
  }, [router]);

  if (loading) return <div className="flex min-h-screen items-center justify-center">Loading…</div>;

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Projects</h1>
        <Link
          href="/projects/new"
          className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 transition"
        >
          + New Project
        </Link>
      </div>

      {projects.length === 0 ? (
        <div className="rounded-xl border-2 border-dashed p-12 text-center text-gray-400">
          <p className="text-lg">No projects yet</p>
          <p className="text-sm mt-1">Create your first project to get started</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {projects.map((p) => (
            <Link
              key={p.id}
              href={`/projects/${p.id}`}
              className="flex items-center justify-between rounded-xl border bg-white p-5 shadow-sm hover:shadow-md transition"
            >
              <div>
                <h2 className="font-semibold">{p.name}</h2>
                <p className="text-sm text-gray-500 mt-1 line-clamp-1">{p.goal_raw}</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-gray-400">
                  {p.completed_tasks}/{p.total_tasks} tasks
                </span>
                <span className={`rounded-full px-3 py-1 text-xs font-medium ${STATUS_COLORS[p.status] || "bg-gray-100"}`}>
                  {p.status}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
