"""Output model – deliverables produced by agents."""
from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Output(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "outputs"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"))

    output_type = Column(String(100), nullable=False)  # document | code | design | report | data
    title = Column(String(500), nullable=False)
    description = Column(Text)

    # Accountability
    author_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))
    reviewed_by_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))
    approved_by_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))

    # Content
    content = Column(Text)
    file_path = Column(String(1000))
    file_format = Column(String(50))

    # Versioning
    version = Column(String(50), default="1.0.0")
    parent_output_id = Column(UUID(as_uuid=True), ForeignKey("outputs.id", ondelete="SET NULL"))
    is_latest = Column(Boolean, default=True)

    # Status
    status = Column(String(50), default="draft")  # draft | review | approved | published
    quality_score = Column(Numeric(3, 2))
    review_comments = Column(Text)

    published_at = Column(DateTime(timezone=True))
    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    project = relationship("Project", back_populates="outputs")
    author_agent = relationship("Agent", foreign_keys=[author_agent_id])
    reviewed_by_agent = relationship("Agent", foreign_keys=[reviewed_by_agent_id])
    approved_by_agent = relationship("Agent", foreign_keys=[approved_by_agent_id])
