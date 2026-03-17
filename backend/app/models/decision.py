"""Decision model – records every decision made by agents."""
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Decision(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "decisions"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"))

    decision_type = Column(String(100), nullable=False)  # technical | architectural | process | resource_allocation
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    made_by_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))
    approved_by_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))

    options_considered = Column(JSONB, default=list)
    chosen_option = Column(JSONB, nullable=False)
    rationale = Column(Text, nullable=False)

    impact_scope = Column(String(50))  # task | project | system
    affected_tasks = Column(JSONB, default=list)
    affected_agents = Column(JSONB, default=list)

    status = Column(String(50), default="proposed")  # proposed | approved | rejected | implemented | reverted

    proposed_at = Column(DateTime(timezone=True))
    approved_at = Column(DateTime(timezone=True))
    implemented_at = Column(DateTime(timezone=True))

    outcome = Column(Text)
    was_successful = Column(Boolean)

    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    project = relationship("Project", back_populates="decisions")
    made_by_agent = relationship("Agent", foreign_keys=[made_by_agent_id])
    approved_by_agent = relationship("Agent", foreign_keys=[approved_by_agent_id])
