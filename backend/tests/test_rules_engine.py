"""Unit tests for the deterministic rule engine (rules/engine.py + rules/validators.py)."""

from __future__ import annotations

import uuid

import pytest

from app.rules.engine import cross_validate, evaluate_rules
from app.rules.validators import (
    extract_percentages,
    is_semantically_close,
    validate_semantic_match,
    validate_threshold,
)


def _rule(
    rule_type: str,
    content: str = "",
    distance: float = 0.1,
    threshold_value: float | None = None,
) -> dict:
    return {
        "rule_id": uuid.uuid4(),
        "rule_type": rule_type,
        "content": content or f"Rule {rule_type}",
        "distance": distance,
        "threshold_value": threshold_value,
    }


class TestExtractPercentages:
    def test_parses_simple_percentage(self):
        assert extract_percentages("Cezai şart %15'tir.") == [15.0]

    def test_handles_comma_decimal(self):
        assert extract_percentages("Oran %12,5 olarak belirlenmiştir.") == [12.5]

    def test_multiple_percentages(self):
        result = extract_percentages("İlk yıl %5 ikinci yıl %10 olacak.")
        assert set(result) == {5.0, 10.0}

    def test_no_percentage_returns_empty(self):
        assert extract_percentages("Bu metinde sayı yok.") == []


class TestIsSemanticallyClose:
    def test_close_returns_true(self):
        assert is_semantically_close(0.2) is True

    def test_far_returns_false(self):
        assert is_semantically_close(0.8) is False

    def test_boundary(self):
        assert is_semantically_close(0.35) is True
        assert is_semantically_close(0.3501) is False


class TestValidateThreshold:
    def test_returns_none_without_threshold(self):
        rule = _rule("rejected", content="No threshold")
        assert validate_threshold("abc", rule) is None

    def test_returns_none_when_clause_has_no_number(self):
        rule = _rule("threshold", threshold_value=15.0)
        assert validate_threshold("Hiç rakam yok.", rule) is None

    def test_detects_exceed(self):
        rule = _rule("threshold", threshold_value=15.0)
        match = validate_threshold("Cezai şart %20'dir.", rule)
        assert match is not None
        assert match.threshold_exceeded is True
        assert match.detected_value == 20.0

    def test_within_threshold_not_flagged(self):
        rule = _rule("threshold", threshold_value=15.0)
        match = validate_threshold("Cezai şart %10'dur.", rule)
        assert match is not None
        assert match.threshold_exceeded is False


class TestValidateSemanticMatch:
    def test_close_rule_matches(self):
        rule = _rule("rejected", distance=0.2)
        match = validate_semantic_match("some clause text", rule)
        assert match is not None
        assert match.rule_type == "rejected"

    def test_far_rule_does_not_match(self):
        rule = _rule("acceptable", distance=0.9)
        match = validate_semantic_match("some clause text", rule)
        assert match is None


class TestCrossValidate:
    def test_rejected_match_escalates_to_high(self):
        rejected_rule = _rule("rejected", distance=0.1, content="Sınırsız sorumluluk yasak.")

        result = cross_validate(
            llm_risk_level="low",
            llm_commercial=0.3,
            llm_legal=0.4,
            llm_rationale="Maddenin standart olduğu düşünülmektedir.",
            llm_policy_compliance=True,
            clause_text="Sınırsız sorumluluk kabul edilmiştir.",
            candidate_rules=[rejected_rule],
        )

        assert result.risk_level == "high"
        assert result.policy_compliance is False
        assert result.cross_validated is True
        assert "Yasaklı kuralla eşleşti" in result.rationale

    def test_threshold_exceeded_escalates_to_high(self):
        threshold_rule = _rule(
            "threshold", distance=0.1, threshold_value=15.0, content="Cezai şart %15'i geçmez."
        )

        result = cross_validate(
            llm_risk_level="medium",
            llm_commercial=0.5,
            llm_legal=0.5,
            llm_rationale="LLM gerekçesi.",
            llm_policy_compliance=True,
            clause_text="Cezai şart %30 olarak belirlenmiştir.",
            candidate_rules=[threshold_rule],
        )

        assert result.risk_level == "high"
        assert result.policy_compliance is False
        assert result.cross_validated is True

    def test_threshold_within_limit_does_not_escalate(self):
        threshold_rule = _rule(
            "threshold", distance=0.1, threshold_value=15.0, content="Cezai şart %15'i geçmez."
        )

        result = cross_validate(
            llm_risk_level="low",
            llm_commercial=0.2,
            llm_legal=0.2,
            llm_rationale="OK",
            llm_policy_compliance=True,
            clause_text="Cezai şart %10 olarak belirlenmiştir.",
            candidate_rules=[threshold_rule],
        )

        assert result.risk_level == "low"
        assert result.policy_compliance is True

    def test_no_rules_passthrough(self):
        result = cross_validate(
            llm_risk_level="medium",
            llm_commercial=0.5,
            llm_legal=0.5,
            llm_rationale="LLM değerlendirmesi.",
            llm_policy_compliance=True,
            clause_text="Bir madde.",
            candidate_rules=[],
        )
        assert result.risk_level == "medium"
        assert result.matches == []
        assert result.cross_validated is False

    def test_scores_are_clipped_to_unit_interval(self):
        result = cross_validate(
            llm_risk_level="low",
            llm_commercial=1.8,
            llm_legal=-0.3,
            llm_rationale="",
            llm_policy_compliance=True,
            clause_text="x",
            candidate_rules=[],
        )
        assert 0.0 <= result.commercial_score <= 1.0
        assert 0.0 <= result.legal_score <= 1.0


class TestEvaluateRules:
    def test_mix_of_matches_and_misses(self):
        rules = [
            _rule("rejected", distance=0.1),
            _rule("acceptable", distance=0.9),  # too far
            _rule("threshold", distance=0.1, threshold_value=10.0),
        ]
        matches = evaluate_rules("Madde metni %25 içeriyor.", rules)
        types = {m.rule_type for m in matches}
        assert "rejected" in types
        assert "threshold" in types
        assert "acceptable" not in types
