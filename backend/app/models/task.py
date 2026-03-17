"""Task model."""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Task(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tasks"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(500), nullable=False)
    description = Column(Text)
    task_type = Column(String(100), nullable=False)

    # Ownership (accountability)
    owner_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))
    reviewer_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))
    approver_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))

    # Status
    status = Column(String(50), default="pending")  # pending | in_progress | blocked | review | approved | completed | failed
    priority = Column(Integer, default=0)

    # Dependencies (stored as list of task UUIDs)
    depends_on = Column(JSONB, default=list)

    # Timing
    estimated_duration = Column(Integer)
    actual_duration = Column(Integer)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # I/O
    input_data = Column(JSONB, default=dict)
    output_data = Column(JSONB, default=dict)

    # Execution
    execution_logs = Column(JSONB, default=list)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    project = relationship("Project", back_populates="tasks")
    owner_agent = relationship("Agent", foreign_keys=[owner_agent_id])
    reviewer_agent = relationship("Agent", foreign_keys=[reviewer_agent_id])
    approver_agent = relationship("Agent", foreign_keys=[approver_agent_id])


class TaskDependency(Base, UUIDMixin):
    __tablename__ = "task_dependencies"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    predecessor_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    successor_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    dependency_type = Column(String(50), default="finish_to_start")
