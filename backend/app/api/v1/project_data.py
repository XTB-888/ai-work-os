"""
Agent, Task, Message, Decision, Output read-only endpoints.
These are populated by the workflow engine; the API exposes them for the frontend.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.agent import Agent
from app.models.task import Task
from app.models.message import Message
from app.models.decision import Decision
from app.models.output import Output
from app.schemas.agent import AgentResponse
from app.schemas.task import TaskResponse
from app.schemas.message import MessageResponse
from app.schemas.decision import DecisionResponse
from app.schemas.output import OutputResponse
from app.core.exceptions import NotFoundException

router = APIRouter(tags=["project-data"])


# ── Agents ───────────────────────────────────────────────────────
@router.get("/{project_id}/agents", response_model=List[AgentResponse])
async def list_agents(project_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Agent).where(Agent.project_id == project_id))
    return [AgentResponse.model_validate(a) for a in result.scalars().all()]


# ── Tasks ────────────────────────────────────────────────────────
@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(project_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Task).where(Task.project_id == project_id).order_by(Task.created_at)
    )
    return [TaskResponse.model_validate(t) for t in result.scalars().all()]


# ── Messages ─────────────────────────────────────────────────────
@router.get("/{project_id}/messages", response_model=List[MessageResponse])
async def list_messages(project_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Message).where(Message.project_id == project_id).order_by(Message.created_at)
    )
    return [MessageResponse.model_validate(m) for m in result.scalars().all()]


# ── Decisions ────────────────────────────────────────────────────
@router.get("/{project_id}/decisions", response_model=List[DecisionResponse])
async def list_decisions(project_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Decision).where(Decision.project_id == project_id).order_by(Decision.created_at)
    )
    return [DecisionResponse.model_validate(d) for d in result.scalars().all()]


# ── Outputs ──────────────────────────────────────────────────────
@router.get("/{project_id}/outputs", response_model=List[OutputResponse])
async def list_outputs(project_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Output).where(Output.project_id == project_id).order_by(Output.created_at)
    )
    return [OutputResponse.model_validate(o) for o in result.scalars().all()]
