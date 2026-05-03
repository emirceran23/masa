"""Rule engine — cross-validates the LLM's risk output against deterministic rules.

The engine takes:
  * the LLM's Risk Agent output for a clause
  * the candidate playbook rules returned by RAG retrieval

and returns a (possibly escalated) final assessment plus the list of rules that
actually matched. This gives us a defensible, auditable layer on top of the LLM.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.rules.validators import (
    RuleMatch,
    validate_semantic_match,
    validate_threshold,
)


RISK_ORDER = {"low": 0, "medium": 1, "high": 2}
ORDER_RISK = {v: k for k, v in RISK_ORDER.items()}


@dataclass
class FinalAssessment:
    risk_level: str
    commercial_score: float
    legal_score: float
    rationale: str
    policy_compliance: bool
    cross_validated: bool
    matches: list[RuleMatch] = field(default_factory=list)


def _escalate(current: str, target: str) -> str:
    """Return the higher of the two risk levels."""
    if RISK_ORDER.get(target, -1) > RISK_ORDER.get(current, -1):
        return target
    return current


def evaluate_rules(clause_text: str, candidate_rules: list[dict]) -> list[RuleMatch]:
    """Run every rule through the right validator; return only the hits."""
    matches: list[RuleMatch] = []
    for rule in candidate_rules:
        if rule.get("rule_type") == "threshold":
            hit = validate_threshold(clause_text, rule)
        else:
            hit = validate_semantic_match(clause_text, rule)
        if hit:
            matches.append(hit)
    return matches


def cross_validate(
    llm_risk_level: str,
    llm_commercial: float,
    llm_legal: float,
    llm_rationale: str,
    llm_policy_compliance: bool,
    clause_text: str,
    candidate_rules: list[dict],
) -> FinalAssessment:
    """Merge LLM output with deterministic rule hits.

    Escalation rules (see data/seed/risk_rubric.json):
      * a 'rejected' rule match → high risk, policy_compliance = False
      * a 'threshold' rule with exceeded value → high risk, policy_compliance = False
      * any divergence between engine and LLM → cross_validated = True
    """
    matches = evaluate_rules(clause_text, candidate_rules)

    final_level = llm_risk_level if llm_risk_level in RISK_ORDER else "medium"
    final_compliance = llm_policy_compliance
    rationale_notes: list[str] = []
    engine_triggered = False

    for match in matches:
        if match.rule_type == "rejected":
            final_level = _escalate(final_level, "high")
            final_compliance = False
            engine_triggered = True
            rationale_notes.append(
                f"[Kural Motoru] Yasaklı kuralla eşleşti: {match.content.strip()}"
            )
        elif match.rule_type == "threshold" and match.threshold_exceeded:
            final_level = _escalate(final_level, "high")
            final_compliance = False
            engine_triggered = True
            rationale_notes.append(
                f"[Kural Motoru] Eşik aşıldı ({match.detected_value}% > "
                f"{match.threshold_value}%): {match.content.strip()}"
            )
        elif match.rule_type == "acceptable":
            # acceptable matches don't change level but signal compliance
            pass
        elif match.rule_type == "required":
            # A required rule appearing here means the clause at least covers the topic.
            # Missing-provision detection runs separately.
            pass

    cross_validated = engine_triggered and final_level != llm_risk_level

    rationale = llm_rationale.strip()
    if rationale_notes:
        rationale = rationale + "\n\n" + "\n".join(rationale_notes)

    return FinalAssessment(
        risk_level=final_level,
        commercial_score=max(0.0, min(1.0, llm_commercial)),
        legal_score=max(0.0, min(1.0, llm_legal)),
        rationale=rationale,
        policy_compliance=final_compliance,
        cross_validated=cross_validated,
        matches=matches,
    )
