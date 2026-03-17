"""
AI Work OS - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.api.v1 import auth, projects, project_data, websocket

# ── Create FastAPI app ───────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="AI Work Operating System - Transform Goals into Results with AI Agent Teams",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health check ─────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "environment": settings.ENVIRONMENT}

# ── API Routes ───────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(project_data.router, prefix="/api/v1/projects", tags=["project-data"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

# ── Startup/Shutdown ─────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.APP_NAME} starting...")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print(f"   Docs: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    print(f"👋 {settings.APP_NAME} shutting down...")
