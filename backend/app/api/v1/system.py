"""
System health and statistics endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from datetime import datetime, timezone

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.agent import Agent
from app.models.task import Task
from app.models.message import Message
from app.models.decision import Decision
from app.models.output import Output
from app.core import settings

router = APIRouter(tags=["system"])


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check with database and Redis status."""
    health = {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {},
    }

    # Check database
    try:
        await db.execute(text("SELECT 1"))
        health["checks"]["database"] = {"status": "ok", "type": "postgresql"}
    except Exception as e:
        health["checks"]["database"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"

    # Check Redis
    try:
        from app.core.cache import get_redis
        redis_client = await get_redis()
        await redis_client.ping()
        health["checks"]["redis"] = {"status": "ok"}
    except Exception as e:
        health["checks"]["redis"] = {"status": "error", "error": str(e)}
        health["status"] = "degraded"

    # Check LLM
    health["checks"]["llm"] = {
        "status": "configured" if settings.OPENAI_API_KEY != "sk-placeholder" else "not_configured",
        "provider": "openai",
        "model": settings.OPENAI_MODEL,
    }

    return health


@router.get("/stats")
async def system_stats(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get system statistics for the current user."""
    user_id = user.id

    # Project stats
    project_count = await db.execute(
        select(func.count(Project.id)).where(Project.user_id == user_id)
    )
    total_projects = project_count.scalar() or 0

    completed_projects = await db.execute(
        select(func.count(Project.id)).where(
            Project.user_id == user_id, Project.status == "completed"
        )
    )
    completed = completed_projects.scalar() or 0

    active_projects = await db.execute(
        select(func.count(Project.id)).where(
            Project.user_id == user_id,
            Project.status.in_(["planning", "executing", "reviewing"]),
        )
    )
    active = active_projects.scalar() or 0

    # Get user's project IDs for sub-queries
    project_ids_query = select(Project.id).where(Project.user_id == user_id)

    # Agent stats
    agent_count = await db.execute(
        select(func.count(Agent.id)).where(Agent.project_id.in_(project_ids_query))
    )
    total_agents = agent_count.scalar() or 0

    # Task stats
    task_count = await db.execute(
        select(func.count(Task.id)).where(Task.project_id.in_(project_ids_query))
    )
    total_tasks = task_count.scalar() or 0

    completed_tasks = await db.execute(
        select(func.count(Task.id)).where(
            Task.project_id.in_(project_ids_query), Task.status == "completed"
        )
    )
    total_completed_tasks = completed_tasks.scalar() or 0

    # Message stats
    message_count = await db.execute(
        select(func.count(Message.id)).where(Message.project_id.in_(project_ids_query))
    )
    total_messages = message_count.scalar() or 0

    # Decision stats
    decision_count = await db.execute(
        select(func.count(Decision.id)).where(Decision.project_id.in_(project_ids_query))
    )
    total_decisions = decision_count.scalar() or 0

    # Output stats
    output_count = await db.execute(
        select(func.count(Output.id)).where(Output.project_id.in_(project_ids_query))
    )
    total_outputs = output_count.scalar() or 0

    return {
        "user_id": str(user_id),
        "projects": {
            "total": total_projects,
            "completed": completed,
            "active": active,
            "failed": total_projects - completed - active,
        },
        "agents": {
            "total": total_agents,
        },
        "tasks": {
            "total": total_tasks,
            "completed": total_completed_tasks,
            "completion_rate": round(total_completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0,
        },
        "messages": {
            "total": total_messages,
        },
        "decisions": {
            "total": total_decisions,
        },
        "outputs": {
            "total": total_outputs,
        },
    }
