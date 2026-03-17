"""
Application configuration with validation.
"""
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "AI Work OS"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://admin:aiworkos_secret_2026@localhost:5432/ai_work_os"
    DATABASE_URL_SYNC: str = "postgresql://admin:aiworkos_secret_2026@localhost:5432/ai_work_os"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # ── Redis ────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50

    # ── JWT ──────────────────────────────────────────────────────
    JWT_SECRET: str = "aiworkos-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ── LLM ──────────────────────────────────────────────────────
    OPENAI_API_KEY: str = "sk-placeholder"
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = Field(default=0.3, ge=0.0, le=2.0)
    OPENAI_MAX_TOKENS: int = Field(default=4000, ge=1, le=128000)
    OPENAI_TIMEOUT: int = 60  # seconds

    # ── CORS ─────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # ── Rate Limiting ────────────────────────────────────────────
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100

    # ── Logging ──────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ── Agent Workspace ──────────────────────────────────────────
    AGENT_WORKSPACE_ROOT: str = "/tmp/aiworkos"

    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, v):
        """Warn if using placeholder API key."""
        if v == "sk-placeholder":
            import warnings
            warnings.warn(
                "Using placeholder OpenAI API key. "
                "Please set OPENAI_API_KEY environment variable."
            )
        return v

    @validator("JWT_SECRET")
    def validate_jwt_secret(cls, v, values):
        """Warn if using default secret in production."""
        if values.get("ENVIRONMENT") == "production" and "change-in-production" in v:
            import warnings
            warnings.warn(
                "Using default JWT secret in production! "
                "Please set a secure JWT_SECRET environment variable."
            )
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
