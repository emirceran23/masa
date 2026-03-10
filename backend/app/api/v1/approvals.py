"""Onay akışı API endpoint'leri."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/approvals", tags=["approvals"])


class ApprovalDecision(BaseModel):
    """Onay kararı modeli."""

    clause_id: str
    decision: str  # "approve" | "reject" | "revise"
    comment: str | None = None


@router.post("/{review_id}/decide")
async def submit_decision(review_id: str, decision: ApprovalDecision):
    """Bir madde için onay/red/revizyon kararı ver."""
    # TODO: Kararı kaydet ve state machine güncelle
    return {
        "review_id": review_id,
        "clause_id": decision.clause_id,
        "decision": decision.decision,
        "status": "recorded",
    }


@router.get("/{review_id}/status")
async def get_approval_status(review_id: str):
    """İncelemenin onay durumunu getir."""
    # TODO: Onay durumunu çek
    return {
        "review_id": review_id,
        "status": "pending",
        "approved_count": 0,
        "rejected_count": 0,
        "pending_count": 0,
    }
