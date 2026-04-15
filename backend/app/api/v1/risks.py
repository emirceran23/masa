"""Risk endpoints — read risk assessments for a contract's clauses."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.risk_assessment import RiskAssessment
from app.models.user import User
from app.schemas.risk import RiskAssessmentResponse

router = APIRouter(tags=["Risks"])


@router.get("/contracts/{contract_id}/risks", response_model=list[RiskAssessmentResponse])
async def list_risks(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bir sözleşmedeki tüm maddelerin risk değerlendirmelerini döndürür."""
    # Verify contract belongs to this user
    contract_stmt = select(Contract).where(
        Contract.id == contract_id, Contract.user_id == current_user.id
    )
    contract = (await db.execute(contract_stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")

    stmt = (
        select(RiskAssessment)
        .join(Clause, Clause.id == RiskAssessment.clause_id)
        .where(Clause.contract_id == contract_id)
        .order_by(RiskAssessment.assessed_at.asc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [RiskAssessmentResponse.model_validate(r) for r in rows]


@router.get("/contracts/{contract_id}/missing-provisions")
async def list_missing_provisions(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşmedeki eksik hükümleri döndürür (Risk Agent tarafından doldurulur)."""
    contract_stmt = select(Contract).where(
        Contract.id == contract_id, Contract.user_id == current_user.id
    )
    contract = (await db.execute(contract_stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")

    stmt = text("""
        SELECT id, contract_id, playbook_rule_id, description, detected_at
        FROM missing_provisions
        WHERE contract_id = :cid
        ORDER BY detected_at ASC
    """)
    rows = (await db.execute(stmt, {"cid": str(contract_id)})).mappings().all()
    return [dict(row) for row in rows]
