"""Structured output schema for Clause Agent (OpenAI Function Calling)."""

from pydantic import BaseModel, Field


class ClauseItem(BaseModel):
    sequence_no: int = Field(description="Madde sıra numarası")
    original_text: str = Field(description="Maddenin tam orijinal metni")
    category: str = Field(
        description=(
            "Hukuki kategori: gizlilik | tazminat | fesih | fikri_mulkiyet | "
            "sorumluluk_sinirlandirma | uyusmazlik_cozumu | odeme_kosullari | "
            "genel_hukumler | diger | belirsiz"
        )
    )
    confidence_score: float = Field(ge=0.0, le=1.0, description="Sınıflandırma güven skoru")


class ClauseAgentOutput(BaseModel):
    clauses: list[ClauseItem] = Field(description="Ayrıştırılmış ve sınıflandırılmış maddeler")
