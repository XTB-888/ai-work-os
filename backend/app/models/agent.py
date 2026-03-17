"""Agent model."""
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Agent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agents"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    # Identity
    role = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    agent_type = Column(String(50), nullable=False)  # coordinator | planner | specialist

    # Capabilities
    capabilities = Column(JSONB, default=list)
    tools = Column(JSONB, default=list)

    # LLM config
    llm_provider = Column(String(50), default="openai")
    llm_model = Column(String(100))
    llm_config = Column(JSONB, default=dict)

    # Authority
    authority_level = Column(Integer, default=1)  # 1-5
    can_approve = Column(Boolean, default=False)
    can_delegate = Column(Boolean, default=False)

    # Status
    status = Column(String(50), default="idle")  # idle | working | waiting | completed | error
    current_task_id = Column(UUID(as_uuid=True))

    # Stats
    tasks_assigned = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    decisions_made = Column(Integer, default=0)

    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    project = relationship("Project", back_populates="agents")


class AgentRelationship(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_relationships"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    parent_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"))
    child_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"))
    relationship_type = Column(String(50), nullable=False)  # manages | reports_to | collaborates_with
