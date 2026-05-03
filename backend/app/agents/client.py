"""Shared AsyncOpenAI client factory.

Reads OPENAI_API_KEY and (optionally) OPENAI_BASE_URL from settings.
Setting OPENAI_BASE_URL to https://openrouter.ai/api/v1 routes all
requests through OpenRouter while keeping the rest of the codebase
unchanged (OpenRouter is 100% OpenAI-API-compatible).
"""

from __future__ import annotations

from openai import AsyncOpenAI

from app.config import settings

_client: AsyncOpenAI | None = None


def get_openai_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        kwargs: dict = {"api_key": settings.OPENAI_API_KEY}
        if settings.OPENAI_BASE_URL:
            kwargs["base_url"] = settings.OPENAI_BASE_URL
        _client = AsyncOpenAI(**kwargs)
    return _client
