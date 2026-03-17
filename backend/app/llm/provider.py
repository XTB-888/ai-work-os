"""
LLM provider abstraction layer.
Supports OpenAI out of the box; extend for Anthropic / local models.
"""
from langchain_openai import ChatOpenAI
from app.core import settings


def get_llm(
    temperature: float | None = None,
    max_tokens: int | None = None,
    model: str | None = None,
) -> ChatOpenAI:
    return ChatOpenAI(
        model=model or settings.OPENAI_MODEL,
        temperature=temperature if temperature is not None else settings.OPENAI_TEMPERATURE,
        max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )


async def llm_invoke(prompt: str, **kwargs) -> str:
    """Convenience: invoke LLM and return content string."""
    llm = get_llm(**kwargs)
    resp = await llm.ainvoke(prompt)
    return resp.content.strip()
