"""Project model."""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Project(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "projects"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    task_type = Column(
        String(50), nullable=False
    )  # research | product_design | software_development | business_analysis | startup_planning
    status = Column(
        String(50), default="draft"
    )  # draft | planning | executing | reviewing | completed | failed | cancelled
    priority = Column(Integer, default=0)

    # Goal
    goal_raw = Column(Text, nullable=False)
    goal_parsed = Column(JSONB, default=dict)

    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    estimated_duration = Column(Integer)  # minutes
    actual_duration = Column(Integer)

    # Stats
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    total_decisions = Column(Integer, default=0)

    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    user = relationship("User", back_populates="projects")
    agents = relationship("Agent", back_populates="project", lazy="selectin", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", lazy="selectin", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="project", lazy="selectin", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="project", lazy="selectin", cascade="all, delete-orphan")
    outputs = relationship("Output", back_populates="project", lazy="selectin", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="project", lazy="selectin", cascade="all, delete-orphan")
