"""Structured output schemas for the Risk Agent."""

from uuid import UUID

from pydantic import BaseModel, Field


class RiskAgentOutput(BaseModel):
    risk_level: str = Field(description="low | medium | high")
    commercial_score: float = Field(ge=0.0, le=1.0)
    legal_score: float = Field(ge=0.0, le=1.0)
    rationale: str
    policy_compliance: bool = True
    matched_rule_ids: list[UUID] = Field(default_factory=list)


class MissingProvisionItem(BaseModel):
    playbook_rule_id: UUID
    description: str


class MissingProvisionsOutput(BaseModel):
    missing: list[MissingProvisionItem] = Field(default_factory=list)
