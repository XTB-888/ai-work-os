"""Shared / common schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


class OrmBase(BaseModel):
    model_config = {"from_attributes": True}


class IDTimestamp(OrmBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None
