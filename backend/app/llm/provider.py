"""
LLM Provider abstraction – supports OpenAI, Alibaba Cloud Bailian (DashScope), and local models.
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
    Supports OpenAI, Alibaba Cloud Bailian (DashScope), and local models.
    """
    
    # Check if using Alibaba Cloud Bailian
    if settings.LLM_PROVIDER == "dashscope":
        from langchain_community.chat_models import ChatTongyi
        
        return ChatTongyi(
            model=model or settings.DASHSCOPE_MODEL,
            temperature=temperature if temperature is not None else settings.DASHSCOPE_TEMPERATURE,
            max_tokens=max_tokens or settings.DASHSCOPE_MAX_TOKENS,
            dashscope_api_key=settings.DASHSCOPE_API_KEY,
        )
    
    # Default to OpenAI
    return ChatOpenAI(
        model=model or settings.OPENAI_MODEL,
        temperature=temperature if temperature is not None else settings.OPENAI_TEMPERATURE,
        max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )
