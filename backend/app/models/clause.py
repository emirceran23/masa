"""Sözleşme Maddesi (Clause) veritabanı modeli."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Clause(Base):
    """Sözleşme maddesi tablosu."""

    __tablename__ = "clauses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False)
    clause_number = Column(Integer, nullable=False, comment="Madde sırası")
    original_text = Column(Text, nullable=False, comment="Orijinal madde metni")
    category = Column(
        String(100),
        nullable=True,
        comment="Sınıflandırma: gizlilik, tazminat, fesih, vb.",
    )
    risk_score = Column(Float, nullable=True, comment="Risk skoru (1-10)")
    risk_reason = Column(Text, nullable=True, comment="Risk gerekçesi")
    suggested_revision = Column(Text, nullable=True, comment="Önerilen revizyon metni")
    approval_status = Column(
        SAEnum("pending", "approved", "rejected", "revised", name="approval_status"),
        default="pending",
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    # İlişkiler
    contract = relationship("Contract", back_populates="clauses")
