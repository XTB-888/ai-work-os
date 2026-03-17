"""User model."""
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(512))
    role = Column(String(50), default="user")  # user | admin
    is_active = Column(Boolean, default=True)
    metadata_ = Column("metadata", JSONB, default=dict)

    # relationships
    projects = relationship("Project", back_populates="user", lazy="selectin")
