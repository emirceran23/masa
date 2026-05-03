"""Revision request / response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RevisionResponse(BaseModel):
    id: UUID
    clause_id: UUID
    suggested_text: str
    context_used: str | None = None
    diff_html: str | None = None
    status: str
    edited_text: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class RevisionEditRequest(BaseModel):
    """User submits their own edited text for a pending revision."""
    edited_text: str


class RevisionDecisionRequest(BaseModel):
    """Accept or reject a revision suggestion."""
    decision: str  # "accepted" | "rejected"
