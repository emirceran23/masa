"""Playbook service — CRUD for Playbook + PlaybookRule with vector re-indexing."""

from __future__ import annotations

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.playbook import Playbook, PlaybookRule
from app.rag.vector_store import index_rule
from app.schemas.playbook import (
    PlaybookCreateRequest,
    PlaybookDetailResponse,
    PlaybookResponse,
    PlaybookUpdateRequest,
)

logger = logging.getLogger(__name__)


# ── Helpers ───────────────────────────────────────────────

async def _get_owned_playbook(
    db: AsyncSession, playbook_id: uuid.UUID, user_id: uuid.UUID
) -> Playbook:
    stmt = (
        select(Playbook)
        .where(Playbook.id == playbook_id, Playbook.user_id == user_id)
        .options(selectinload(Playbook.rules))
    )
    pb = (await db.execute(stmt)).scalar_one_or_none()
    if not pb:
        raise NotFoundError("Playbook bulunamadı.")
    return pb


async def _index_rules(db: AsyncSession, rules: list[PlaybookRule]) -> None:
    """Fire-and-forget vector indexing — log errors, never block the caller."""
    for rule in rules:
        try:
            await index_rule(db, rule.id, rule.content)
        except Exception:
            logger.exception("Vector indexing failed for rule %s — skipping", rule.id)


# ── CRUD ─────────────────────────────────────────────────

async def create_playbook(
    db: AsyncSession,
    user_id: uuid.UUID,
    data: PlaybookCreateRequest,
) -> PlaybookDetailResponse:
    playbook = Playbook(
        user_id=user_id,
        name=data.name,
        description=data.description,
    )
    db.add(playbook)
    await db.flush()  # get playbook.id before adding rules

    rules = [
        PlaybookRule(
            playbook_id=playbook.id,
            rule_type=r.rule_type,
            content=r.content,
            threshold_value=r.threshold_value,
        )
        for r in data.rules
    ]
    db.add_all(rules)
    await db.flush()

    await _index_rules(db, rules)

    await db.refresh(playbook)
    # reload with rules relationship populated
    return await get_playbook(db, playbook.id, user_id)


async def list_playbooks(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[PlaybookResponse]:
    stmt = (
        select(Playbook)
        .where(Playbook.user_id == user_id)
        .order_by(Playbook.created_at.desc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [PlaybookResponse.model_validate(pb) for pb in rows]


async def get_playbook(
    db: AsyncSession,
    playbook_id: uuid.UUID,
    user_id: uuid.UUID,
) -> PlaybookDetailResponse:
    pb = await _get_owned_playbook(db, playbook_id, user_id)
    return PlaybookDetailResponse.model_validate(pb)


async def update_playbook(
    db: AsyncSession,
    playbook_id: uuid.UUID,
    user_id: uuid.UUID,
    data: PlaybookUpdateRequest,
) -> PlaybookDetailResponse:
    pb = await _get_owned_playbook(db, playbook_id, user_id)

    if data.name is not None:
        pb.name = data.name
    if data.description is not None:
        pb.description = data.description

    if data.rules is not None:
        # Replace all rules — cascade delete removes old rows + their embeddings
        for old_rule in list(pb.rules):
            await db.delete(old_rule)
        await db.flush()

        new_rules = [
            PlaybookRule(
                playbook_id=pb.id,
                rule_type=r.rule_type,
                content=r.content,
                threshold_value=r.threshold_value,
            )
            for r in data.rules
        ]
        db.add_all(new_rules)
        await db.flush()
        await _index_rules(db, new_rules)

    await db.flush()
    return await get_playbook(db, pb.id, user_id)


async def delete_playbook(
    db: AsyncSession,
    playbook_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    pb = await _get_owned_playbook(db, playbook_id, user_id)
    await db.delete(pb)
    await db.flush()
