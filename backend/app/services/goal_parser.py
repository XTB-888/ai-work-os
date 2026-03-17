"""
Goal Parser – uses LLM to analyse a natural-language goal and extract structured data.
"""
import json
from typing import Dict, Any

from app.llm.provider import get_llm


GOAL_PARSE_PROMPT = """You are the Goal Parser of an AI Work Operating System.
Analyse the user's goal and return a JSON object with these fields:

{{
  "task_type": one of ["research", "product_design", "software_development", "business_analysis", "startup_planning"],
  "domain": short domain label,
  "title": concise project title,
  "requirements": {{
    "tech_stack": [...],
    "features": [...],
    "constraints": {{}}
  }},
  "success_criteria": [...],
  "estimated_complexity": "low" | "medium" | "high"
}}

Rules:
- Return ONLY valid JSON, no markdown fences.
- Infer missing details from context.

User Goal:
{goal}
"""


class GoalParserService:
    @staticmethod
    async def parse(goal: str) -> Dict[str, Any]:
        llm = get_llm(temperature=0.2)
        prompt = GOAL_PARSE_PROMPT.format(goal=goal)
        response = await llm.ainvoke(prompt)
        text = response.content.strip()

        # strip markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            # fallback
            parsed = {
                "task_type": "software_development",
                "domain": "general",
                "title": goal[:80],
                "requirements": {"tech_stack": [], "features": [], "constraints": {}},
                "success_criteria": [goal],
                "estimated_complexity": "medium",
            }
        return parsed
