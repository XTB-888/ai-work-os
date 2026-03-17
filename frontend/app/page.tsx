import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 p-8">
      {/* Hero */}
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-brand-600 to-purple-600 bg-clip-text text-transparent">
          AI Work OS
        </h1>
        <p className="mt-4 text-lg text-gray-600">
          Transform Goals into Results with AI Agent Teams
        </p>
        <p className="mt-2 text-sm text-gray-500">
          Goal &rarr; AI Team &rarr; Workflow &rarr; Result
        </p>
      </div>

      {/* CTA */}
      <div className="flex gap-4">
        <Link
          href="/login"
          className="rounded-lg bg-brand-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-brand-700 transition"
        >
          Sign In
        </Link>
        <Link
          href="/register"
          className="rounded-lg border border-gray-300 px-6 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-100 transition"
        >
          Create Account
        </Link>
      </div>

      {/* Feature grid */}
      <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl">
        {[
          { icon: "🤖", title: "Multi-Agent Teams", desc: "Specialised AI agents collaborate like a real team" },
          { icon: "👁️", title: "Observable Execution", desc: "Watch every step in real-time" },
          { icon: "📊", title: "Full Accountability", desc: "Track who did what and why" },
        ].map((f) => (
          <div key={f.title} className="rounded-xl border bg-white p-6 shadow-sm">
            <span className="text-3xl">{f.icon}</span>
            <h3 className="mt-3 font-semibold">{f.title}</h3>
            <p className="mt-1 text-sm text-gray-500">{f.desc}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
