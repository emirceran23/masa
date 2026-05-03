"""OpenAI embedding helper — converts text to 1536-dim vectors."""

from __future__ import annotations

import logging

from app.agents.client import get_openai_client
from app.config import settings

logger = logging.getLogger(__name__)


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return an embedding vector for each input string.

    Sends all texts in a single API call (OpenAI supports batch input).
    Raises on API error — callers should handle and log.
    """
    if not texts:
        return []

    client = get_openai_client()
    response = await client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=texts,
    )

    # OpenAI returns results in the same order as the input
    vectors = [item.embedding for item in response.data]
    logger.debug("Embedded %d text(s) via %s", len(texts), settings.OPENAI_EMBEDDING_MODEL)
    return vectors


async def embed_text(text: str) -> list[float]:
    """Convenience wrapper for a single string."""
    results = await embed_texts([text])
    return results[0]
