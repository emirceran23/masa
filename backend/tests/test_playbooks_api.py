"""Integration tests for /api/v1/playbooks endpoints.

index_rule is mocked throughout — we test HTTP + DB logic, not OpenAI.
"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.models.playbook import Playbook

MOCK_INDEX = patch("app.services.playbook_service.index_rule", new_callable=AsyncMock)

BASE = "/api/v1/playbooks"


@pytest.mark.asyncio
class TestListPlaybooks:
    async def test_unauthenticated_returns_401(self, client: AsyncClient):
        resp = await client.get(BASE)
        assert resp.status_code == 401

    async def test_empty_list(self, client: AsyncClient, auth_headers, test_user):
        with MOCK_INDEX:
            resp = await client.get(BASE, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_own_playbooks(
        self, client: AsyncClient, auth_headers, test_playbook: Playbook
    ):
        with MOCK_INDEX:
            resp = await client.get(BASE, headers=auth_headers)
        assert resp.status_code == 200
        ids = [pb["id"] for pb in resp.json()]
        assert str(test_playbook.id) in ids


@pytest.mark.asyncio
class TestCreatePlaybook:
    async def test_unauthenticated_returns_401(self, client: AsyncClient):
        resp = await client.post(BASE, json={"name": "X"})
        assert resp.status_code == 401

    async def test_create_without_rules(self, client: AsyncClient, auth_headers):
        with MOCK_INDEX:
            resp = await client.post(
                BASE,
                json={"name": "Empty Playbook"},
                headers=auth_headers,
            )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Empty Playbook"
        assert data["rules"] == []
        assert "id" in data

    async def test_create_with_rules(self, client: AsyncClient, auth_headers):
        payload = {
            "name": "Kira Playbook",
            "description": "Kira sözleşmeleri için",
            "rules": [
                {"rule_type": "required", "content": "Kira bedeli açıkça belirtilmelidir."},
                {"rule_type": "rejected", "content": "Tek taraflı fesih hakkı kabul edilemez."},
            ],
        }
        with MOCK_INDEX:
            resp = await client.post(BASE, json=payload, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Kira Playbook"
        assert len(data["rules"]) == 2
        rule_types = {r["rule_type"] for r in data["rules"]}
        assert rule_types == {"required", "rejected"}

    async def test_create_missing_name_returns_422(self, client: AsyncClient, auth_headers):
        with MOCK_INDEX:
            resp = await client.post(BASE, json={}, headers=auth_headers)
        assert resp.status_code == 422

    async def test_create_empty_name_returns_422(self, client: AsyncClient, auth_headers):
        with MOCK_INDEX:
            resp = await client.post(BASE, json={"name": ""}, headers=auth_headers)
        assert resp.status_code == 422


@pytest.mark.asyncio
class TestGetPlaybook:
    async def test_unauthenticated_returns_401(self, client: AsyncClient, test_playbook):
        resp = await client.get(f"{BASE}/{test_playbook.id}")
        assert resp.status_code == 401

    async def test_get_own_playbook(
        self, client: AsyncClient, auth_headers, test_playbook: Playbook
    ):
        with MOCK_INDEX:
            resp = await client.get(f"{BASE}/{test_playbook.id}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == str(test_playbook.id)
        assert data["name"] == "Test Playbook"
        assert len(data["rules"]) == 1

    async def test_get_nonexistent_returns_404(self, client: AsyncClient, auth_headers):
        import uuid
        with MOCK_INDEX:
            resp = await client.get(f"{BASE}/{uuid.uuid4()}", headers=auth_headers)
        assert resp.status_code == 404

    async def test_cannot_access_other_users_playbook(
        self, client: AsyncClient, test_playbook: Playbook
    ):
        # Register and login as a different user
        await client.post(
            "/api/v1/auth/register",
            json={"email": "other@lagent.dev", "password": "OtherPass123!@#", "full_name": "Other"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "other@lagent.dev", "password": "OtherPass123!@#"},
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        with MOCK_INDEX:
            resp = await client.get(f"{BASE}/{test_playbook.id}", headers=other_headers)
        assert resp.status_code == 404


@pytest.mark.asyncio
class TestUpdatePlaybook:
    async def test_unauthenticated_returns_401(self, client: AsyncClient, test_playbook):
        resp = await client.put(f"{BASE}/{test_playbook.id}", json={"name": "X"})
        assert resp.status_code == 401

    async def test_update_name_only(
        self, client: AsyncClient, auth_headers, test_playbook: Playbook
    ):
        with MOCK_INDEX:
            resp = await client.put(
                f"{BASE}/{test_playbook.id}",
                json={"name": "Updated Name"},
                headers=auth_headers,
            )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"
        # Rules must be untouched
        assert len(resp.json()["rules"]) == 1

    async def test_update_rules_replaces_all(
        self, client: AsyncClient, auth_headers, test_playbook: Playbook
    ):
        new_rules = [
            {"rule_type": "acceptable", "content": "Ödeme vadesi 30 gün olabilir."},
            {"rule_type": "threshold", "content": "Ceza oranı", "threshold_value": 0.05},
        ]
        with MOCK_INDEX:
            resp = await client.put(
                f"{BASE}/{test_playbook.id}",
                json={"rules": new_rules},
                headers=auth_headers,
            )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["rules"]) == 2
        assert data["rules"][1]["threshold_value"] == 0.05

    async def test_update_nonexistent_returns_404(self, client: AsyncClient, auth_headers):
        import uuid
        with MOCK_INDEX:
            resp = await client.put(
                f"{BASE}/{uuid.uuid4()}",
                json={"name": "X"},
                headers=auth_headers,
            )
        assert resp.status_code == 404


@pytest.mark.asyncio
class TestDeletePlaybook:
    async def test_unauthenticated_returns_401(self, client: AsyncClient, test_playbook):
        resp = await client.delete(f"{BASE}/{test_playbook.id}")
        assert resp.status_code == 401

    async def test_delete_own_playbook(
        self, client: AsyncClient, auth_headers, test_playbook: Playbook
    ):
        with MOCK_INDEX:
            resp = await client.delete(f"{BASE}/{test_playbook.id}", headers=auth_headers)
        assert resp.status_code == 200
        assert "silindi" in resp.json()["message"]

        # Confirm it's gone
        get_resp = await client.get(f"{BASE}/{test_playbook.id}", headers=auth_headers)
        assert get_resp.status_code == 404

    async def test_delete_nonexistent_returns_404(self, client: AsyncClient, auth_headers):
        import uuid
        with MOCK_INDEX:
            resp = await client.delete(f"{BASE}/{uuid.uuid4()}", headers=auth_headers)
        assert resp.status_code == 404
