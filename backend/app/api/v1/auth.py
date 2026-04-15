"""Authentication endpoints — register, login, refresh."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.services import auth_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Yeni kullanıcı kaydı oluşturur."""
    return await auth_service.register_user(db, payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """E-posta ve şifre ile giriş yapar, JWT token çifti döndürür."""
    return await auth_service.authenticate_user(db, payload.email, payload.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest):
    """Refresh token kullanarak yeni access token alır."""
    return await auth_service.refresh_access_token(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    """Geçerli oturumdaki kullanıcı bilgilerini döndürür."""
    return UserResponse.model_validate(current_user)
