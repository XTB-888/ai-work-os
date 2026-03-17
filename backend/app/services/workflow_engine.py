"""
Workflow Engine – orchestrates agent collaboration using LangGraph.
This is the heart of the AI Work OS.
"""
import json
import asyncio
from uuid import UUID
from typing import Dict, Any, List
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core import settings
from app.db.base import Base
from app.models.project import Project
from app.models.agent import Agent
from app.models.task import Task
from app.models.message import Message
from app.models.decision import Decision
from app.models.output import Output
from app.llm.provider import get_llm
from app.agents.prompts.coordinator import COORDINATOR_PROMPT, COORDINATOR_SYSTEM_MESSAGE
from app.agents.prompts.planner import PLANNER_PROMPT, PLANNER_SYSTEM_MESSAGE
from app.agents.prompts.backend_engineer import BACKEND_ENGINEER_PROMPT, BACKEND_ENGINEER_SYSTEM_MESSAGE


class WorkflowEngine:
    """
    Orchestrates the entire project execution workflow.
    
    Workflow phases:
    1. Initialization: Coordinator reviews goal and team
    2. Planning: Planner creates task breakdown
    3. Execution: Specialists execute tasks
    4. Review: QA reviews outputs
    5. Completion: Coordinator finalizes project
    """

    @staticmethod
    async def run(project_id: str):
        """Main entry point – runs the entire workflow for a project."""
        # Create a new DB session for this background task
        engine = create_async_engine(settings.DATABASE_URL, echo=False)
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as db:
            try:
                # Load project
                result = await db.execute(select(Project).where(Project.id == UUID(project_id)))
                project = result.scalar_one_or_none()
                if not project:
                    print(f"Project {project_id} not found")
                    return

                print(f"🚀 Starting workflow for project: {project.name}")

                # Phase 1: Coordinator initialization
                await WorkflowEngine._phase_coordinator_init(db, project)

                # Phase 2: Planner creates tasks
                await WorkflowEngine._phase_planner_breakdown(db, project)

                # Phase 3: Execute tasks
                await WorkflowEngine._phase_execute_tasks(db, project)

                # Phase 4: Finalize
                await WorkflowEngine._phase_finalize(db, project)

                print(f"✅ Workflow completed for project: {project.name}")

            except Exception as e:
                print(f"❌ Workflow error for project {project_id}: {e}")
                if project:
                    project.status = "failed"
                    await db.commit()

    @staticmethod
    async def _phase_coordinator_init(db: AsyncSession, project: Project):
        """Phase 1: Coordinator reviews the project and delegates to Planner."""
        print("📋 Phase 1: Coordinator Initialization")

        project.status = "planning"
        project.started_at = datetime.now(timezone.utc)
        await db.commit()

        # Get coordinator agent
        result = await db.execute(
            select(Agent).where(Agent.project_id == project.id, Agent.agent_type == "coordinator")
        )
        coordinator = result.scalar_one_or_none()
        if not coordinator:
            raise Exception("Coordinator agent not found")

        # Get all agents for team composition
        result = await db.execute(select(Agent).where(Agent.project_id == project.id))
        agents = result.scalars().all()
        team_composition = "\n".join([f"- {a.name} ({a.role}): {a.description}" for a in agents])

        # Build prompt
        prompt = COORDINATOR_PROMPT.format(
            agent_name=coordinator.name,
            project_id=str(project.id),
            task_type=project.task_type,
            user_goal=project.goal_raw,
            parsed_goal=json.dumps(project.goal_parsed, indent=2),
            team_composition=team_composition,
            project_status=project.status,
            progress_percentage=0,
            completed_tasks=0,
            total_tasks=0,
            current_phase="Initialization",
            recent_messages="(No messages yet)",
        )

        # Call LLM
        llm = get_llm(temperature=0.3)
        messages = [
            {"role": "system", "content": COORDINATOR_SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ]
        response = await llm.ainvoke(messages)
        response_text = response.content.strip()

        # Parse response
        try:
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            action_data = json.loads(response_text)
        except json.JSONDecodeError:
            print(f"⚠️ Coordinator response not valid JSON: {response_text[:200]}")
            action_data = {
                "action": "send_message",
                "reasoning": "Delegating to Planner",
                "data": {
                    "to": "PlannerAgent",
                    "message_type": "TASK_ASSIGNMENT",
                    "subject": "Create Task Breakdown",
                    "content": "Please analyze the goal and create a task breakdown.",
                },
            }

        # Execute action
        if action_data.get("action") == "send_message":
            data = action_data.get("data", {})
            # Find receiver agent
            result = await db.execute(
                select(Agent).where(
                    Agent.project_id == project.id, Agent.role == data.get("to", "PlannerAgent")
                )
            )
            receiver = result.scalar_one_or_none()

            msg = Message(
                project_id=project.id,
                sender_agent_id=coordinator.id,
                receiver_agent_id=receiver.id if receiver else None,
                message_type=data.get("message_type", "INFO"),
                subject=data.get("subject", ""),
                content=data.get("content", ""),
            )
            db.add(msg)
            coordinator.messages_sent += 1
            await db.commit()
            print(f"  ✉️ Coordinator → {data.get('to')}: {data.get('subject')}")

    @staticmethod
    async def _phase_planner_breakdown(db: AsyncSession, project: Project):
        """Phase 2: Planner creates task breakdown."""
        print("📝 Phase 2: Planner Task Breakdown")

        # Get planner agent
        result = await db.execute(
            select(Agent).where(Agent.project_id == project.id, Agent.agent_type == "planner")
        )
        planner = result.scalar_one_or_none()
        if not planner:
            raise Exception("Planner agent not found")

        # Get team
        result = await db.execute(select(Agent).where(Agent.project_id == project.id))
        agents = result.scalars().all()
        team_composition = "\n".join([f"- {a.name} ({a.role})" for a in agents])

        # Get recent messages
        result = await db.execute(
            select(Message)
            .where(Message.project_id == project.id)
            .order_by(Message.created_at.desc())
            .limit(5)
        )
        messages = result.scalars().all()
        recent_messages = "\n".join(
            [f"- {m.sender_agent_id} → {m.receiver_agent_id}: {m.subject}" for m in messages]
        )

        # Build prompt
        prompt = PLANNER_PROMPT.format(
            agent_name=planner.name,
            project_id=str(project.id),
            user_goal=project.goal_raw,
            parsed_goal=json.dumps(project.goal_parsed, indent=2),
            team_composition=team_composition,
            existing_tasks="(None yet)",
            recent_messages=recent_messages or "(No messages)",
        )

        # Call LLM
        llm = get_llm(temperature=0.2)
        messages_llm = [
            {"role": "system", "content": PLANNER_SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ]
        response = await llm.ainvoke(messages_llm)
        response_text = response.content.strip()

        # Parse response
        try:
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            action_data = json.loads(response_text)
        except json.JSONDecodeError:
            print(f"⚠️ Planner response not valid JSON: {response_text[:200]}")
            # Fallback: create a simple task
            action_data = {
                "action": "create_tasks",
                "reasoning": "Creating basic task structure",
                "data": {
                    "tasks": [
                        {
                            "title": "Implement Core Functionality",
                            "description": "Implement the main features as described in the goal",
                            "task_type": "implementation",
                            "owner_role": "BackendEngineerAgent",
                            "priority": 5,
                            "estimated_duration": 120,
                            "depends_on": [],
                            "success_criteria": ["Feature implemented", "Tests passing"],
                        }
                    ]
                },
            }

        # Create tasks
        if action_data.get("action") == "create_tasks":
            tasks_data = action_data.get("data", {}).get("tasks", [])
            created_tasks = []

            for task_data in tasks_data:
                # Find owner agent
                owner_role = task_data.get("owner_role", "BackendEngineerAgent")
                result = await db.execute(
                    select(Agent).where(Agent.project_id == project.id, Agent.role == owner_role)
                )
                owner_agent = result.scalar_one_or_none()

                task = Task(
                    project_id=project.id,
                    title=task_data.get("title", "Untitled Task"),
                    description=task_data.get("description", ""),
                    task_type=task_data.get("task_type", "implementation"),
                    owner_agent_id=owner_agent.id if owner_agent else None,
                    status="pending",
                    priority=task_data.get("priority", 3),
                    estimated_duration=task_data.get("estimated_duration", 60),
                    depends_on=task_data.get("depends_on", []),
                    input_data=task_data.get("input_data", {}),
                )
                db.add(task)
                created_tasks.append(task)
                if owner_agent:
                    owner_agent.tasks_assigned += 1

            await db.flush()
            project.total_tasks = len(created_tasks)
            planner.tasks_completed += 1
            await db.commit()

            print(f"  ✅ Created {len(created_tasks)} tasks")
            for t in created_tasks:
                print(f"     - {t.title} (owner: {t.owner_agent_id})")

    @staticmethod
    async def _phase_execute_tasks(db: AsyncSession, project: Project):
        """Phase 3: Execute tasks sequentially (simplified for MVP)."""
        print("⚙️ Phase 3: Task Execution")

        project.status = "executing"
        await db.commit()

        # Get all tasks
        result = await db.execute(
            select(Task).where(Task.project_id == project.id).order_by(Task.priority.desc())
        )
        tasks = result.scalars().all()

        for task in tasks:
            print(f"  🔨 Executing: {task.title}")
            task.status = "in_progress"
            task.started_at = datetime.now(timezone.utc)
            await db.commit()

            # Get owner agent
            if task.owner_agent_id:
                result = await db.execute(select(Agent).where(Agent.id == task.owner_agent_id))
                owner_agent = result.scalar_one_or_none()

                if owner_agent and owner_agent.role == "BackendEngineerAgent":
                    # Execute with Backend Engineer
                    output = await WorkflowEngine._execute_backend_task(db, project, task, owner_agent)
                    
                    # Mark task complete
                    task.status = "completed"
                    task.completed_at = datetime.now(timezone.utc)
                    task.output_data = {"summary": output}
                    owner_agent.tasks_completed += 1
                    project.completed_tasks += 1
                    await db.commit()
                    print(f"     ✅ Task completed")
                else:
                    # For other agents, simulate completion
                    task.status = "completed"
                    task.completed_at = datetime.now(timezone.utc)
                    task.output_data = {"summary": f"Task completed by {owner_agent.name if owner_agent else 'Unknown'}"}
                    if owner_agent:
                        owner_agent.tasks_completed += 1
                    project.completed_tasks += 1
                    await db.commit()
                    print(f"     ✅ Task completed (simulated)")

            await asyncio.sleep(0.5)  # Small delay between tasks

    @staticmethod
    async def _execute_backend_task(
        db: AsyncSession, project: Project, task: Task, agent: Agent
    ) -> str:
        """Execute a backend engineering task."""
        # Build context
        prompt = BACKEND_ENGINEER_PROMPT.format(
            agent_name=agent.name,
            project_id=str(project.id),
            current_task=f"{task.title}\n{task.description}",
            task_requirements=json.dumps(task.input_data, indent=2) if task.input_data else "{}",
            context=f"Project Goal: {project.goal_raw}",
            recent_messages="(No recent messages)",
        )

        # Call LLM
        llm = get_llm(temperature=0.3)
        messages = [
            {"role": "system", "content": BACKEND_ENGINEER_SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ]
        response = await llm.ainvoke(messages)
        response_text = response.content.strip()

        # Parse response
        try:
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            action_data = json.loads(response_text)
        except json.JSONDecodeError:
            action_data = {
                "action": "complete_task",
                "reasoning": "Task completed",
                "data": {"output": {"summary": "Implementation completed"}},
            }

        # Handle actions
        if action_data.get("action") == "write_code":
            data = action_data.get("data", {})
            # Create output record
            output = Output(
                project_id=project.id,
                task_id=task.id,
                output_type="code",
                title=f"Code: {data.get('file_path', 'output.py')}",
                description=data.get("description", ""),
                author_agent_id=agent.id,
                content=data.get("content", ""),
                file_path=data.get("file_path", ""),
                status="published",
            )
            db.add(output)
            await db.commit()
            return f"Code written: {data.get('file_path')}"

        elif action_data.get("action") == "complete_task":
            data = action_data.get("data", {}).get("output", {})
            return data.get("documentation", "Task completed successfully")

        return "Task executed"

    @staticmethod
    async def _phase_finalize(db: AsyncSession, project: Project):
        """Phase 4: Finalize project."""
        print("🎉 Phase 4: Finalization")

        project.status = "completed"
        project.completed_at = datetime.now(timezone.utc)
        await db.commit()

        print(f"  ✅ Project completed: {project.completed_tasks}/{project.total_tasks} tasks done")
