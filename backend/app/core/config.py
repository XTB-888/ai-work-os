"""
Application configuration with validation.
"""
from typing import List, Optional, Literal
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "AI Work OS"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # ── LLM Provider ─────────────────────────────────────────────
    LLM_PROVIDER: Literal["openai", "dashscope"] = "dashscope"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = "sk-placeholder"
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = Field(default=0.3, ge=0.0, le=2.0)
    OPENAI_MAX_TOKENS: int = Field(default=4000, ge=1, le=128000)
    
    # Alibaba Cloud Bailian (DashScope) Configuration
    DASHSCOPE_API_KEY: str = "sk-placeholder"
    DASHSCOPE_MODEL: str = "qwen-max"
    DASHSCOPE_TEMPERATURE: float = Field(default=0.3, ge=0.0, le=2.0)
    DASHSCOPE_MAX_TOKENS: int = Field(default=4000, ge=1, le=8000)

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://admin:aiworkos_secret_2026@localhost:5433/ai_work_os"
    DATABASE_URL_SYNC: str = "postgresql://admin:aiworkos_secret_2026@localhost:5433/ai_work_os"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # ── Redis ────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6380/0"
    REDIS_MAX_CONNECTIONS: int = 50

    # ── JWT ──────────────────────────────────────────────────────
    JWT_SECRET: str = "aiworkos-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ── CORS ─────────────────────────────────────────────────────
    ALLOWED_ORIGINS: str = "http://localhost:3001,http://127.0.0.1:3001"
    
    @property
    def ALLOWED_ORIGINS_LIST(self) -> List[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # ── Rate Limiting ────────────────────────────────────────────
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100

    # ── Logging ──────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ── Agent Workspace ──────────────────────────────────────────
    AGENT_WORKSPACE_ROOT: str = "/tmp/aiworkos"

    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, v, values):
        """Warn if using placeholder API key when OpenAI is selected."""
        if values.get("LLM_PROVIDER") == "openai" and v == "sk-placeholder":
            import warnings
            warnings.warn(
                "Using placeholder OpenAI API key. "
                "Please set OPENAI_API_KEY environment variable."
            )
        return v
    
    @validator("DASHSCOPE_API_KEY")
    def validate_dashscope_key(cls, v, values):
        """Warn if using placeholder API key when DashScope is selected."""
        if values.get("LLM_PROVIDER") == "dashscope" and v == "sk-placeholder":
            import warnings
            warnings.warn(
                "Using placeholder DashScope API key. "
                "Please set DASHSCOPE_API_KEY environment variable."
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
