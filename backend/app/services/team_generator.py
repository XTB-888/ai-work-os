"""
Team Generator – creates the right set of Agent rows for a project.
"""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.agent import Agent, AgentRelationship

# ── Agent template library ───────────────────────────────────────
TEAM_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "software_development": [
        {
            "role": "CoordinatorAgent",
            "name": "Coordinator",
            "description": "Oversees the entire project, delegates tasks, monitors progress, resolves conflicts.",
            "agent_type": "coordinator",
            "capabilities": ["team_management", "decision_making", "progress_monitoring"],
            "tools": ["send_message", "make_decision", "assign_task"],
            "authority_level": 5,
            "can_approve": True,
            "can_delegate": True,
        },
        {
            "role": "PlannerAgent",
            "name": "Planner",
            "description": "Breaks down goals into tasks, analyses dependencies, creates execution plan.",
            "agent_type": "planner",
            "capabilities": ["task_planning", "dependency_analysis", "scheduling"],
            "tools": ["create_task", "estimate_duration", "send_message"],
            "authority_level": 4,
            "can_approve": False,
            "can_delegate": True,
        },
        {
            "role": "ArchitectAgent",
            "name": "Architect",
            "description": "Designs system architecture, selects technologies, defines APIs.",
            "agent_type": "specialist",
            "capabilities": ["system_design", "api_design", "technology_selection"],
            "tools": ["web_search", "code_executor", "file_manager", "send_message"],
            "authority_level": 3,
            "can_approve": True,
            "can_delegate": False,
        },
        {
            "role": "BackendEngineerAgent",
            "name": "Backend Engineer",
            "description": "Implements backend services, writes clean code and tests.",
            "agent_type": "specialist",
            "capabilities": ["backend_development", "api_implementation", "testing"],
            "tools": ["code_executor", "file_manager", "web_search", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
        {
            "role": "QAAgent",
            "name": "QA Engineer",
            "description": "Reviews code, runs tests, verifies quality standards.",
            "agent_type": "specialist",
            "capabilities": ["code_review", "testing", "quality_assurance"],
            "tools": ["code_executor", "file_manager", "send_message"],
            "authority_level": 3,
            "can_approve": True,
            "can_delegate": False,
        },
    ],
    "research": [
        {
            "role": "CoordinatorAgent",
            "name": "Coordinator",
            "description": "Oversees the research project.",
            "agent_type": "coordinator",
            "capabilities": ["team_management", "decision_making"],
            "tools": ["send_message", "make_decision", "assign_task"],
            "authority_level": 5,
            "can_approve": True,
            "can_delegate": True,
        },
        {
            "role": "PlannerAgent",
            "name": "Planner",
            "description": "Plans research phases and milestones.",
            "agent_type": "planner",
            "capabilities": ["task_planning", "scheduling"],
            "tools": ["create_task", "send_message"],
            "authority_level": 4,
            "can_approve": False,
            "can_delegate": True,
        },
        {
            "role": "ResearchAgent",
            "name": "Researcher",
            "description": "Gathers and analyses information from multiple sources.",
            "agent_type": "specialist",
            "capabilities": ["information_gathering", "data_analysis", "synthesis"],
            "tools": ["web_search", "file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
        {
            "role": "WriterAgent",
            "name": "Writer",
            "description": "Produces research reports and documentation.",
            "agent_type": "specialist",
            "capabilities": ["technical_writing", "report_generation"],
            "tools": ["file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
        {
            "role": "ReviewerAgent",
            "name": "Reviewer",
            "description": "Reviews research quality and accuracy.",
            "agent_type": "specialist",
            "capabilities": ["quality_review", "fact_checking"],
            "tools": ["web_search", "send_message"],
            "authority_level": 3,
            "can_approve": True,
            "can_delegate": False,
        },
    ],
    "product_design": [
        {
            "role": "CoordinatorAgent",
            "name": "Coordinator",
            "description": "Oversees the product design process.",
            "agent_type": "coordinator",
            "capabilities": ["team_management", "decision_making"],
            "tools": ["send_message", "make_decision", "assign_task"],
            "authority_level": 5,
            "can_approve": True,
            "can_delegate": True,
        },
        {
            "role": "PlannerAgent",
            "name": "Planner",
            "description": "Plans design phases.",
            "agent_type": "planner",
            "capabilities": ["task_planning", "scheduling"],
            "tools": ["create_task", "send_message"],
            "authority_level": 4,
            "can_approve": False,
            "can_delegate": True,
        },
        {
            "role": "ProductManagerAgent",
            "name": "Product Manager",
            "description": "Defines product requirements and user stories.",
            "agent_type": "specialist",
            "capabilities": ["requirement_analysis", "user_story_writing", "market_analysis"],
            "tools": ["web_search", "file_manager", "send_message"],
            "authority_level": 3,
            "can_approve": True,
            "can_delegate": False,
        },
        {
            "role": "DesignerAgent",
            "name": "UX Designer",
            "description": "Creates wireframes, user flows, and design specifications.",
            "agent_type": "specialist",
            "capabilities": ["ux_design", "wireframing", "user_flow_design"],
            "tools": ["file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
    ],
    "business_analysis": [
        {
            "role": "CoordinatorAgent",
            "name": "Coordinator",
            "description": "Oversees the business analysis.",
            "agent_type": "coordinator",
            "capabilities": ["team_management", "decision_making"],
            "tools": ["send_message", "make_decision", "assign_task"],
            "authority_level": 5,
            "can_approve": True,
            "can_delegate": True,
        },
        {
            "role": "PlannerAgent",
            "name": "Planner",
            "description": "Plans analysis phases.",
            "agent_type": "planner",
            "capabilities": ["task_planning"],
            "tools": ["create_task", "send_message"],
            "authority_level": 4,
            "can_approve": False,
            "can_delegate": True,
        },
        {
            "role": "MarketAnalystAgent",
            "name": "Market Analyst",
            "description": "Analyses market trends and opportunities.",
            "agent_type": "specialist",
            "capabilities": ["market_analysis", "data_analysis"],
            "tools": ["web_search", "file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
        {
            "role": "StrategyAgent",
            "name": "Strategist",
            "description": "Develops strategic recommendations.",
            "agent_type": "specialist",
            "capabilities": ["strategy_development", "competitive_analysis"],
            "tools": ["web_search", "file_manager", "send_message"],
            "authority_level": 3,
            "can_approve": True,
            "can_delegate": False,
        },
    ],
    "startup_planning": [
        {
            "role": "CoordinatorAgent",
            "name": "Coordinator",
            "description": "Oversees the startup planning process.",
            "agent_type": "coordinator",
            "capabilities": ["team_management", "decision_making"],
            "tools": ["send_message", "make_decision", "assign_task"],
            "authority_level": 5,
            "can_approve": True,
            "can_delegate": True,
        },
        {
            "role": "PlannerAgent",
            "name": "Planner",
            "description": "Plans startup phases.",
            "agent_type": "planner",
            "capabilities": ["task_planning"],
            "tools": ["create_task", "send_message"],
            "authority_level": 4,
            "can_approve": False,
            "can_delegate": True,
        },
        {
            "role": "MarketResearchAgent",
            "name": "Market Researcher",
            "description": "Researches market opportunity and competition.",
            "agent_type": "specialist",
            "capabilities": ["market_research", "competitive_analysis"],
            "tools": ["web_search", "file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
        {
            "role": "FinanceAgent",
            "name": "Finance Analyst",
            "description": "Creates financial models and projections.",
            "agent_type": "specialist",
            "capabilities": ["financial_modeling", "budgeting"],
            "tools": ["code_executor", "file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
        {
            "role": "WriterAgent",
            "name": "Business Writer",
            "description": "Writes business plan and pitch deck content.",
            "agent_type": "specialist",
            "capabilities": ["business_writing", "pitch_creation"],
            "tools": ["file_manager", "send_message"],
            "authority_level": 2,
            "can_approve": False,
            "can_delegate": False,
        },
    ],
}


class TeamGeneratorService:
    @staticmethod
    async def generate(db: AsyncSession, project: Project) -> List[Agent]:
        """Create Agent rows for the project based on its task_type."""
        task_type = project.task_type
        templates = TEAM_TEMPLATES.get(task_type, TEAM_TEMPLATES["software_development"])

        agents: List[Agent] = []
        for tpl in templates:
            agent = Agent(
                project_id=project.id,
                role=tpl["role"],
                name=tpl["name"],
                description=tpl["description"],
                agent_type=tpl["agent_type"],
                capabilities=tpl["capabilities"],
                tools=tpl["tools"],
                authority_level=tpl["authority_level"],
                can_approve=tpl["can_approve"],
                can_delegate=tpl["can_delegate"],
                status="idle",
            )
            db.add(agent)
            agents.append(agent)

        await db.flush()

        # Build hierarchy relationships
        coordinator = next((a for a in agents if a.agent_type == "coordinator"), None)
        planner = next((a for a in agents if a.agent_type == "planner"), None)
        specialists = [a for a in agents if a.agent_type == "specialist"]

        if coordinator and planner:
            db.add(AgentRelationship(
                project_id=project.id,
                parent_agent_id=coordinator.id,
                child_agent_id=planner.id,
                relationship_type="manages",
            ))
        if planner:
            for spec in specialists:
                db.add(AgentRelationship(
                    project_id=project.id,
                    parent_agent_id=planner.id,
                    child_agent_id=spec.id,
                    relationship_type="manages",
                ))

        project.total_tasks = 0
        return agents
