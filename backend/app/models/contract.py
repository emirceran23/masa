"""Sözleşme (Contract) veritabanı modeli."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Contract(Base):
    """Sözleşme tablosu."""

    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(512), nullable=False)
    original_path = Column(String(1024), nullable=False, comment="MinIO object path")
    raw_text = Column(Text, nullable=True, comment="Çıkarılan ham metin")
    status = Column(
        SAEnum("uploaded", "processing", "analyzed", "reviewed", "error", name="contract_status"),
        default="uploaded",
        nullable=False,
    )
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # İlişkiler
    clauses = relationship("Clause", back_populates="contract", cascade="all, delete-orphan")
