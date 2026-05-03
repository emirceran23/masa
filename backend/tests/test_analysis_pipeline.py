"""Integration tests — full analysis pipeline (Clause Agent + Risk Phase).

All external I/O is mocked:
  * OpenAI (clause agent LLM + risk agent LLM)
  * pgvector / embeddings (search_similar_rules, embed_text)
  * WebSocket / Redis (progress side-channels)
  * MinIO (startup fixture only)

The DB layer uses the real SQLite-backed in-memory session from conftest so we
actually persist rows and can assert on them.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.agents.schemas.clause_schema import ClauseAgentOutput, ClauseItem
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.risk_assessment import RiskAssessment
from app.services.analysis_service import start_analysis


# ── Helpers / stubs ───────────────────────────────────────────


def _fake_clause_items(n: int = 2) -> list[ClauseItem]:
    """Produce n synthetic clauses for mocking run_clause_agent."""
    return [
        ClauseItem(
            sequence_no=i,
            original_text=f"Madde {i}: Taraflar bu hüküme uymayı taahhüt eder.",
            category="gizlilik" if i % 2 == 0 else "fesih",
            confidence_score=0.9,
        )
        for i in range(1, n + 1)
    ]


def _fake_risk_llm_response(risk_level: str = "low") -> str:
    import json

    return json.dumps(
        {
            "risk_level": risk_level,
            "commercial_score": 0.2 if risk_level == "low" else 0.8,
            "legal_score": 0.3 if risk_level == "low" else 0.7,
            "rationale": "Otomatik test gerekçesi.",
            "policy_compliance": risk_level != "high",
            "matched_rule_ids": [],
        }
    )


def _fake_missing_llm_response() -> str:
    import json

    return json.dumps({"missing": []})


def _make_openai_chat_response(content: str) -> MagicMock:
    choice = MagicMock()
    choice.message.content = content
    resp = MagicMock()
    resp.choices = [choice]
    return resp


# ── Fixtures ──────────────────────────────────────────────────


@pytest_asyncio.fixture
async def processing_contract(_session_factory, test_user) -> Contract:
    """A contract in 'uploaded' state with raw text ready for analysis."""
    async with _session_factory() as session:
        contract = Contract(
            id=uuid.uuid4(),
            user_id=test_user.id,
            file_name="integration_test.pdf",
            storage_path="tests/integration_test.pdf",
            file_format="pdf",
            file_size=2048,
            raw_text=(
                "Madde 1: Taraflar bu gizlilik sözleşmesine uymayı taahhüt eder.\n"
                "Madde 2: Fesih bildirimi 30 gün önceden yapılmalıdır.\n"
                "Madde 3: Uyuşmazlıklar İstanbul Tahkim Merkezi'nde çözülecektir."
            ),
            status="uploaded",
            total_clauses=0,
        )
        session.add(contract)
        await session.commit()
        await session.refresh(contract)
        return contract


# ── Tests ─────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestAnalysisPipelineEndToEnd:
    """Full pipeline: uploaded → analyzed, clauses + risk_assessments persisted."""

    async def _run_pipeline(self, session_factory, contract, playbook_id=None):
        """Helper: run start_analysis inside a session with all external I/O mocked."""
        clause_items = _fake_clause_items(2)

        mock_openai_client = AsyncMock()
        mock_openai_client.chat.completions.create = AsyncMock(
            side_effect=[
                # Risk Agent call for clause 1
                _make_openai_chat_response(_fake_risk_llm_response("low")),
                # Risk Agent call for clause 2
                _make_openai_chat_response(_fake_risk_llm_response("medium")),
                # Missing-provisions call (only when playbook supplied)
                _make_openai_chat_response(_fake_missing_llm_response()),
            ]
        )

        async with session_factory() as session:
            with (
                patch(
                    "app.agents.clause_agent.run_clause_agent",
                    new_callable=AsyncMock,
                    return_value=clause_items,
                ),
                patch(
                    "app.agents.risk_agent._get_client",
                    return_value=mock_openai_client,
                ),
                patch(
                    "app.rag.vector_store.embed_text",
                    new_callable=AsyncMock,
                    return_value=[0.1] * 1536,
                ),
                patch(
                    "app.rag.vector_store.search_similar_rules",
                    new_callable=AsyncMock,
                    return_value=[],
                ),
                patch(
                    "app.core.websocket_manager.ws_manager.send_progress",
                    new_callable=AsyncMock,
                ),
                patch(
                    "app.core.redis.set_analysis_progress",
                    new_callable=AsyncMock,
                ),
            ):
                try:
                    await start_analysis(
                        session,
                        contract_id=contract.id,
                        user_id=contract.user_id,
                        playbook_id=playbook_id,
                    )
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise

    async def test_contract_status_becomes_analyzed(
        self, _session_factory, processing_contract
    ):
        await self._run_pipeline(_session_factory, processing_contract)

        async with _session_factory() as session:
            contract = (
                await session.execute(
                    select(Contract).where(Contract.id == processing_contract.id)
                )
            ).scalar_one()

        assert contract.status == "analyzed"
        assert contract.analyzed_at is not None
        assert contract.total_clauses == 2

    async def test_clause_rows_are_persisted(
        self, _session_factory, processing_contract
    ):
        await self._run_pipeline(_session_factory, processing_contract)

        async with _session_factory() as session:
            rows = (
                await session.execute(
                    select(Clause)
                    .where(Clause.contract_id == processing_contract.id)
                    .order_by(Clause.sequence_no)
                )
            ).scalars().all()

        assert len(rows) == 2
        assert rows[0].sequence_no == 1
        assert rows[1].sequence_no == 2
        assert rows[0].category in ("gizlilik", "fesih")

    async def test_risk_assessments_are_persisted(
        self, _session_factory, processing_contract
    ):
        await self._run_pipeline(_session_factory, processing_contract)

        async with _session_factory() as session:
            clauses = (
                await session.execute(
                    select(Clause).where(Clause.contract_id == processing_contract.id)
                )
            ).scalars().all()
            clause_ids = [c.id for c in clauses]

            risks = (
                await session.execute(
                    select(RiskAssessment).where(
                        RiskAssessment.clause_id.in_(clause_ids)
                    )
                )
            ).scalars().all()

        assert len(risks) == 2
        risk_levels = {r.risk_level for r in risks}
        assert risk_levels <= {"low", "medium", "high"}

    async def test_already_processing_raises_error(
        self, _session_factory, processing_contract
    ):
        """Re-triggering analysis on a processing contract must raise BadRequestError."""
        from app.core.exceptions import BadRequestError

        async with _session_factory() as session:
            contract = (
                await session.execute(
                    select(Contract).where(Contract.id == processing_contract.id)
                )
            ).scalar_one()
            contract.status = "processing"
            await session.commit()

        async with _session_factory() as session:
            with pytest.raises(BadRequestError):
                await start_analysis(
                    session,
                    contract_id=processing_contract.id,
                    user_id=processing_contract.user_id,
                )

    async def test_missing_contract_raises_not_found(
        self, _session_factory, test_user
    ):
        from app.core.exceptions import NotFoundError

        async with _session_factory() as session:
            with pytest.raises(NotFoundError):
                await start_analysis(
                    session,
                    contract_id=uuid.uuid4(),  # non-existent
                    user_id=test_user.id,
                )


@pytest.mark.asyncio
class TestRiskPhaseAlone:
    """Unit-level tests for run_risk_phase without going through start_analysis."""

    async def test_run_risk_phase_creates_assessments(
        self, _session_factory, test_contract
    ):
        """run_risk_phase should write RiskAssessment rows for every clause."""
        from app.agents.orchestrator import run_risk_phase
        from app.models.clause import Clause

        # Seed two clauses on the test_contract
        async with _session_factory() as session:
            for seq in range(1, 3):
                session.add(
                    Clause(
                        contract_id=test_contract.id,
                        sequence_no=seq,
                        original_text=f"Test madde {seq}.",
                        category="gizlilik",
                        confidence_score=0.95,
                    )
                )
            await session.commit()

        mock_openai_client = AsyncMock()
        mock_openai_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_chat_response(_fake_risk_llm_response("medium"))
        )

        async with _session_factory() as session:
            with (
                patch(
                    "app.agents.risk_agent._get_client",
                    return_value=mock_openai_client,
                ),
                patch(
                    "app.rag.vector_store.embed_text",
                    new_callable=AsyncMock,
                    return_value=[0.0] * 1536,
                ),
                patch(
                    "app.rag.vector_store.search_similar_rules",
                    new_callable=AsyncMock,
                    return_value=[],
                ),
            ):
                summary = await run_risk_phase(
                    session,
                    contract_id=test_contract.id,
                    playbook_id=None,
                )
                await session.commit()

        assert summary.total_clauses == 2
        assert summary.evaluated == 2
        assert summary.medium_count == 2

    async def test_run_risk_phase_upserts_on_rerun(
        self, _session_factory, test_contract
    ):
        """Running risk phase twice on the same contract should upsert, not duplicate."""
        from app.agents.orchestrator import run_risk_phase

        # Seed one clause
        async with _session_factory() as session:
            session.add(
                Clause(
                    contract_id=test_contract.id,
                    sequence_no=1,
                    original_text="Tek madde.",
                    category="diger",
                    confidence_score=0.8,
                )
            )
            await session.commit()

        mock_openai_client = AsyncMock()
        mock_openai_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_chat_response(_fake_risk_llm_response("low"))
        )

        patches = (
            patch("app.agents.risk_agent._get_client", return_value=mock_openai_client),
            patch(
                "app.rag.vector_store.embed_text",
                new_callable=AsyncMock,
                return_value=[0.0] * 1536,
            ),
            patch(
                "app.rag.vector_store.search_similar_rules",
                new_callable=AsyncMock,
                return_value=[],
            ),
        )

        for _ in range(2):
            mock_openai_client.chat.completions.create = AsyncMock(
                return_value=_make_openai_chat_response(_fake_risk_llm_response("low"))
            )
            async with _session_factory() as session:
                with patches[0], patches[1], patches[2]:
                    await run_risk_phase(session, contract_id=test_contract.id, playbook_id=None)
                    await session.commit()

        async with _session_factory() as session:
            clauses = (
                await session.execute(
                    select(Clause).where(Clause.contract_id == test_contract.id)
                )
            ).scalars().all()
            clause_ids = [c.id for c in clauses]
            risks = (
                await session.execute(
                    select(RiskAssessment).where(
                        RiskAssessment.clause_id.in_(clause_ids)
                    )
                )
            ).scalars().all()

        # One row per clause, not doubled
        assert len(risks) == len(clause_ids)
