"""
Base class for all AI agents.
"""
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.provider import get_llm
from app.models.message import Message
from app.models.decision import Decision

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base for every agent in the system."""

    role: str = "BaseAgent"
    agent_type: str = "specialist"

    def __init__(self, agent_id: UUID, project_id: UUID, db: AsyncSession):
        self.agent_id = agent_id
        self.project_id = project_id
        self.db = db
        self.llm = get_llm()

    # ── subclass must implement ──────────────────────────────────
    @abstractmethod
    def build_prompt(self, context: Dict[str, Any]) -> str:
        ...

    # ── shared helpers ───────────────────────────────────────────
    async def invoke_llm(self, prompt: str) -> Dict[str, Any]:
        """Call LLM, parse JSON response, return dict."""
        resp = await self.llm.ainvoke(prompt)
        text = resp.content.strip()
        # strip markdown fences
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("LLM returned non-JSON: %s", text[:200])
            return {"thought": text, "error": "non-json response"}

    async def send_message(
        self,
        receiver_agent_id: UUID,
        message_type: str,
        subject: str,
        content: str,
        task_id: Optional[UUID] = None,
    ) -> Message:
        msg = Message(
            project_id=self.project_id,
            task_id=task_id,
            sender_agent_id=self.agent_id,
            receiver_agent_id=receiver_agent_id,
            message_type=message_type,
            subject=subject,
            content=content,
        )
        self.db.add(msg)
        await self.db.flush()
        return msg

    async def record_decision(
        self,
        title: str,
        description: str,
        decision_type: str,
        chosen_option: Dict,
        rationale: str,
        task_id: Optional[UUID] = None,
    ) -> Decision:
        dec = Decision(
            project_id=self.project_id,
            task_id=task_id,
            decision_type=decision_type,
            title=title,
            description=description,
            made_by_agent_id=self.agent_id,
            chosen_option=chosen_option,
            rationale=rationale,
            status="approved",
        )
        self.db.add(dec)
        await self.db.flush()
        return dec
