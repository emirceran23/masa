"""Risk assessment model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    clause_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clauses.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)  # low | medium | high
    commercial_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    legal_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    policy_compliance: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    cross_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    clause = relationship("Clause", back_populates="risk_assessment")
