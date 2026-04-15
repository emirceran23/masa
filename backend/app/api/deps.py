"""Shared FastAPI dependencies (auth, db session)."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_token
from app.models.user import User
from app.services.auth_service import get_user_by_id


async def get_current_user(
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate JWT from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Geçersiz token formatı.")

    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedError("Geçersiz veya süresi dolmuş token.")

    user_id = UUID(payload["sub"])
    user = await get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise UnauthorizedError("Kullanıcı bulunamadı veya devre dışı.")
    return user
