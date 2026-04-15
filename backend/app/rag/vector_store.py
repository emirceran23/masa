"""pgvector CRUD — index embeddings and search by cosine similarity."""

from __future__ import annotations

import logging
import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.rag.embeddings import embed_text

logger = logging.getLogger(__name__)


# ── Indexing ─────────────────────────────────────────────

async def index_clause(db: AsyncSession, clause_id: uuid.UUID, clause_text: str) -> None:
    """Embed clause_text and upsert into clause_embeddings."""
    vector = await embed_text(clause_text)
    vector_str = _to_pg_vector(vector)

    await db.execute(
        text("""
            INSERT INTO clause_embeddings (clause_id, embedding)
            VALUES (:clause_id, :embedding)
            ON CONFLICT (clause_id) DO UPDATE SET embedding = EXCLUDED.embedding
        """),
        {"clause_id": str(clause_id), "embedding": vector_str},
    )
    logger.debug("Indexed embedding for clause %s", clause_id)


async def index_rule(db: AsyncSession, rule_id: uuid.UUID, rule_text: str) -> None:
    """Embed rule_text and upsert into playbook_rule_embeddings."""
    vector = await embed_text(rule_text)
    vector_str = _to_pg_vector(vector)

    await db.execute(
        text("""
            INSERT INTO playbook_rule_embeddings (rule_id, embedding)
            VALUES (:rule_id, :embedding)
            ON CONFLICT (rule_id) DO UPDATE SET embedding = EXCLUDED.embedding
        """),
        {"rule_id": str(rule_id), "embedding": vector_str},
    )
    logger.debug("Indexed embedding for rule %s", rule_id)


# ── Search ───────────────────────────────────────────────

async def search_similar_rules(
    db: AsyncSession,
    query_text: str,
    playbook_id: uuid.UUID | None = None,
    limit: int = 5,
) -> list[dict]:
    """Return the top-N playbook rules closest to query_text (cosine distance).

    Each result dict has keys: rule_id, playbook_id, rule_type, content,
    threshold_value, distance.
    """
    vector = await embed_text(query_text)
    vector_str = _to_pg_vector(vector)

    if playbook_id:
        stmt = text("""
            SELECT
                pr.id           AS rule_id,
                pr.playbook_id  AS playbook_id,
                pr.rule_type    AS rule_type,
                pr.content      AS content,
                pr.threshold_value AS threshold_value,
                pre.embedding <=> CAST(:embedding AS vector) AS distance
            FROM playbook_rule_embeddings pre
            JOIN playbook_rules pr ON pr.id = pre.rule_id
            WHERE pr.playbook_id = :playbook_id
            ORDER BY distance ASC
            LIMIT :limit
        """)
        params = {
            "embedding": vector_str,
            "playbook_id": str(playbook_id),
            "limit": limit,
        }
    else:
        stmt = text("""
            SELECT
                pr.id           AS rule_id,
                pr.playbook_id  AS playbook_id,
                pr.rule_type    AS rule_type,
                pr.content      AS content,
                pr.threshold_value AS threshold_value,
                pre.embedding <=> CAST(:embedding AS vector) AS distance
            FROM playbook_rule_embeddings pre
            JOIN playbook_rules pr ON pr.id = pre.rule_id
            ORDER BY distance ASC
            LIMIT :limit
        """)
        params = {"embedding": vector_str, "limit": limit}

    rows = (await db.execute(stmt, params)).mappings().all()
    return [dict(row) for row in rows]


# ── Internal helper ───────────────────────────────────────

def _to_pg_vector(vector: list[float]) -> str:
    """Convert a Python float list to the pgvector literal format '[1.0,2.0,...]'."""
    return "[" + ",".join(str(v) for v in vector) + "]"
