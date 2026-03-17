"""Project schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field

from app.schemas.common import OrmBase


# ── Request ──────────────────────────────────────────────────────
class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    goal: str = Field(..., min_length=10, max_length=5000, description="Natural language goal")


class GoalSubmit(BaseModel):
    goal: str = Field(..., min_length=10)


# ── Response ─────────────────────────────────────────────────────
class ProjectBrief(OrmBase):
    id: UUID
    name: str
    task_type: str
    status: str
    goal_raw: str
    total_tasks: int
    completed_tasks: int
    created_at: datetime


class ProjectDetail(OrmBase):
    id: UUID
    name: str
    description: Optional[str]
    task_type: str
    status: str
    priority: int
    goal_raw: str
    goal_parsed: Optional[Dict[str, Any]]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    estimated_duration: Optional[int]
    actual_duration: Optional[int]
    total_tasks: int
    completed_tasks: int
    total_messages: int
    total_decisions: int
    created_at: datetime
    updated_at: datetime
