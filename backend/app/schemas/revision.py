"""Revision response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RevisionResponse(BaseModel):
    id: UUID
    clause_id: UUID
    suggested_text: str
    diff_html: str | None = None
    status: str
    edited_text: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
