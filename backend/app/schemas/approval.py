"""Approval decision request / response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ApprovalDecisionRequest(BaseModel):
    decision: str = Field(description="approved | rejected | revise")
    comment: str | None = None


class ApprovalDecisionResponse(BaseModel):
    id: UUID
    clause_id: UUID
    user_id: UUID
    decision: str
    comment: str | None = None
    decided_at: datetime

    model_config = {"from_attributes": True}


class BulkApprovalRequest(BaseModel):
    clause_ids: list[UUID]
    decision: str = Field(description="approved | rejected | revise")
    comment: str | None = None
