"""API tests for /api/v1/playbooks — service layer mocked, no DB required."""

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
from app.schemas.playbook import PlaybookDetailResponse, PlaybookResponse, PlaybookRuleResponse

BASE = "/api/v1/playbooks"

# ── Shared test data ──────────────────────────────────────

FAKE_USER_ID = uuid.uuid4()
FAKE_PB_ID = uuid.uuid4()
FAKE_RULE_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)


def _fake_user() -> MagicMock:
    u = MagicMock(spec=User)
    u.id = FAKE_USER_ID
    u.email = "test@lagent.dev"
    u.is_active = True
    return u


def _pb_response(**kwargs) -> PlaybookResponse:
    defaults = dict(
        id=FAKE_PB_ID,
        user_id=FAKE_USER_ID,
        name="Test Playbook",
        description=None,
        is_default=False,
        is_active=True,
        created_at=NOW,
        updated_at=NOW,
    )
    defaults.update(kwargs)
    return PlaybookResponse(**defaults)


def _pb_detail(name="Test Playbook", rules=None) -> PlaybookDetailResponse:
    return PlaybookDetailResponse(
        id=FAKE_PB_ID,
        user_id=FAKE_USER_ID,
        name=name,
        description=None,
        is_default=False,
        is_active=True,
        created_at=NOW,
        updated_at=NOW,
        rules=rules or [],
    )


def _rule_response() -> PlaybookRuleResponse:
    return PlaybookRuleResponse(
        id=FAKE_RULE_ID,
        rule_type="required",
        content="Fesih maddesi zorunludur.",
        threshold_value=None,
        created_at=NOW,
    )


# ── Fixtures ──────────────────────────────────────────────

@pytest_asyncio.fixture
async def api_client():
    """HTTP client with mocked DB + startup services. No auth override."""
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
    """api_client with get_current_user returning a fake user."""
    app.dependency_overrides[get_current_user] = lambda: _fake_user()
    yield api_client


# ── Tests: List ───────────────────────────────────────────

@pytest.mark.asyncio
class TestListPlaybooks:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.get(BASE)
        assert resp.status_code == 401

    async def test_empty_list(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.list_playbooks", new_callable=AsyncMock) as m:
            m.return_value = []
            resp = await auth_client.get(BASE)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_playbooks(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.list_playbooks", new_callable=AsyncMock) as m:
            m.return_value = [_pb_response(), _pb_response(id=uuid.uuid4(), name="Second")]
            resp = await auth_client.get(BASE)
        assert resp.status_code == 200
        assert len(resp.json()) == 2


# ── Tests: Create ─────────────────────────────────────────

@pytest.mark.asyncio
class TestCreatePlaybook:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.post(BASE, json={"name": "X"})
        assert resp.status_code == 401

    async def test_create_without_rules(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.create_playbook", new_callable=AsyncMock) as m:
            m.return_value = _pb_detail()
            resp = await auth_client.post(BASE, json={"name": "Empty Playbook"})
        assert resp.status_code == 201
        assert resp.json()["name"] == "Test Playbook"
        assert resp.json()["rules"] == []

    async def test_create_with_rules(self, auth_client: AsyncClient):
        rules = [_rule_response()]
        with patch("app.api.v1.playbooks.playbook_service.create_playbook", new_callable=AsyncMock) as m:
            m.return_value = _pb_detail(rules=rules)
            resp = await auth_client.post(
                BASE,
                json={
                    "name": "Kira Playbook",
                    "rules": [{"rule_type": "required", "content": "Fesih maddesi zorunludur."}],
                },
            )
        assert resp.status_code == 201
        assert len(resp.json()["rules"]) == 1
        assert resp.json()["rules"][0]["rule_type"] == "required"

    async def test_missing_name_returns_422(self, auth_client: AsyncClient):
        resp = await auth_client.post(BASE, json={})
        assert resp.status_code == 422

    async def test_empty_name_returns_422(self, auth_client: AsyncClient):
        resp = await auth_client.post(BASE, json={"name": ""})
        assert resp.status_code == 422


# ── Tests: Get ────────────────────────────────────────────

@pytest.mark.asyncio
class TestGetPlaybook:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.get(f"{BASE}/{FAKE_PB_ID}")
        assert resp.status_code == 401

    async def test_get_existing(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.get_playbook", new_callable=AsyncMock) as m:
            m.return_value = _pb_detail(rules=[_rule_response()])
            resp = await auth_client.get(f"{BASE}/{FAKE_PB_ID}")
        assert resp.status_code == 200
        assert resp.json()["id"] == str(FAKE_PB_ID)
        assert len(resp.json()["rules"]) == 1

    async def test_get_nonexistent_returns_404(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.get_playbook", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Playbook bulunamadı.")
            resp = await auth_client.get(f"{BASE}/{uuid.uuid4()}")
        assert resp.status_code == 404

    async def test_other_users_playbook_returns_404(self, auth_client: AsyncClient):
        """Service enforces ownership — raises NotFoundError for wrong user."""
        with patch("app.api.v1.playbooks.playbook_service.get_playbook", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Playbook bulunamadı.")
            resp = await auth_client.get(f"{BASE}/{uuid.uuid4()}")
        assert resp.status_code == 404


# ── Tests: Update ─────────────────────────────────────────

@pytest.mark.asyncio
class TestUpdatePlaybook:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.put(f"{BASE}/{FAKE_PB_ID}", json={"name": "X"})
        assert resp.status_code == 401

    async def test_update_name_only(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.update_playbook", new_callable=AsyncMock) as m:
            m.return_value = _pb_detail(name="Updated Name", rules=[_rule_response()])
            resp = await auth_client.put(f"{BASE}/{FAKE_PB_ID}", json={"name": "Updated Name"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"
        assert len(resp.json()["rules"]) == 1  # rules untouched

    async def test_update_rules_replaces_all(self, auth_client: AsyncClient):
        new_rule = PlaybookRuleResponse(
            id=uuid.uuid4(), rule_type="threshold", content="Ceza",
            threshold_value=0.05, created_at=NOW
        )
        with patch("app.api.v1.playbooks.playbook_service.update_playbook", new_callable=AsyncMock) as m:
            m.return_value = _pb_detail(rules=[new_rule])
            resp = await auth_client.put(
                f"{BASE}/{FAKE_PB_ID}",
                json={"rules": [{"rule_type": "threshold", "content": "Ceza", "threshold_value": 0.05}]},
            )
        assert resp.status_code == 200
        assert resp.json()["rules"][0]["threshold_value"] == 0.05

    async def test_update_nonexistent_returns_404(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.update_playbook", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Playbook bulunamadı.")
            resp = await auth_client.put(f"{BASE}/{uuid.uuid4()}", json={"name": "X"})
        assert resp.status_code == 404


# ── Tests: Delete ─────────────────────────────────────────

@pytest.mark.asyncio
class TestDeletePlaybook:
    async def test_unauthenticated_returns_401(self, api_client: AsyncClient):
        resp = await api_client.delete(f"{BASE}/{FAKE_PB_ID}")
        assert resp.status_code == 401

    async def test_delete_success(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.delete_playbook", new_callable=AsyncMock) as m:
            m.return_value = None
            resp = await auth_client.delete(f"{BASE}/{FAKE_PB_ID}")
        assert resp.status_code == 200
        assert "silindi" in resp.json()["message"]

    async def test_delete_nonexistent_returns_404(self, auth_client: AsyncClient):
        with patch("app.api.v1.playbooks.playbook_service.delete_playbook", new_callable=AsyncMock) as m:
            m.side_effect = NotFoundError("Playbook bulunamadı.")
            resp = await auth_client.delete(f"{BASE}/{uuid.uuid4()}")
        assert resp.status_code == 404
