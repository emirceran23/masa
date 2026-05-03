"""Unit tests for Negotiation Agent and diff utility."""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.utils.diff import compute_diff_html, similarity_ratio


# ── Diff utility tests ────────────────────────────────────────

class TestComputeDiffHtml:
    def test_identical_texts_no_markup(self):
        result = compute_diff_html("Madde bir.", "Madde bir.")
        assert "<ins" not in result
        assert "<del" not in result
        assert "Madde bir." in result

    def test_insertion_marked_with_ins(self):
        result = compute_diff_html("ödeme yapılır.", "ödeme peşin yapılır.")
        assert '<ins class="diff-ins">' in result
        assert "peşin" in result

    def test_deletion_marked_with_del(self):
        result = compute_diff_html("sorumsuzluk hükmü geçerlidir.", "hükmü geçerlidir.")
        assert '<del class="diff-del">' in result
        assert "sorumsuzluk" in result

    def test_replacement_has_both_tags(self):
        result = compute_diff_html("high risk", "low risk")
        assert "diff-del" in result
        assert "diff-ins" in result

    def test_html_escaping(self):
        result = compute_diff_html("a < b", "a > b")
        assert "<" not in result.replace("<del", "").replace("<ins", "").replace("</del>", "").replace("</ins>", "")

    def test_empty_original(self):
        result = compute_diff_html("", "yeni metin")
        assert '<ins class="diff-ins">' in result

    def test_empty_revised(self):
        result = compute_diff_html("eski metin", "")
        assert '<del class="diff-del">' in result


class TestSimilarityRatio:
    def test_identical_is_one(self):
        assert similarity_ratio("abc", "abc") == 1.0

    def test_completely_different_is_low(self):
        assert similarity_ratio("aaaa", "bbbb") < 0.5

    def test_partial_overlap(self):
        ratio = similarity_ratio("Madde 1: ödeme yapılır.", "Madde 1: ödeme peşin yapılır.")
        assert 0.5 < ratio < 1.0


# ── Negotiation Agent tests ───────────────────────────────────

def _fake_clause(risk_level: str = "high") -> MagicMock:
    clause = MagicMock()
    clause.id = uuid.uuid4()
    clause.sequence_no = 1
    clause.original_text = "Taraflardan biri sözleşmeyi istediği zaman feshedebilir."
    clause.category = "fesih"
    return clause


def _fake_risk_assessment(risk_level: str = "high") -> MagicMock:
    ra = MagicMock()
    ra.risk_level = risk_level
    ra.rationale = "Tek taraflı fesih hakkı yüksek risk taşır."
    return ra


def _make_openai_response(content: str) -> MagicMock:
    import json
    choice = MagicMock()
    choice.message.content = content
    resp = MagicMock()
    resp.choices = [choice]
    return resp


@pytest.mark.asyncio
class TestNegotiationAgent:
    async def test_low_risk_returns_none(self):
        from app.agents.negotiation_agent import run_negotiation_agent

        clause = _fake_clause()
        ra = _fake_risk_assessment("low")
        db = AsyncMock()

        result = await run_negotiation_agent(db, clause, ra, playbook_id=None)
        assert result is None

    async def test_high_risk_returns_suggestion(self):
        import json
        from app.agents.negotiation_agent import run_negotiation_agent

        clause = _fake_clause("high")
        ra = _fake_risk_assessment("high")
        db = AsyncMock()

        fake_response = json.dumps({
            "suggested_text": "Fesih bildirimi 30 gün önceden yazılı olarak yapılır.",
            "context_used": "Tek taraflı fesih hakkı dengeli hale getirildi.",
        })

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response(fake_response)
        )

        with (
            patch("app.agents.negotiation_agent._get_client", return_value=mock_client),
            patch(
                "app.rag.retriever.retrieve_relevant_rules",
                new_callable=AsyncMock,
                return_value=[],
            ),
        ):
            result = await run_negotiation_agent(db, clause, ra, playbook_id=None)

        assert result is not None
        assert "30 gün" in result.suggested_text
        assert result.context_used

    async def test_medium_risk_returns_suggestion(self):
        import json
        from app.agents.negotiation_agent import run_negotiation_agent

        clause = _fake_clause("medium")
        ra = _fake_risk_assessment("medium")
        db = AsyncMock()

        fake_response = json.dumps({
            "suggested_text": "Ödeme 30 gün içinde yapılır; gecikme halinde aylık %1 faiz uygulanır.",
            "context_used": "Gecikme faizi oranı sınırlandırıldı.",
        })
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response(fake_response)
        )

        with (
            patch("app.agents.negotiation_agent._get_client", return_value=mock_client),
            patch(
                "app.rag.retriever.retrieve_relevant_rules",
                new_callable=AsyncMock,
                return_value=[],
            ),
        ):
            result = await run_negotiation_agent(db, clause, ra, playbook_id=None)

        assert result is not None

    async def test_malformed_llm_response_returns_none(self):
        from app.agents.negotiation_agent import run_negotiation_agent

        clause = _fake_clause("high")
        ra = _fake_risk_assessment("high")
        db = AsyncMock()

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response("not valid json {{{")
        )

        with (
            patch("app.agents.negotiation_agent._get_client", return_value=mock_client),
            patch(
                "app.rag.retriever.retrieve_relevant_rules",
                new_callable=AsyncMock,
                return_value=[],
            ),
        ):
            result = await run_negotiation_agent(db, clause, ra, playbook_id=None)

        assert result is None
