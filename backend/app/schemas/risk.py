"""Risk assessment response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RiskAssessmentResponse(BaseModel):
    id: UUID
    clause_id: UUID
    risk_level: str
    commercial_score: float | None = None
    legal_score: float | None = None
    rationale: str
    policy_compliance: bool | None = None
    cross_validated: bool
    assessed_at: datetime

    model_config = {"from_attributes": True}
