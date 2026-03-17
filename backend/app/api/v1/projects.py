"""
Project CRUD + goal submission + execution trigger.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectBrief, ProjectDetail
from app.core.exceptions import NotFoundException
from app.services.goal_parser import GoalParserService
from app.services.team_generator import TeamGeneratorService
from app.services.workflow_engine import WorkflowEngine

router = APIRouter(tags=["projects"])


@router.post("", response_model=ProjectDetail, status_code=201)
async def create_project(
    body: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a project, parse the goal, generate team & workflow, then start execution."""
    # 1. Parse goal
    parsed = await GoalParserService.parse(body.goal)

    # 2. Persist project
    project = Project(
        user_id=user.id,
        name=body.name,
        description=body.description,
        task_type=parsed["task_type"],
        goal_raw=body.goal,
        goal_parsed=parsed,
        status="planning",
    )
    db.add(project)
    await db.flush()

    # 3. Generate team
    await TeamGeneratorService.generate(db, project)
    await db.flush()

    # 4. Kick off workflow in background
    background_tasks.add_task(WorkflowEngine.run, str(project.id))

    return ProjectDetail.model_validate(project)


@router.get("", response_model=List[ProjectBrief])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project)
        .where(Project.user_id == user.id)
        .order_by(Project.created_at.desc())
    )
    return [ProjectBrief.model_validate(p) for p in result.scalars().all()]


@router.get("/{project_id}", response_model=ProjectDetail)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundException("Project not found")
    return ProjectDetail.model_validate(project)
