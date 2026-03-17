"""
Coordinator Agent – the CEO of the AI team.
"""
import json
from typing import Any, Dict
from app.agents.base import BaseAgent
from app.agents.prompts.coordinator import COORDINATOR_SYSTEM, COORDINATOR_PLAN_INSTRUCTION


class CoordinatorAgent(BaseAgent):
    role = "CoordinatorAgent"
    agent_type = "coordinator"

    def build_prompt(self, context: Dict[str, Any]) -> str:
        return COORDINATOR_SYSTEM.format(
            project_name=context.get("project_name", ""),
            goal_raw=context.get("goal_raw", ""),
            goal_parsed=json.dumps(context.get("goal_parsed", {}), indent=2),
            team_summary=context.get("team_summary", ""),
            project_status=context.get("project_status", "planning"),
            recent_messages=context.get("recent_messages", "None yet"),
            instruction=context.get("instruction", COORDINATOR_PLAN_INSTRUCTION),
        )

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self.build_prompt(context)
        result = await self.invoke_llm(prompt)

        # persist any messages the coordinator wants to send
        for action in result.get("actions", []):
            if action.get("action") == "send_message":
                params = action.get("params", {})
                receiver_id = context.get("agent_id_map", {}).get(params.get("to_role"))
                if receiver_id:
                    await self.send_message(
                        receiver_agent_id=receiver_id,
                        message_type=params.get("type", "TASK_ASSIGNMENT"),
                        subject=params.get("subject", "Task from Coordinator"),
                        content=params.get("content", ""),
                    )

        return result
