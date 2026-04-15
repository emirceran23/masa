"""Playbook endpoints — CRUD."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.playbook import (
    PlaybookCreateRequest,
    PlaybookDetailResponse,
    PlaybookResponse,
    PlaybookUpdateRequest,
)
from app.services import playbook_service

router = APIRouter(prefix="/playbooks", tags=["Playbooks"])


@router.get("", response_model=list[PlaybookResponse])
async def list_playbooks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kullanıcının tüm playbook'larını listeler."""
    return await playbook_service.list_playbooks(db, current_user.id)


@router.post("", response_model=PlaybookDetailResponse, status_code=201)
async def create_playbook(
    payload: PlaybookCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Yeni playbook oluşturur ve kurallarını vektörize eder."""
    return await playbook_service.create_playbook(db, current_user.id, payload)


@router.get("/{playbook_id}", response_model=PlaybookDetailResponse)
async def get_playbook(
    playbook_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Playbook detayını (kurallarıyla birlikte) döndürür."""
    return await playbook_service.get_playbook(db, playbook_id, current_user.id)


@router.put("/{playbook_id}", response_model=PlaybookDetailResponse)
async def update_playbook(
    playbook_id: UUID,
    payload: PlaybookUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Playbook'u günceller; kurallar sağlanırsa vektör indeksi yenilenir."""
    return await playbook_service.update_playbook(db, playbook_id, current_user.id, payload)


@router.delete("/{playbook_id}", response_model=MessageResponse)
async def delete_playbook(
    playbook_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Playbook'u ve ilişkili tüm verileri siler."""
    await playbook_service.delete_playbook(db, playbook_id, current_user.id)
    return MessageResponse(message="Playbook başarıyla silindi.")
