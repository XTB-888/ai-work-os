"""Workflow model – LangGraph workflow definitions."""
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Workflow(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "workflows"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text)
    graph_definition = Column(JSONB, nullable=False)

    status = Column(String(50), default="draft")  # draft | active | paused | completed
    current_node = Column(String(100))
    execution_state = Column(JSONB, default=dict)

    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    project = relationship("Project", back_populates="workflows")
