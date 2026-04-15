"""Clause endpoints — list, detail, manual category update."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.user import User
from app.schemas.clause import (
    ClauseDetailResponse,
    ClauseListResponse,
    ClauseResponse,
    UpdateCategoryRequest,
)

router = APIRouter(prefix="/clauses", tags=["Clauses"])


@router.get("/by-contract/{contract_id}", response_model=ClauseListResponse)
async def list_clauses(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bir sözleşmenin tüm maddelerini döndürür."""
    # ownership check
    c = await db.execute(
        select(Contract).where(Contract.id == contract_id, Contract.user_id == current_user.id)
    )
    if not c.scalar_one_or_none():
        raise NotFoundError("Sözleşme bulunamadı.")

    count = (
        await db.execute(
            select(func.count()).select_from(Clause).where(Clause.contract_id == contract_id)
        )
    ).scalar() or 0

    rows = (
        await db.execute(
            select(Clause)
            .where(Clause.contract_id == contract_id)
            .order_by(Clause.sequence_no)
        )
    ).scalars().all()

    items = [ClauseResponse.model_validate(r) for r in rows]
    return ClauseListResponse(total=count, items=items)


@router.get("/{clause_id}", response_model=ClauseDetailResponse)
async def get_clause(
    clause_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Madde detayını (risk + revizyon) döndürür."""
    stmt = (
        select(Clause)
        .options(
            selectinload(Clause.risk_assessment),
            selectinload(Clause.revisions),
        )
        .where(Clause.id == clause_id)
    )
    clause = (await db.execute(stmt)).scalar_one_or_none()
    if not clause:
        raise NotFoundError("Madde bulunamadı.")

    # ownership via contract
    contract = await db.get(Contract, clause.contract_id)
    if not contract or contract.user_id != current_user.id:
        raise NotFoundError("Madde bulunamadı.")

    return ClauseDetailResponse.model_validate(clause)


@router.patch("/{clause_id}/category", response_model=ClauseResponse)
async def update_category(
    clause_id: UUID,
    payload: UpdateCategoryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Maddenin kategorisini manuel olarak günceller (düşük güven senaryosu)."""
    clause = await db.get(Clause, clause_id)
    if not clause:
        raise NotFoundError("Madde bulunamadı.")

    contract = await db.get(Contract, clause.contract_id)
    if not contract or contract.user_id != current_user.id:
        raise NotFoundError("Madde bulunamadı.")

    clause.category = payload.category
    clause.confidence_score = 1.0  # manual override → full confidence
    await db.flush()
    await db.refresh(clause)
    return ClauseResponse.model_validate(clause)
