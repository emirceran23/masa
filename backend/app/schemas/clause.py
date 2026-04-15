"""Clause request / response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ClauseResponse(BaseModel):
    id: UUID
    contract_id: UUID
    sequence_no: int
    original_text: str
    category: str | None = None
    confidence_score: float | None = None
    status: str

    model_config = {"from_attributes": True}


class ClauseListResponse(BaseModel):
    total: int
    items: list[ClauseResponse]


class ClauseDetailResponse(ClauseResponse):
    risk_assessment: "RiskAssessmentResponse | None" = None
    revisions: "list[RevisionResponse]" = []


class UpdateCategoryRequest(BaseModel):
    category: str


# Forward-ref imports (to avoid circular) ─────────────────
from app.schemas.risk import RiskAssessmentResponse  # noqa: E402
from app.schemas.revision import RevisionResponse  # noqa: E402

ClauseDetailResponse.model_rebuild()
