"""Lagent — FastAPI Application Factory."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
from app.core.redis import get_redis
from app.storage.minio_client import ensure_bucket

# Import all models so Base.metadata knows about them
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup & shutdown hooks."""
    # ── Startup ──────────────────────────────────────────────
    # Auto-create database tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅  Database tables ensured.")

    # Ensure MinIO bucket exists (sync MinIO client, best-effort)
    try:
        ensure_bucket()
    except Exception as exc:
        print(f"⚠️  MinIO bucket setup skipped: {exc}")

    # Quick Redis health-check
    redis = await get_redis()
    await redis.ping()
    await redis.aclose()

    print("🟢  Lagent backend is ready.")
    yield
    # ── Shutdown ─────────────────────────────────────────────
    print("🔴  Lagent backend shutting down.")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Lagent API",
        description="Multi-Agent Legal Ops — Sözleşme İnceleme & Müzakere Orkestratörü",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ─────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routes ───────────────────────────────────────────────
    app.include_router(api_router, prefix="/api/v1")

    # ── Health check ─────────────────────────────────────────
    @app.get("/health", tags=["Health"])
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
