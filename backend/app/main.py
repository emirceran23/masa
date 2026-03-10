"""Multi-Agent Legal Ops — FastAPI Application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.approvals import router as approvals_router
from app.api.v1.contracts import router as contracts_router
from app.api.v1.reviews import router as reviews_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Uygulama yaşam döngüsü: başlatma ve kapatma işlemleri."""
    # Startup
    print(f"🚀 {settings.app_name} başlatılıyor...")
    yield
    # Shutdown
    print(f"🛑 {settings.app_name} kapatılıyor...")


app = FastAPI(
    title="Multi-Agent Legal Ops API",
    description="Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 route'larını bağla
app.include_router(contracts_router, prefix="/api/v1")
app.include_router(reviews_router, prefix="/api/v1")
app.include_router(approvals_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Sağlık kontrolü."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Detaylı sağlık kontrolü."""
    return {
        "status": "healthy",
        "services": {
            "api": True,
            # TODO: DB, Redis, MinIO bağlantı kontrolleri eklenecek
        },
    }
