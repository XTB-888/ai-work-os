"""
Planner Agent – breaks goals into tasks.
"""
import json
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import BaseAgent
from app.agents.prompts.planner import PLANNER_SYSTEM, PLANNER_BREAKDOWN_INSTRUCTION
from app.models.task import Task


class PlannerAgent(BaseAgent):
    role = "PlannerAgent"
    agent_type = "planner"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return PLANNER_SYSTEM.format(
            project_name=context.get("project_name", ""),
            goal_raw=context.get("goal_raw", ""),
            goal_parsed=json.dumps(context.get("goal_parsed", {}), indent=2),
            team_summary=context.get("team_summary", ""),
            coordinator_message=context.get("coordinator_message", ""),
            instruction=context.get("instruction", PLANNER_BREAKDOWN_INSTRUCTION),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self.build_prompt(context)
        result = await self.invoke_llm(prompt)

        # Create Task rows from the LLM output
        tasks_data = result.get("tasks", [])
        role_to_agent_id: Dict[str, UUID] = context.get("role_to_agent_id", {})
        created_tasks: List[Task] = []

        for idx, td in enumerate(tasks_data):
            owner_id = role_to_agent_id.get(td.get("owner_role"))
            reviewer_id = role_to_agent_id.get(td.get("reviewer_role"))
            approver_id = role_to_agent_id.get(td.get("approver_role"))

            task = Task(
                project_id=self.project_id,
                title=td.get("title", f"Task {idx + 1}"),
                description=td.get("description", ""),
                task_type=td.get("task_type", "coding"),
                owner_agent_id=owner_id,
                reviewer_agent_id=reviewer_id,
                approver_agent_id=approver_id,
                status="pending",
                priority=td.get("priority", 5),
                estimated_duration=td.get("estimated_duration", 30),
                depends_on=[],  # will be resolved after all tasks are created
            )
            self.db.add(task)
            created_tasks.append(task)

        await self.db.flush()

        # Resolve depends_on indices → UUIDs
        for idx, td in enumerate(tasks_data):
            dep_indices = td.get("depends_on_indices", [])
            dep_ids = []
            for di in dep_indices:
                if 0 <= di < len(created_tasks):
                    dep_ids.append(str(created_tasks[di].id))
            created_tasks[idx].depends_on = dep_ids

        await self.db.flush()

        result["created_task_ids"] = [str(t.id) for t in created_tasks]
        return result
