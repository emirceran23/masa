"""Contract service — upload, list, detail, delete."""

from __future__ import annotations

import uuid
from pathlib import PurePosixPath

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import FileTooLargeError, NotFoundError, UnsupportedFileError
from app.models.contract import Contract
from app.schemas.contract import ContractListResponse, ContractResponse, ContractDetailResponse
from app.services.document_processor import extract_text
from app.storage.minio_client import delete_file, upload_file

ALLOWED_FORMATS = {"pdf", "docx"}


async def upload_contract(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    file_name: str,
    file_data: bytes,
    content_type: str,
) -> ContractResponse:
    """Validate, store, convert to text, and persist contract metadata."""

    # ── Validate format ──────────────────────────────────
    suffix = PurePosixPath(file_name).suffix.lower().strip(".")
    if suffix not in ALLOWED_FORMATS:
        raise UnsupportedFileError()

    # ── Validate size ────────────────────────────────────
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(file_data) > max_bytes:
        raise FileTooLargeError(settings.MAX_FILE_SIZE_MB)

    # ── Upload to MinIO ──────────────────────────────────
    object_name = f"{user_id}/{uuid.uuid4().hex}_{file_name}"
    storage_path = upload_file(object_name, file_data, content_type)

    # ── Convert to plain text ────────────────────────────
    try:
        raw_text = extract_text(file_data, suffix)
    except Exception as exc:
        raw_text = None  # will be marked as error

    status = "uploaded" if raw_text else "error"

    # ── Persist to DB ────────────────────────────────────
    contract = Contract(
        user_id=user_id,
        file_name=file_name,
        storage_path=storage_path,
        file_format=suffix,
        file_size=len(file_data),
        raw_text=raw_text,
        status=status,
    )
    db.add(contract)
    await db.flush()
    await db.refresh(contract)
    return ContractResponse.model_validate(contract)


async def list_contracts(
    db: AsyncSession,
    user_id: uuid.UUID,
    page: int = 1,
    size: int = 20,
) -> ContractListResponse:
    count_stmt = select(func.count()).select_from(Contract).where(Contract.user_id == user_id)
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(Contract)
        .where(Contract.user_id == user_id)
        .order_by(Contract.uploaded_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    rows = (await db.execute(stmt)).scalars().all()
    items = [ContractResponse.model_validate(c) for c in rows]
    return ContractListResponse(total=total, page=page, size=size, items=items)


async def get_contract(
    db: AsyncSession, contract_id: uuid.UUID, user_id: uuid.UUID
) -> ContractDetailResponse:
    stmt = select(Contract).where(Contract.id == contract_id, Contract.user_id == user_id)
    contract = (await db.execute(stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")
    return ContractDetailResponse.model_validate(contract)


async def delete_contract(
    db: AsyncSession, contract_id: uuid.UUID, user_id: uuid.UUID
) -> None:
    stmt = select(Contract).where(Contract.id == contract_id, Contract.user_id == user_id)
    contract = (await db.execute(stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")
    # Delete from MinIO
    try:
        object_name = contract.storage_path.replace(f"{settings.MINIO_BUCKET}/", "", 1)
        delete_file(object_name)
    except Exception:
        pass  # best-effort
    await db.delete(contract)
    await db.flush()
