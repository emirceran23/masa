"""API tests for risk and missing-provisions endpoints — service mocked, no DB."""

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.main import app
from app.models.user import User
from app.schemas.risk import RiskAssessmentResponse

# ── Shared test data ──────────────────────────────────────

FAKE_USER_ID = uuid.uuid4()
FAKE_CONTRACT_ID = uuid.uuid4()
FAKE_CLAUSE_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)


def _fake_user() -> MagicMock:
    u = MagicMock(spec=User)
    u.id = FAKE_USER_ID
    u.is_active = True
    return u


def _risk_response(**kwargs) -> RiskAssessmentResponse:
    defaults = dict(
        id=uuid.uuid4(),
        clause_id=FAKE_CLAUSE_ID,
        risk_level="high",
        commercial_score=0.8,
        legal_score=0.9,
        rationale="Tek taraflı fesih yüksek risk taşır.",
        policy_compliance=False,
        cross_validated=False,
        assessed_at=NOW,
    )
    defaults.update(kwargs)
    return RiskAssessmentResponse(**defaults)


RISKS_URL = f"/api/v1/contracts/{FAKE_CONTRACT_ID}/risks"
MISSING_URL = f"/api/v1/contracts/{FAKE_CONTRACT_ID}/missing-provisions"


# ── Fixtures ──────────────────────────────────────────────

@pytest_asyncio.fixture
async def api_client():
    """Client with mocked DB — no auth override (for 401 tests)."""
    mock_redis = AsyncMock()

    async def _mock_get_db():
        yield AsyncMock()

    app.dependency_overrides[get_db] = _mock_get_db

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
async def auth_client(api_client):
    app.dependency_overrides[get_current_user] = lambda: _fake_user()
    yield api_client


# ── Tests: /risks ─────────────────────────────────────────

@pytest.mark.asyncio
class TestListRisks:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.get(RISKS_URL)
        assert resp.status_code == 401

    async def test_empty_before_risk_agent_runs(self, auth_client: AsyncClient):
        with patch("app.api.v1.risks.risk_service.list_risks", new_callable=AsyncMock) as m:
            m.return_value = []
            resp = await auth_client.get(RISKS_URL)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_risk_assessments(self, auth_client: AsyncClient):
        risks = [_risk_response(risk_level="high"), _risk_response(risk_level="low")]
        with patch("app.api.v1.risks.risk_service.list_risks", new_callable=AsyncMock) as m:
            m.return_value = risks
            resp = await auth_client.get(RISKS_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["risk_level"] == "high"
        assert data[1]["risk_level"] == "low"

    async def test_risk_response_fields_present(self, auth_client: AsyncClient):
        with patch("app.api.v1.risks.risk_service.list_risks", new_callable=AsyncMock) as m:
            m.return_value = [_risk_response()]
            resp = await auth_client.get(RISKS_URL)
        item = resp.json()[0]
        assert "risk_level" in item
        assert "rationale" in item
        assert "commercial_score" in item
        assert "legal_score" in item
        assert "policy_compliance" in item
        assert "cross_validated" in item

    async def test_nonexistent_contract_returns_404(self, auth_client: AsyncClient):
        with patch("app.api.v1.risks.risk_service.list_risks", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Sözleşme bulunamadı.")
            resp = await auth_client.get(f"/api/v1/contracts/{uuid.uuid4()}/risks")
        assert resp.status_code == 404

    async def test_other_users_contract_returns_404(self, auth_client: AsyncClient):
        """Service enforces ownership — other user's contract looks like 404."""
        with patch("app.api.v1.risks.risk_service.list_risks", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Sözleşme bulunamadı.")
            resp = await auth_client.get(RISKS_URL)
        assert resp.status_code == 404


# ── Tests: /missing-provisions ────────────────────────────

@pytest.mark.asyncio
class TestMissingProvisions:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.get(MISSING_URL)
        assert resp.status_code == 401

    async def test_empty_before_risk_agent_runs(self, auth_client: AsyncClient):
        with patch("app.api.v1.risks.risk_service.list_missing_provisions", new_callable=AsyncMock) as m:
            m.return_value = []
            resp = await auth_client.get(MISSING_URL)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_provisions_after_risk_agent(self, auth_client: AsyncClient):
        provisions = [
            {
                "id": str(uuid.uuid4()),
                "contract_id": str(FAKE_CONTRACT_ID),
                "playbook_rule_id": None,
                "description": "Gizlilik maddesi eksik.",
                "detected_at": NOW.isoformat(),
            }
        ]
        with patch("app.api.v1.risks.risk_service.list_missing_provisions", new_callable=AsyncMock) as m:
            m.return_value = provisions
            resp = await auth_client.get(MISSING_URL)
        assert resp.status_code == 200
        assert resp.json()[0]["description"] == "Gizlilik maddesi eksik."

    async def test_nonexistent_contract_returns_404(self, auth_client: AsyncClient):
        with patch("app.api.v1.risks.risk_service.list_missing_provisions", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Sözleşme bulunamadı.")
            resp = await auth_client.get(f"/api/v1/contracts/{uuid.uuid4()}/missing-provisions")
        assert resp.status_code == 404
