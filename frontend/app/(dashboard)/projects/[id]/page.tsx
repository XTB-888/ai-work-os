"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api/client";
import { useWebSocket } from "@/hooks/useWebSocket";
import type { Project, Agent, Task, Message, Decision, Output } from "@/types";

/* ── Status badge colours ── */
const S: Record<string, string> = {
  pending: "bg-gray-100 text-gray-600",
  in_progress: "bg-yellow-100 text-yellow-700",
  completed: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
  review: "bg-purple-100 text-purple-700",
  idle: "bg-gray-100 text-gray-600",
  working: "bg-yellow-100 text-yellow-700",
  draft: "bg-gray-100 text-gray-600",
  approved: "bg-green-100 text-green-700",
  executing: "bg-yellow-100 text-yellow-700",
  planning: "bg-blue-100 text-blue-700",
};

const AGENT_TYPE_ICON: Record<string, string> = {
  coordinator: "👔",
  planner: "📋",
  specialist: "⚙️",
};

const MSG_TYPE_ICON: Record<string, string> = {
  TASK_ASSIGNMENT: "📌",
  PROPOSAL: "💡",
  QUESTION: "❓",
  DECISION: "⚖️",
  REPORT: "📊",
  DISCUSSION: "💬",
  INFO: "ℹ️",
  ERROR: "🚨",
};

/* ── Tab selector ── */
type Tab = "team" | "tasks" | "messages" | "decisions" | "outputs";

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { lastEvent } = useWebSocket(id);

  const [project, setProject] = useState<Project | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [outputs, setOutputs] = useState<Output[]>([]);
  const [tab, setTab] = useState<Tab>("team");
  const [loading, setLoading] = useState(true);

  /* ── Fetch all data ── */
  const fetchAll = async () => {
    try {
      const [p, a, t, m, d, o] = await Promise.all([
        api.getProject(id),
        api.getAgents(id),
        api.getTasks(id),
        api.getMessages(id),
        api.getDecisions(id),
        api.getOutputs(id),
      ]);
      setProject(p);
      setAgents(a);
      setTasks(t);
      setMessages(m);
      setDecisions(d);
      setOutputs(o);
    } catch {
      router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchAll(); }, [id]);

  /* ── Auto-refresh while executing ── */
  useEffect(() => {
    if (!project || project.status === "completed" || project.status === "failed") return;
    const timer = setInterval(fetchAll, 5000);
    return () => clearInterval(timer);
  }, [project?.status]);

  /* ── Refresh on WS event ── */
  useEffect(() => { if (lastEvent) fetchAll(); }, [lastEvent]);

  if (loading || !project) {
    return <div className="flex min-h-screen items-center justify-center text-gray-400">Loading project…</div>;
  }

  const agentMap = Object.fromEntries(agents.map((a) => [a.id, a]));
  const agentName = (aid?: string) => (aid && agentMap[aid]?.name) || "—";
  const progress = project.total_tasks > 0 ? Math.round((project.completed_tasks / project.total_tasks) * 100) : 0;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      {/* ── Header ── */}
      <div className="mb-6 flex items-start justify-between">
        <div>
          <button onClick={() => router.push("/projects")} className="text-sm text-gray-400 hover:text-gray-600 mb-1">&larr; Projects</button>
          <h1 className="text-2xl font-bold">{project.name}</h1>
          <p className="text-sm text-gray-500 mt-1 max-w-2xl">{project.goal_raw}</p>
        </div>
        <span className={`rounded-full px-4 py-1.5 text-sm font-medium ${S[project.status] || "bg-gray-100"}`}>
          {project.status}
        </span>
      </div>

      {/* ── Progress bar ── */}
      <div className="mb-6">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>{project.completed_tasks}/{project.total_tasks} tasks</span>
          <span>{progress}%</span>
        </div>
        <div className="h-2 rounded-full bg-gray-200 overflow-hidden">
          <div className="h-full rounded-full bg-brand-600 transition-all duration-500" style={{ width: `${progress}%` }} />
        </div>
      </div>

      {/* ── Tabs ── */}
      <div className="flex gap-1 border-b mb-6">
        {(["team", "tasks", "messages", "decisions", "outputs"] as Tab[]).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2.5 text-sm font-medium capitalize transition ${
              tab === t ? "border-b-2 border-brand-600 text-brand-600" : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {t} {t === "tasks" ? `(${tasks.length})` : t === "messages" ? `(${messages.length})` : ""}
          </button>
        ))}
      </div>

      {/* ── Tab content ── */}
      {tab === "team" && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {agents.map((a) => (
            <div key={a.id} className="rounded-xl border bg-white p-5 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xl">{AGENT_TYPE_ICON[a.agent_type] || "🤖"}</span>
                <div>
                  <h3 className="font-semibold">{a.name}</h3>
                  <p className="text-xs text-gray-400">{a.role}</p>
                </div>
                <span className={`ml-auto rounded-full px-2 py-0.5 text-xs ${S[a.status] || "bg-gray-100"}`}>{a.status}</span>
              </div>
              <p className="text-sm text-gray-500 mb-3">{a.description}</p>
              <div className="flex gap-4 text-xs text-gray-400">
                <span>Auth: L{a.authority_level}</span>
                <span>Tasks: {a.tasks_completed}/{a.tasks_assigned}</span>
                <span>Msgs: {a.messages_sent}</span>
              </div>
              <div className="mt-2 flex flex-wrap gap-1">
                {a.capabilities.map((c) => (
                  <span key={c} className="rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-500">{c}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === "tasks" && (
        <div className="space-y-3">
          {tasks.map((t) => (
            <div key={t.id} className="rounded-xl border bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between mb-1">
                <h3 className="font-medium">{t.title}</h3>
                <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${S[t.status] || "bg-gray-100"}`}>{t.status}</span>
              </div>
              {t.description && <p className="text-sm text-gray-500 mb-2">{t.description}</p>}
              <div className="flex gap-4 text-xs text-gray-400">
                <span>Owner: {agentName(t.owner_agent_id)}</span>
                <span>Reviewer: {agentName(t.reviewer_agent_id)}</span>
                <span>Approver: {agentName(t.approver_agent_id)}</span>
                {t.estimated_duration && <span>~{t.estimated_duration}min</span>}
              </div>
              {t.error_message && <p className="mt-2 text-xs text-red-500">Error: {t.error_message}</p>}
            </div>
          ))}
          {tasks.length === 0 && <p className="text-center text-gray-400 py-8">Tasks will appear once the Planner Agent creates them…</p>}
        </div>
      )}

      {tab === "messages" && (
        <div className="space-y-3 max-h-[600px] overflow-y-auto">
          {messages.map((m) => (
            <div key={m.id} className="rounded-xl border bg-white p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-1">
                <span>{MSG_TYPE_ICON[m.message_type] || "💬"}</span>
                <span className="text-xs font-medium text-brand-600">{agentName(m.sender_agent_id)}</span>
                <span className="text-xs text-gray-400">&rarr;</span>
                <span className="text-xs text-gray-500">{agentName(m.receiver_agent_id)}</span>
                <span className="ml-auto text-xs text-gray-300">{new Date(m.created_at).toLocaleTimeString()}</span>
              </div>
              {m.subject && <p className="text-sm font-medium">{m.subject}</p>}
              <p className="text-sm text-gray-600 whitespace-pre-wrap">{m.content}</p>
            </div>
          ))}
          {messages.length === 0 && <p className="text-center text-gray-400 py-8">Agent messages will appear here…</p>}
        </div>
      )}

      {tab === "decisions" && (
        <div className="space-y-3">
          {decisions.map((d) => (
            <div key={d.id} className="rounded-xl border bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between mb-1">
                <h3 className="font-medium">⚖️ {d.title}</h3>
                <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${S[d.status] || "bg-gray-100"}`}>{d.status}</span>
              </div>
              <p className="text-sm text-gray-600">{d.description}</p>
              <p className="text-sm text-gray-500 mt-1"><strong>Rationale:</strong> {d.rationale}</p>
              <div className="flex gap-4 text-xs text-gray-400 mt-2">
                <span>By: {agentName(d.made_by_agent_id)}</span>
                <span>Type: {d.decision_type}</span>
              </div>
            </div>
          ))}
          {decisions.length === 0 && <p className="text-center text-gray-400 py-8">Decisions will appear as agents make them…</p>}
        </div>
      )}

      {tab === "outputs" && (
        <div className="space-y-3">
          {outputs.map((o) => (
            <div key={o.id} className="rounded-xl border bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between mb-1">
                <h3 className="font-medium">{o.title}</h3>
                <div className="flex gap-2">
                  <span className="rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-500">{o.output_type}</span>
                  <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${S[o.status] || "bg-gray-100"}`}>{o.status}</span>
                </div>
              </div>
              {o.description && <p className="text-sm text-gray-500 mb-2">{o.description}</p>}
              <div className="flex gap-4 text-xs text-gray-400 mb-2">
                <span>Author: {agentName(o.author_agent_id)}</span>
                <span>v{o.version}</span>
                {o.quality_score && <span>Score: {o.quality_score}/10</span>}
              </div>
              {o.content && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-xs text-brand-600 hover:underline">View content</summary>
                  <pre className="mt-2 max-h-80 overflow-auto rounded-lg bg-gray-900 p-4 text-xs text-green-400">{o.content}</pre>
                </details>
              )}
            </div>
          ))}
          {outputs.length === 0 && <p className="text-center text-gray-400 py-8">Outputs will appear as agents produce them…</p>}
        </div>
      )}
    </div>
  );
}
