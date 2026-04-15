"""Contract endpoints — upload, list, detail, delete, analyze."""

from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.redis import get_analysis_progress
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.contract import (
    AnalyzeRequest,
    ContractDetailResponse,
    ContractListResponse,
    ContractResponse,
)
from app.services import contract_service, analysis_service, audit_service

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/upload", response_model=ContractResponse, status_code=201)
async def upload_contract(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşme dosyası yükler (PDF / DOCX, maks 10 MB)."""
    data = await file.read()
    result = await contract_service.upload_contract(
        db,
        user_id=current_user.id,
        file_name=file.filename or "unknown",
        file_data=data,
        content_type=file.content_type or "application/octet-stream",
    )
    await audit_service.log_action(
        db,
        user_id=current_user.id,
        action_type="upload",
        resource_type="contract",
        resource_id=result.id,
    )
    return result


@router.get("", response_model=ContractListResponse)
async def list_contracts(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kullanıcının sözleşme listesini döndürür."""
    return await contract_service.list_contracts(db, current_user.id, page, size)


@router.get("/{contract_id}", response_model=ContractDetailResponse)
async def get_contract(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşme detayını döndürür."""
    return await contract_service.get_contract(db, contract_id, current_user.id)


@router.delete("/{contract_id}", response_model=MessageResponse)
async def delete_contract(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşmeyi siler."""
    await contract_service.delete_contract(db, contract_id, current_user.id)
    await audit_service.log_action(
        db,
        user_id=current_user.id,
        action_type="delete",
        resource_type="contract",
        resource_id=contract_id,
    )
    return MessageResponse(message="Sözleşme başarıyla silindi.")


@router.post("/{contract_id}/analyze", response_model=MessageResponse)
async def analyze_contract(
    contract_id: UUID,
    payload: Optional[AnalyzeRequest] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşme analizi başlatır (Clause Agent → sınıflandırma)."""
    playbook_id = payload.playbook_id if payload else None
    await analysis_service.start_analysis(db, contract_id, current_user.id, playbook_id)
    await audit_service.log_action(
        db,
        user_id=current_user.id,
        action_type="analyze",
        resource_type="contract",
        resource_id=contract_id,
    )
    return MessageResponse(message="Analiz başarıyla tamamlandı.")


@router.get("/{contract_id}/status")
async def contract_status(contract_id: UUID):
    """Analiz ilerleme durumunu döndürür (Redis'ten)."""
    progress = await get_analysis_progress(str(contract_id))
    if not progress:
        return {"status": "unknown", "progress": 0}
    return progress
