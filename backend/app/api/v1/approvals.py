"""Approval endpoints — clause-level human decision workflow."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.approval import (
    ApprovalDecisionRequest,
    ApprovalDecisionResponse,
    BulkApprovalRequest,
)
from app.services import approval_service

router = APIRouter(tags=["Approvals"])


@router.get(
    "/clauses/{clause_id}/decisions",
    response_model=list[ApprovalDecisionResponse],
)
async def get_clause_decisions(
    clause_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bir maddenin karar geçmişini döndürür."""
    return await approval_service.get_decisions_for_clause(
        db, clause_id, current_user.id
    )


@router.post(
    "/clauses/{clause_id}/decide",
    response_model=ApprovalDecisionResponse,
    status_code=201,
)
async def decide_clause(
    clause_id: UUID,
    payload: ApprovalDecisionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Madde için onay/red/revize kararı yaz."""
    return await approval_service.decide_clause(
        db,
        clause_id=clause_id,
        user_id=current_user.id,
        decision=payload.decision,
        comment=payload.comment,
    )


@router.post(
    "/contracts/{contract_id}/bulk-decide",
    response_model=list[ApprovalDecisionResponse],
    status_code=201,
)
async def bulk_decide(
    contract_id: UUID,
    payload: BulkApprovalRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Birden fazla maddeye aynı anda karar ver."""
    return await approval_service.bulk_decide(
        db,
        clause_ids=payload.clause_ids,
        user_id=current_user.id,
        decision=payload.decision,
        comment=payload.comment,
    )
