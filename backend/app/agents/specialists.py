"""
Specialist agents – Architect, Engineer, QA, Research, Writer.
Each wraps the corresponding prompt and persists outputs.
"""
import json
from typing import Any, Dict
from uuid import UUID

from app.agents.base import BaseAgent
from app.agents.prompts.specialists import (
    ARCHITECT_SYSTEM,
    ENGINEER_SYSTEM,
    QA_SYSTEM,
    RESEARCH_SYSTEM,
    WRITER_SYSTEM,
)
from app.models.output import Output


# ── Architect ────────────────────────────────────────────────────
class ArchitectAgent(BaseAgent):
    role = "ArchitectAgent"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return ARCHITECT_SYSTEM.format(
            project_name=context.get("project_name", ""),
            goal_raw=context.get("goal_raw", ""),
            goal_parsed=json.dumps(context.get("goal_parsed", {}), indent=2),
            task_title=context.get("task_title", ""),
            task_description=context.get("task_description", ""),
            instruction=context.get("instruction", "Design the system architecture."),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.invoke_llm(self.build_prompt(context))
        # persist architecture as an output
        arch = result.get("architecture", {})
        output = Output(
            project_id=self.project_id,
            task_id=context.get("task_id"),
            output_type="design",
            title="System Architecture",
            description="Architecture design produced by ArchitectAgent",
            author_agent_id=self.agent_id,
            content=json.dumps(arch, indent=2),
            status="draft",
            version="1.0.0",
        )
        self.db.add(output)
        await self.db.flush()
        result["output_id"] = str(output.id)
        return result


# ── Backend Engineer ─────────────────────────────────────────────
class BackendEngineerAgent(BaseAgent):
    role = "BackendEngineerAgent"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return ENGINEER_SYSTEM.format(
            project_name=context.get("project_name", ""),
            goal_raw=context.get("goal_raw", ""),
            architecture=context.get("architecture", "Not yet defined"),
            task_title=context.get("task_title", ""),
            task_description=context.get("task_description", ""),
            instruction=context.get("instruction", "Implement the required functionality."),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.invoke_llm(self.build_prompt(context))
        # persist each generated file as an output
        for f in result.get("files", []):
            output = Output(
                project_id=self.project_id,
                task_id=context.get("task_id"),
                output_type="code",
                title=f.get("path", "code_file"),
                description=f.get("description", ""),
                author_agent_id=self.agent_id,
                content=f.get("content", ""),
                file_path=f.get("path"),
                file_format=f.get("path", "").rsplit(".", 1)[-1] if "." in f.get("path", "") else "py",
                status="draft",
                version="1.0.0",
            )
            self.db.add(output)
        await self.db.flush()
        return result


# ── QA Agent ─────────────────────────────────────────────────────
class QAAgent(BaseAgent):
    role = "QAAgent"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return QA_SYSTEM.format(
            project_name=context.get("project_name", ""),
            task_title=context.get("task_title", ""),
            deliverables=context.get("deliverables", ""),
            success_criteria=context.get("success_criteria", ""),
            instruction=context.get("instruction", "Review the deliverables."),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.invoke_llm(self.build_prompt(context))
        # record the review decision
        verdict = result.get("verdict", "needs_revision")
        await self.record_decision(
            title=f"QA Review: {context.get('task_title', 'task')}",
            description=result.get("feedback", ""),
            decision_type="quality_review",
            chosen_option={"verdict": verdict, "score": result.get("quality_score", 0)},
            rationale=result.get("thought", ""),
            task_id=context.get("task_id"),
        )
        return result


# ── Research Agent ───────────────────────────────────────────────
class ResearchAgent(BaseAgent):
    role = "ResearchAgent"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return RESEARCH_SYSTEM.format(
            project_name=context.get("project_name", ""),
            task_title=context.get("task_title", ""),
            task_description=context.get("task_description", ""),
            instruction=context.get("instruction", "Conduct the research."),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.invoke_llm(self.build_prompt(context))
        output = Output(
            project_id=self.project_id,
            task_id=context.get("task_id"),
            output_type="report",
            title=f"Research: {context.get('task_title', '')}",
            author_agent_id=self.agent_id,
            content=json.dumps(result.get("findings", []), indent=2),
            status="draft",
            version="1.0.0",
        )
        self.db.add(output)
        await self.db.flush()
        return result


# ── Writer Agent ─────────────────────────────────────────────────
class WriterAgent(BaseAgent):
    role = "WriterAgent"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return WRITER_SYSTEM.format(
            project_name=context.get("project_name", ""),
            task_title=context.get("task_title", ""),
            source_material=context.get("source_material", ""),
            instruction=context.get("instruction", "Write the document."),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.invoke_llm(self.build_prompt(context))
        doc = result.get("document", {})
        output = Output(
            project_id=self.project_id,
            task_id=context.get("task_id"),
            output_type="document",
            title=doc.get("title", context.get("task_title", "Document")),
            author_agent_id=self.agent_id,
            content=json.dumps(doc, indent=2),
            status="draft",
            version="1.0.0",
        )
        self.db.add(output)
        await self.db.flush()
        return result
