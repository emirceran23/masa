"""Revision endpoints — list, accept, reject, edit."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.revision import (
    RevisionDecisionRequest,
    RevisionEditRequest,
    RevisionResponse,
)
from app.services import revision_service

router = APIRouter(tags=["Revisions"])


# ── Per-contract list (for the redline screen) ────────────────

@router.get(
    "/contracts/{contract_id}/revisions",
    response_model=list[RevisionResponse],
)
async def list_contract_revisions(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bir sözleşmedeki tüm revizyon önerilerini madde sırasıyla döndürür."""
    return await revision_service.list_revisions_for_contract(
        db, contract_id, current_user.id
    )


# ── Per-clause list ───────────────────────────────────────────

@router.get(
    "/clauses/{clause_id}/revisions",
    response_model=list[RevisionResponse],
)
async def list_clause_revisions(
    clause_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Belirli bir maddenin revizyon önerilerini döndürür."""
    return await revision_service.list_revisions_for_clause(
        db, clause_id, current_user.id
    )


# ── Decisions ────────────────────────────────────────────────

@router.post(
    "/revisions/{revision_id}/accept",
    response_model=RevisionResponse,
)
async def accept_revision(
    revision_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Revizyon önerisini kabul et."""
    return await revision_service.accept_revision(db, revision_id, current_user.id)


@router.post(
    "/revisions/{revision_id}/reject",
    response_model=RevisionResponse,
)
async def reject_revision(
    revision_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Revizyon önerisini reddet."""
    return await revision_service.reject_revision(db, revision_id, current_user.id)


@router.post(
    "/revisions/{revision_id}/edit",
    response_model=RevisionResponse,
)
async def edit_revision(
    revision_id: UUID,
    payload: RevisionEditRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kullanıcı kendi düzenlediği metni kaydeder; diff yeniden hesaplanır."""
    return await revision_service.edit_revision(
        db, revision_id, current_user.id, payload.edited_text
    )
