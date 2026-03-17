"""
AI Work OS – FastAPI application entry-point.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.db.base import Base
from app.db.session import async_engine

# Import all models so they are registered with Base.metadata
import app.models  # noqa

# Import routers
from app.api.v1.auth import router as auth_router
from app.api.v1.projects import router as projects_router
from app.api.v1.project_data import router as project_data_router
from app.api.v1.websocket import router as ws_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# ── Lifespan: create tables on startup ───────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Work OS …")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ready.")
    yield
    logger.info("Shutting down AI Work OS …")


# ── App factory ──────────────────────────────────────────────────
app = FastAPI(
    title="AI Work OS API",
    description="AI Work Operating System – Transform Goals into Results with AI Agent Teams",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ─────────────────────────────────────────────
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(projects_router, prefix="/api/v1/projects")
app.include_router(project_data_router, prefix="/api/v1/projects")
app.include_router(ws_router, prefix="/ws")


@app.get("/", tags=["health"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}
