"""Report Pydantic schemas."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ReportGenerateRequest(BaseModel):
    report_type: str = "summary"  # summary | detailed
    fmt: str = "pdf"              # pdf | docx


class ReportResponse(BaseModel):
    id: UUID
    contract_id: UUID
    report_type: str
    total_clauses: int | None = None
    summary_data: dict[str, Any] | None = None
    storage_path: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
