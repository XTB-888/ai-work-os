"""Agent schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from app.schemas.common import OrmBase


class AgentResponse(OrmBase):
    id: UUID
    project_id: UUID
    role: str
    name: str
    description: Optional[str]
    agent_type: str
    capabilities: List[str]
    tools: List[str]
    authority_level: int
    can_approve: bool
    can_delegate: bool
    status: str
    tasks_assigned: int
    tasks_completed: int
    messages_sent: int
    decisions_made: int
    created_at: datetime
