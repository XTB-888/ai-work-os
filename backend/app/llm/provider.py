"""
LLM Provider abstraction – supports OpenAI, Anthropic, local models, etc.
"""
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from app.core import settings


def get_llm(
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> BaseChatModel:
    """
    Returns a configured LLM instance.
    Currently supports OpenAI; can be extended to Anthropic, local models, etc.
    """
    return ChatOpenAI(
        model=model or settings.OPENAI_MODEL,
        temperature=temperature if temperature is not None else settings.OPENAI_TEMPERATURE,
        max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )
