"""Authentication service — register, login, token management."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import (
    AccountLockedError,
    BadRequestError,
    ConflictError,
    UnauthorizedError,
)
from app.core.redis import (
    clear_login_attempts,
    increment_login_attempts,
    is_account_locked,
    lock_account,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse


async def register_user(db: AsyncSession, payload: RegisterRequest) -> UserResponse:
    """Create a new user account."""
    # Check if email already exists
    stmt = select(User).where(User.email == payload.email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise ConflictError("Bu e-posta adresi zaten kullanımda.")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return UserResponse.model_validate(user)


async def authenticate_user(db: AsyncSession, email: str, password: str) -> TokenResponse:
    """Validate credentials, return JWT pair. Handles lockout logic."""
    # Check lock
    if await is_account_locked(email):
        raise AccountLockedError(settings.LOGIN_LOCKOUT_MINUTES)

    # Fetch user
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        attempts = await increment_login_attempts(email)
        if attempts >= settings.MAX_LOGIN_ATTEMPTS:
            await lock_account(email)
            raise AccountLockedError(settings.LOGIN_LOCKOUT_MINUTES)
        raise UnauthorizedError("E-posta veya şifre hatalı.")

    if not user.is_active:
        raise UnauthorizedError("Hesabınız devre dışı bırakılmış.")

    # Success → clear counter, issue tokens
    await clear_login_attempts(email)
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


async def refresh_access_token(refresh_token: str) -> TokenResponse:
    """Issue a new access token using a valid refresh token."""
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise UnauthorizedError("Geçersiz veya süresi dolmuş yenileme token'ı.")
    token_data = {"sub": payload["sub"], "email": payload["email"], "role": payload["role"]}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
