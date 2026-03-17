"""Message model – agent-to-agent communication."""
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base import Base, UUIDMixin, TimestampMixin


class Message(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "messages"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"))

    sender_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))
    receiver_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"))

    message_type = Column(
        String(50), nullable=False
    )  # PROPOSAL | QUESTION | DISCUSSION | TASK_ASSIGNMENT | REPORT | DECISION | ERROR | INFO
    subject = Column(String(500))
    content = Column(Text, nullable=False)

    thread_id = Column(UUID(as_uuid=True))
    parent_message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="SET NULL"))

    attachments = Column(JSONB, default=list)
    mentioned_agents = Column(JSONB, default=list)

    is_read = Column(Boolean, default=False)
    is_important = Column(Boolean, default=False)
    requires_response = Column(Boolean, default=False)

    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    from sqlalchemy.orm import relationship
    project = relationship("Project", back_populates="messages")
    sender_agent = relationship("Agent", foreign_keys=[sender_agent_id])
    receiver_agent = relationship("Agent", foreign_keys=[receiver_agent_id])
