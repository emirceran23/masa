"""Integration tests for /api/v1/contracts/{id}/risks and /missing-provisions."""

import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.models.clause import Clause
from app.models.contract import Contract
from app.models.risk_assessment import RiskAssessment


# ── Helpers ───────────────────────────────────────────────

async def _add_clause_with_risk(session_factory, contract_id, risk_level="high"):
    """Insert a clause + risk assessment directly into the DB."""
    async with session_factory() as session:
        clause = Clause(
            id=uuid.uuid4(),
            contract_id=contract_id,
            sequence_no=1,
            original_text="Taraflardan biri istediği zaman sözleşmeyi feshedebilir.",
            category="fesih",
            confidence_score=0.95,
        )
        session.add(clause)
        await session.flush()

        risk = RiskAssessment(
            id=uuid.uuid4(),
            clause_id=clause.id,
            risk_level=risk_level,
            commercial_score=0.8,
            legal_score=0.9,
            rationale="Tek taraflı fesih hakkı yüksek risk taşır.",
            policy_compliance=False,
            cross_validated=False,
        )
        session.add(risk)
        await session.commit()
        return clause, risk


@pytest.mark.asyncio
class TestListRisks:
    async def test_unauthenticated_returns_401(self, client: AsyncClient, test_contract: Contract):
        resp = await client.get(f"/api/v1/contracts/{test_contract.id}/risks")
        assert resp.status_code == 401

    async def test_empty_when_no_risk_agent_run(
        self, client: AsyncClient, auth_headers, test_contract: Contract
    ):
        resp = await client.get(
            f"/api/v1/contracts/{test_contract.id}/risks",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_risk_assessments(
        self, client: AsyncClient, auth_headers, test_contract: Contract, _session_factory
    ):
        _, risk = await _add_clause_with_risk(_session_factory, test_contract.id, "high")

        resp = await client.get(
            f"/api/v1/contracts/{test_contract.id}/risks",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["risk_level"] == "high"
        assert data[0]["policy_compliance"] is False
        assert "rationale" in data[0]

    async def test_returns_all_risk_levels(
        self, client: AsyncClient, auth_headers, test_contract: Contract, _session_factory
    ):
        await _add_clause_with_risk(_session_factory, test_contract.id, "low")

        resp = await client.get(
            f"/api/v1/contracts/{test_contract.id}/risks",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_nonexistent_contract_returns_404(
        self, client: AsyncClient, auth_headers
    ):
        resp = await client.get(
            f"/api/v1/contracts/{uuid.uuid4()}/risks",
            headers=auth_headers,
        )
        assert resp.status_code == 404

    async def test_cannot_access_other_users_contract(
        self, client: AsyncClient, _session_factory, test_user
    ):
        # Create a contract owned by a different user
        other_user_id = uuid.uuid4()
        async with _session_factory() as session:
            from app.models.user import User
            from app.core.security import hash_password
            other = User(
                id=other_user_id,
                email="riskother@lagent.dev",
                password_hash=hash_password("OtherPass123!@#"),
                full_name="Other User",
            )
            session.add(other)
            contract = Contract(
                id=uuid.uuid4(),
                user_id=other_user_id,
                file_name="other.pdf",
                storage_path="other/other.pdf",
                file_format="pdf",
                file_size=512,
                status="analyzed",
            )
            session.add(contract)
            await session.commit()
            other_contract_id = contract.id

        # Login as test_user (not the owner)
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@lagent.dev", "password": "TestPass123!@#"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        resp = await client.get(
            f"/api/v1/contracts/{other_contract_id}/risks",
            headers=headers,
        )
        assert resp.status_code == 404


@pytest.mark.asyncio
class TestMissingProvisions:
    async def test_unauthenticated_returns_401(
        self, client: AsyncClient, test_contract: Contract
    ):
        resp = await client.get(
            f"/api/v1/contracts/{test_contract.id}/missing-provisions"
        )
        assert resp.status_code == 401

    async def test_empty_before_risk_agent(
        self, client: AsyncClient, auth_headers, test_contract: Contract
    ):
        resp = await client.get(
            f"/api/v1/contracts/{test_contract.id}/missing-provisions",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_nonexistent_contract_returns_404(
        self, client: AsyncClient, auth_headers
    ):
        resp = await client.get(
            f"/api/v1/contracts/{uuid.uuid4()}/missing-provisions",
            headers=auth_headers,
        )
        assert resp.status_code == 404

    async def test_returns_provisions_inserted_by_risk_agent(
        self, client: AsyncClient, auth_headers, test_contract: Contract, _session_factory
    ):
        """Simulate the Risk Agent inserting a missing provision and verify the endpoint."""
        from sqlalchemy import text as sa_text

        async with _session_factory() as session:
            await session.execute(
                sa_text("""
                    INSERT INTO missing_provisions (contract_id, description)
                    VALUES (:cid, :desc)
                """),
                {"cid": str(test_contract.id), "desc": "Gizlilik maddesi eksik."},
            )
            await session.commit()

        resp = await client.get(
            f"/api/v1/contracts/{test_contract.id}/missing-provisions",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["description"] == "Gizlilik maddesi eksik."
