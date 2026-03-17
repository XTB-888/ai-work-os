"""
Workflow Engine – orchestrates the full Goal → Team → Tasks → Execution → Result pipeline.

This is the heart of AI Work OS.  It runs as a background task after a project is created.
It uses plain async orchestration (no LangGraph dependency at runtime so the MVP stays lean).
"""
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.project import Project
from app.models.agent import Agent
from app.models.task import Task
from app.models.message import Message
from app.models.workflow import Workflow

from app.agents.coordinator import CoordinatorAgent
from app.agents.planner import PlannerAgent
from app.agents.specialists import (
    ArchitectAgent,
    BackendEngineerAgent,
    QAAgent,
    ResearchAgent,
    WriterAgent,
)

logger = logging.getLogger(__name__)

# Map role strings → agent classes
AGENT_CLASS_MAP = {
    "CoordinatorAgent": CoordinatorAgent,
    "PlannerAgent": PlannerAgent,
    "ArchitectAgent": ArchitectAgent,
    "BackendEngineerAgent": BackendEngineerAgent,
    "QAAgent": QAAgent,
    "ResearchAgent": ResearchAgent,
    "WriterAgent": WriterAgent,
}


class WorkflowEngine:
    """Runs the entire project lifecycle."""

    @staticmethod
    async def run(project_id: str):
        """Entry-point called from a BackgroundTask."""
        logger.info("WorkflowEngine.run  project=%s", project_id)
        async with AsyncSessionLocal() as db:
            try:
                await WorkflowEngine._execute(db, UUID(project_id))
                await db.commit()
            except Exception:
                logger.exception("Workflow failed for project %s", project_id)
                await db.rollback()
                # mark project as failed
                async with AsyncSessionLocal() as db2:
                    proj = await db2.get(Project, UUID(project_id))
                    if proj:
                        proj.status = "failed"
                        await db2.commit()

    # ── internal pipeline ────────────────────────────────────────
    @staticmethod
    async def _execute(db: AsyncSession, project_id: UUID):
        # 1. Load project + agents
        project = await db.get(Project, project_id)
        if not project:
            return
        project.status = "executing"
        project.started_at = datetime.now(timezone.utc)

        result = await db.execute(select(Agent).where(Agent.project_id == project_id))
        agents = list(result.scalars().all())
        agent_map: Dict[str, Agent] = {a.role: a for a in agents}
        role_to_id: Dict[str, UUID] = {a.role: a.id for a in agents}
        agent_id_map: Dict[str, UUID] = role_to_id.copy()

        # helper to build team summary string
        team_summary = "\n".join(
            f"- {a.name} ({a.role}): {a.description}" for a in agents
        )

        # ── Phase 1: Coordinator kick-off ────────────────────────
        coord_agent_row = agent_map.get("CoordinatorAgent")
        if not coord_agent_row:
            project.status = "failed"
            return

        coord = CoordinatorAgent(coord_agent_row.id, project_id, db)
        coord_result = await coord.run({
            "project_name": project.name,
            "goal_raw": project.goal_raw,
            "goal_parsed": project.goal_parsed,
            "team_summary": team_summary,
            "project_status": "planning",
            "recent_messages": "None yet",
            "agent_id_map": agent_id_map,
        })
        logger.info("Coordinator result: %s", coord_result.get("summary", ""))

        # ── Phase 2: Planner creates tasks ───────────────────────
        planner_row = agent_map.get("PlannerAgent")
        if not planner_row:
            project.status = "failed"
            return

        planner = PlannerAgent(planner_row.id, project_id, db)
        planner_result = await planner.run({
            "project_name": project.name,
            "goal_raw": project.goal_raw,
            "goal_parsed": project.goal_parsed,
            "team_summary": team_summary,
            "coordinator_message": coord_result.get("summary", ""),
            "role_to_agent_id": role_to_id,
        })
        logger.info("Planner created %d tasks", len(planner_result.get("tasks", [])))

        # Reload tasks from DB
        task_result = await db.execute(
            select(Task).where(Task.project_id == project_id).order_by(Task.created_at)
        )
        tasks = list(task_result.scalars().all())
        project.total_tasks = len(tasks)

        # ── Phase 3: Execute tasks in dependency order ───────────
        completed_ids: set = set()
        architecture_json = ""

        for _round in range(20):  # safety cap
            # find next runnable tasks
            runnable = [
                t for t in tasks
                if t.status == "pending"
                and all(dep in completed_ids for dep in (t.depends_on or []))
            ]
            if not runnable:
                break

            for task in runnable:
                task.status = "in_progress"
                task.started_at = datetime.now(timezone.utc)
                await db.flush()

                # pick the right agent
                owner_agent_row = None
                if task.owner_agent_id:
                    owner_agent_row = next(
                        (a for a in agents if a.id == task.owner_agent_id), None
                    )
                if not owner_agent_row:
                    # fallback: first specialist
                    owner_agent_row = next(
                        (a for a in agents if a.agent_type == "specialist"), agents[0]
                    )

                agent_cls = AGENT_CLASS_MAP.get(owner_agent_row.role)
                if not agent_cls:
                    # generic fallback
                    agent_cls = BackendEngineerAgent

                agent_instance = agent_cls(owner_agent_row.id, project_id, db)

                context = {
                    "project_name": project.name,
                    "goal_raw": project.goal_raw,
                    "goal_parsed": project.goal_parsed,
                    "task_id": task.id,
                    "task_title": task.title,
                    "task_description": task.description or "",
                    "architecture": architecture_json,
                    "deliverables": "",
                    "success_criteria": json.dumps(
                        project.goal_parsed.get("success_criteria", [])
                    ),
                    "source_material": "",
                }

                try:
                    task_result_data = await agent_instance.run(context)

                    # capture architecture for downstream tasks
                    if owner_agent_row.role == "ArchitectAgent":
                        architecture_json = json.dumps(
                            task_result_data.get("architecture", {}), indent=2
                        )

                    task.status = "completed"
                    task.completed_at = datetime.now(timezone.utc)
                    task.output_data = task_result_data
                    completed_ids.add(str(task.id))
                    project.completed_tasks = len(completed_ids)

                    # update agent stats
                    owner_agent_row.tasks_completed += 1
                    owner_agent_row.status = "idle"

                except Exception as exc:
                    logger.exception("Task %s failed: %s", task.id, exc)
                    task.status = "failed"
                    task.error_message = str(exc)

                await db.flush()

        # ── Phase 4: Mark project complete ───────────────────────
        all_done = all(t.status in ("completed", "failed") for t in tasks)
        any_failed = any(t.status == "failed" for t in tasks)

        if all_done and not any_failed:
            project.status = "completed"
        elif any_failed:
            project.status = "completed"  # partial success
        else:
            project.status = "completed"

        project.completed_at = datetime.now(timezone.utc)
        if project.started_at:
            delta = project.completed_at - project.started_at
            project.actual_duration = int(delta.total_seconds() / 60)

        # Save workflow record
        wf = Workflow(
            project_id=project_id,
            name=f"Workflow for {project.name}",
            description="Auto-generated workflow",
            graph_definition={
                "tasks": [
                    {
                        "id": str(t.id),
                        "title": t.title,
                        "status": t.status,
                        "owner": t.owner_agent_id and str(t.owner_agent_id),
                        "depends_on": t.depends_on,
                    }
                    for t in tasks
                ]
            },
            status="completed",
        )
        db.add(wf)
        await db.flush()

        logger.info(
            "Project %s finished – %d/%d tasks completed",
            project_id,
            project.completed_tasks,
            project.total_tasks,
        )
