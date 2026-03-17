"""
Unit tests for the Goal Parser service.
"""
import pytest
from app.services.goal_parser import GoalParserService


@pytest.mark.asyncio
async def test_parse_software_goal():
    """GoalParser should identify software_development tasks."""
    result = await GoalParserService.parse(
        "Build a REST API for task management with FastAPI and PostgreSQL"
    )
    assert result["task_type"] in (
        "software_development",
        "product_design",
    )
    assert "title" in result
    assert "requirements" in result


@pytest.mark.asyncio
async def test_parse_research_goal():
    result = await GoalParserService.parse(
        "Research the impact of large language models on healthcare diagnostics in 2025"
    )
    assert result["task_type"] in ("research", "business_analysis")
