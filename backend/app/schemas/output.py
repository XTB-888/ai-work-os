"""Output schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

from app.schemas.common import OrmBase


class OutputResponse(OrmBase):
    id: UUID
    project_id: UUID
    task_id: Optional[UUID]
    output_type: str
    title: str
    description: Optional[str]
    author_agent_id: Optional[UUID]
    reviewed_by_agent_id: Optional[UUID]
    approved_by_agent_id: Optional[UUID]
    content: Optional[str]
    file_path: Optional[str]
    file_format: Optional[str]
    version: str
    is_latest: bool
    status: str
    quality_score: Optional[Decimal]
    review_comments: Optional[str]
    created_at: datetime
