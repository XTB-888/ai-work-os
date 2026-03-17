"""
LLM provider abstraction – currently wraps OpenAI; easy to add Anthropic / local.
"""
from langchain_openai import ChatOpenAI
from app.core import settings


def get_llm(
    temperature: float | None = None,
    max_tokens: int | None = None,
    model: str | None = None,
) -> ChatOpenAI:
    """Return a LangChain ChatOpenAI instance with project defaults."""
    return ChatOpenAI(
        model=model or settings.OPENAI_MODEL,
        temperature=temperature if temperature is not None else settings.OPENAI_TEMPERATURE,
        max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )
