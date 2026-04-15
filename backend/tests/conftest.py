"""Shared test fixtures."""

import uuid
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models.contract import Contract
from app.models.playbook import Playbook, PlaybookRule
from app.models.user import User

# Use a separate test database
TEST_DATABASE_URL = settings.database_url.replace(
    f"/{settings.POSTGRES_DB}", f"/{settings.POSTGRES_DB}_test"
)


@pytest_asyncio.fixture
async def _engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        # ORM-managed tables
        await conn.run_sync(Base.metadata.create_all)
        # Raw SQL tables (not ORM models — no pgvector type needed in tests)
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS missing_provisions (
                id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                contract_id      UUID NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
                playbook_rule_id UUID REFERENCES playbook_rules(id) ON DELETE SET NULL,
                description      TEXT NOT NULL,
                detected_at      TIMESTAMPTZ DEFAULT NOW()
            )
        """))
    yield engine
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS missing_provisions"))
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def _session_factory(_engine):
    return async_sessionmaker(_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def client(_session_factory) -> AsyncGenerator[AsyncClient, None]:
    async def _override_get_db():
        async with _session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = _override_get_db

    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock()
    mock_redis.aclose = AsyncMock()

    with (
        patch("app.main.ensure_bucket", return_value=None),
        patch("app.main.get_redis", return_value=mock_redis),
        patch("app.services.auth_service.is_account_locked", return_value=False),
        patch("app.services.auth_service.increment_login_attempts", return_value=1),
        patch("app.services.auth_service.clear_login_attempts", return_value=None),
        patch("app.services.auth_service.lock_account", return_value=None),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(_session_factory) -> User:
    async with _session_factory() as session:
        user = User(
            id=uuid.uuid4(),
            email="test@lagent.dev",
            password_hash=hash_password("TestPass123!@#"),
            full_name="Test User",
            role="user",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict:
    """Return Authorization headers for the test user."""
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@lagent.dev", "password": "TestPass123!@#"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def test_playbook(_session_factory, test_user: User) -> Playbook:
    """A persisted playbook (no embedding — index_rule is mocked in tests)."""
    async with _session_factory() as session:
        pb = Playbook(
            id=uuid.uuid4(),
            user_id=test_user.id,
            name="Test Playbook",
            description="Playbook for tests",
        )
        session.add(pb)
        await session.flush()
        rule = PlaybookRule(
            id=uuid.uuid4(),
            playbook_id=pb.id,
            rule_type="required",
            content="Sözleşme fesih maddesini içermelidir.",
        )
        session.add(rule)
        await session.commit()
        await session.refresh(pb)
        return pb


@pytest_asyncio.fixture
async def test_contract(_session_factory, test_user: User) -> Contract:
    """A minimal persisted contract in 'analyzed' status."""
    async with _session_factory() as session:
        contract = Contract(
            id=uuid.uuid4(),
            user_id=test_user.id,
            file_name="test.pdf",
            storage_path="test/test.pdf",
            file_format="pdf",
            file_size=1024,
            raw_text="Madde 1: Taraflar bu sözleşmeye uymayı kabul eder.",
            status="analyzed",
            total_clauses=1,
        )
        session.add(contract)
        await session.commit()
        await session.refresh(contract)
        return contract
