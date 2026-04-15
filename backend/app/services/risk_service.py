"""Risk service — read risk assessments and missing provisions."""

from __future__ import annotations

import uuid

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.risk_assessment import RiskAssessment
from app.schemas.risk import RiskAssessmentResponse


async def _verify_contract_owner(
    db: AsyncSession, contract_id: uuid.UUID, user_id: uuid.UUID
) -> None:
    stmt = select(Contract).where(
        Contract.id == contract_id, Contract.user_id == user_id
    )
    contract = (await db.execute(stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")


async def list_risks(
    db: AsyncSession, contract_id: uuid.UUID, user_id: uuid.UUID
) -> list[RiskAssessmentResponse]:
    await _verify_contract_owner(db, contract_id, user_id)

    stmt = (
        select(RiskAssessment)
        .join(Clause, Clause.id == RiskAssessment.clause_id)
        .where(Clause.contract_id == contract_id)
        .order_by(RiskAssessment.assessed_at.asc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [RiskAssessmentResponse.model_validate(r) for r in rows]


async def list_missing_provisions(
    db: AsyncSession, contract_id: uuid.UUID, user_id: uuid.UUID
) -> list[dict]:
    await _verify_contract_owner(db, contract_id, user_id)

    stmt = text("""
        SELECT id, contract_id, playbook_rule_id, description, detected_at
        FROM missing_provisions
        WHERE contract_id = :cid
        ORDER BY detected_at ASC
    """)
    rows = (await db.execute(stmt, {"cid": str(contract_id)})).mappings().all()
    return [dict(row) for row in rows]
