"""Approval service — clause-level decision workflow with audit trail.

State machine for a clause:
  draft → in_review  (when analysis completes and risk is medium/high)
  in_review → approved | rejected | revise  (human decision)
  revise → in_review  (after a revision is edited/accepted, ready for re-review)

High-risk clauses cannot be marked 'approved' without an explicit decision
(they start as 'in_review' after analysis).
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.approval import ApprovalDecision
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.risk_assessment import RiskAssessment
from app.schemas.approval import ApprovalDecisionResponse
from app.services.audit_service import log_action

VALID_DECISIONS = {"approved", "rejected", "revise"}


async def _verify_clause_owner(
    db: AsyncSession,
    clause_id: uuid.UUID,
    user_id: uuid.UUID,
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


async def decide_clause(
    db: AsyncSession,
    clause_id: uuid.UUID,
    user_id: uuid.UUID,
    decision: str,
    comment: str | None = None,
) -> ApprovalDecisionResponse:
    if decision not in VALID_DECISIONS:
        raise BadRequestError(
            f"Geçersiz karar: '{decision}'. Kabul edilen değerler: {VALID_DECISIONS}"
        )

    clause = await _verify_clause_owner(db, clause_id, user_id)

    # Persist the decision
    record = ApprovalDecision(
        clause_id=clause_id,
        user_id=user_id,
        decision=decision,
        comment=comment,
    )
    db.add(record)

    # Transition clause status
    new_clause_status = _next_clause_status(decision)
    clause.status = new_clause_status
    await db.flush()

    # Audit trail
    await log_action(
        db,
        user_id=user_id,
        action_type=f"clause.{decision}",
        resource_type="clause",
        resource_id=clause_id,
        details={"decision": decision, "comment": comment},
    )

    return ApprovalDecisionResponse.model_validate(record)


async def bulk_decide(
    db: AsyncSession,
    clause_ids: list[uuid.UUID],
    user_id: uuid.UUID,
    decision: str,
    comment: str | None = None,
) -> list[ApprovalDecisionResponse]:
    if decision not in VALID_DECISIONS:
        raise BadRequestError(f"Geçersiz karar: '{decision}'.")

    results = []
    for cid in clause_ids:
        try:
            result = await decide_clause(db, cid, user_id, decision, comment)
            results.append(result)
        except NotFoundError:
            continue  # Skip clauses not owned by user
    return results


async def get_decisions_for_clause(
    db: AsyncSession,
    clause_id: uuid.UUID,
    user_id: uuid.UUID,
) -> list[ApprovalDecisionResponse]:
    await _verify_clause_owner(db, clause_id, user_id)
    stmt = (
        select(ApprovalDecision)
        .where(ApprovalDecision.clause_id == clause_id)
        .order_by(ApprovalDecision.decided_at.asc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [ApprovalDecisionResponse.model_validate(r) for r in rows]


async def promote_risky_clauses_to_review(
    db: AsyncSession,
    contract_id: uuid.UUID,
) -> int:
    """After analysis, set all medium/high clauses to 'in_review' status.

    Called at the end of start_analysis so the approval queue is pre-populated.
    Returns the number of clauses promoted.
    """
    stmt = (
        select(Clause)
        .join(RiskAssessment, RiskAssessment.clause_id == Clause.id)
        .where(
            Clause.contract_id == contract_id,
            Clause.status == "draft",
            RiskAssessment.risk_level.in_(["medium", "high"]),
        )
    )
    clauses = (await db.execute(stmt)).scalars().all()
    for clause in clauses:
        clause.status = "in_review"
    await db.flush()
    return len(clauses)


def _next_clause_status(decision: str) -> str:
    return {
        "approved": "approved",
        "rejected": "rejected",
        "revise": "in_review",
    }[decision]
