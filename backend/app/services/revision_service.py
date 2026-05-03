"""Revision service — CRUD for Revision suggestions."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.revision import Revision
from app.schemas.revision import RevisionResponse
from app.utils.diff import compute_diff_html


async def _verify_clause_owner(
    db: AsyncSession, clause_id: uuid.UUID, user_id: uuid.UUID
) -> Clause:
    stmt = (
        select(Clause)
        .join(Contract, Contract.id == Clause.contract_id)
        .where(Clause.id == clause_id, Contract.user_id == user_id)
    )
    clause = (await db.execute(stmt)).scalar_one_or_none()
    if not clause:
        raise NotFoundError("Madde bulunamadı.")
    return clause


async def list_revisions_for_clause(
    db: AsyncSession,
    clause_id: uuid.UUID,
    user_id: uuid.UUID,
) -> list[RevisionResponse]:
    await _verify_clause_owner(db, clause_id, user_id)
    stmt = (
        select(Revision)
        .where(Revision.clause_id == clause_id)
        .order_by(Revision.created_at.asc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [RevisionResponse.model_validate(r) for r in rows]


async def list_revisions_for_contract(
    db: AsyncSession,
    contract_id: uuid.UUID,
    user_id: uuid.UUID,
) -> list[RevisionResponse]:
    """Return all revisions for every clause in a contract."""
    # Verify ownership via contract
    stmt_c = select(Contract).where(
        Contract.id == contract_id, Contract.user_id == user_id
    )
    contract = (await db.execute(stmt_c)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")

    stmt = (
        select(Revision)
        .join(Clause, Clause.id == Revision.clause_id)
        .where(Clause.contract_id == contract_id)
        .order_by(Clause.sequence_no.asc(), Revision.created_at.asc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [RevisionResponse.model_validate(r) for r in rows]


async def accept_revision(
    db: AsyncSession,
    revision_id: uuid.UUID,
    user_id: uuid.UUID,
) -> RevisionResponse:
    rev = await _get_owned_revision(db, revision_id, user_id)
    _assert_pending(rev)
    rev.status = "accepted"
    await db.flush()
    return RevisionResponse.model_validate(rev)


async def reject_revision(
    db: AsyncSession,
    revision_id: uuid.UUID,
    user_id: uuid.UUID,
) -> RevisionResponse:
    rev = await _get_owned_revision(db, revision_id, user_id)
    _assert_pending(rev)
    rev.status = "rejected"
    await db.flush()
    return RevisionResponse.model_validate(rev)


async def edit_revision(
    db: AsyncSession,
    revision_id: uuid.UUID,
    user_id: uuid.UUID,
    edited_text: str,
) -> RevisionResponse:
    """User provides their own final text; diff is recomputed."""
    rev = await _get_owned_revision(db, revision_id, user_id)
    _assert_pending(rev)
    rev.edited_text = edited_text
    rev.diff_html = compute_diff_html(rev.suggested_text, edited_text)
    rev.status = "edited"
    await db.flush()
    return RevisionResponse.model_validate(rev)


# ── Helpers ───────────────────────────────────────────────────

async def _get_owned_revision(
    db: AsyncSession,
    revision_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Revision:
    stmt = (
        select(Revision)
        .join(Clause, Clause.id == Revision.clause_id)
        .join(Contract, Contract.id == Clause.contract_id)
        .where(Revision.id == revision_id, Contract.user_id == user_id)
    )
    rev = (await db.execute(stmt)).scalar_one_or_none()
    if not rev:
        raise NotFoundError("Revizyon bulunamadı.")
    return rev


def _assert_pending(rev: Revision) -> None:
    if rev.status != "pending":
        raise BadRequestError(
            f"Bu revizyon zaten '{rev.status}' durumunda; tekrar işlem yapılamaz."
        )
