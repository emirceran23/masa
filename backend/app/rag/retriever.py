"""High-level retriever — called by the Risk Agent to get relevant playbook rules."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.rag.vector_store import search_similar_rules


async def retrieve_relevant_rules(
    db: AsyncSession,
    clause_text: str,
    playbook_id: uuid.UUID | None = None,
    limit: int = 5,
) -> list[dict]:
    """Return the most semantically similar playbook rules for a given clause.

    Args:
        db:           Active async DB session.
        clause_text:  The raw clause text to compare against.
        playbook_id:  If provided, restricts search to rules within that playbook.
        limit:        Maximum number of rules to return.

    Returns:
        List of dicts with keys: rule_id, playbook_id, rule_type, content,
        threshold_value, distance.  Sorted by ascending cosine distance
        (closer = more similar).
    """
    return await search_similar_rules(
        db,
        query_text=clause_text,
        playbook_id=playbook_id,
        limit=limit,
    )
