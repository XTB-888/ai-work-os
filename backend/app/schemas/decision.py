"""Decision schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from app.schemas.common import OrmBase


class DecisionResponse(OrmBase):
    id: UUID
    project_id: UUID
    task_id: Optional[UUID]
    decision_type: str
    title: str
    description: str
    made_by_agent_id: Optional[UUID]
    approved_by_agent_id: Optional[UUID]
    options_considered: List[Dict[str, Any]]
    chosen_option: Dict[str, Any]
    rationale: str
    impact_scope: Optional[str]
    status: str
    created_at: datetime
