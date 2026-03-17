"""Message schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.schemas.common import OrmBase


class MessageResponse(OrmBase):
    id: UUID
    project_id: UUID
    task_id: Optional[UUID]
    sender_agent_id: Optional[UUID]
    receiver_agent_id: Optional[UUID]
    message_type: str
    subject: Optional[str]
    content: str
    thread_id: Optional[UUID]
    is_important: bool
    requires_response: bool
    created_at: datetime
