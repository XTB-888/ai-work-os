"""Task schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from app.schemas.common import OrmBase


class TaskResponse(OrmBase):
    id: UUID
    project_id: UUID
    title: str
    description: Optional[str]
    task_type: str
    owner_agent_id: Optional[UUID]
    reviewer_agent_id: Optional[UUID]
    approver_agent_id: Optional[UUID]
    status: str
    priority: int
    depends_on: List[str]
    estimated_duration: Optional[int]
    actual_duration: Optional[int]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
