"""Contract request / response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ContractResponse(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    file_format: str
    file_size: int
    status: str
    total_clauses: int
    playbook_id: UUID | None = None
    uploaded_at: datetime
    analyzed_at: datetime | None = None

    model_config = {"from_attributes": True}


class ContractListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[ContractResponse]


class ContractDetailResponse(ContractResponse):
    raw_text: str | None = None


class AnalyzeRequest(BaseModel):
    playbook_id: UUID | None = None
