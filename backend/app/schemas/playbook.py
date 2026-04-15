"""Playbook request / response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# ── Rule ─────────────────────────────────────────────────
class PlaybookRuleBase(BaseModel):
    rule_type: str = Field(description="acceptable | rejected | required | threshold")
    content: str
    threshold_value: float | None = None


class PlaybookRuleResponse(PlaybookRuleBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Playbook ─────────────────────────────────────────────
class PlaybookCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    rules: list[PlaybookRuleBase] = []


class PlaybookUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    rules: list[PlaybookRuleBase] | None = None


class PlaybookResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None = None
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PlaybookDetailResponse(PlaybookResponse):
    rules: list[PlaybookRuleResponse] = []
