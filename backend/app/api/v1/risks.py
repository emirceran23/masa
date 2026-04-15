"""Risk endpoints — read risk assessments and missing provisions."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.risk import RiskAssessmentResponse
from app.services import risk_service

router = APIRouter(tags=["Risks"])


@router.get("/contracts/{contract_id}/risks", response_model=list[RiskAssessmentResponse])
async def list_risks(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bir sözleşmedeki tüm maddelerin risk değerlendirmelerini döndürür."""
    return await risk_service.list_risks(db, contract_id, current_user.id)


@router.get("/contracts/{contract_id}/missing-provisions")
async def list_missing_provisions(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşmedeki eksik hükümleri döndürür (Risk Agent tarafından doldurulur)."""
    return await risk_service.list_missing_provisions(db, contract_id, current_user.id)
