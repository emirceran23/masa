"""Deterministic rule validators — thin heuristics that complement the LLM risk agent.

Each validator inspects a clause against a single playbook rule and returns either
a RuleMatch (hit) or None (no match). The engine aggregates the matches and
escalates risk accordingly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

RuleType = Literal["acceptable", "rejected", "required", "threshold"]


@dataclass(frozen=True)
class RuleMatch:
    rule_id: str
    rule_type: RuleType
    content: str
    distance: float
    threshold_value: float | None = None
    threshold_exceeded: bool = False
    detected_value: float | None = None


# ── Helpers ─────────────────────────────────────────────────

_NUMBER_PATTERN = re.compile(r"%\s*([0-9]+(?:[.,][0-9]+)?)")


def extract_percentages(text: str) -> list[float]:
    """Pull percentage values out of Turkish clause text (e.g. '%15', '%12,5')."""
    values: list[float] = []
    for match in _NUMBER_PATTERN.finditer(text):
        raw = match.group(1).replace(",", ".")
        try:
            values.append(float(raw))
        except ValueError:
            continue
    return values


def is_semantically_close(distance: float, max_distance: float = 0.35) -> bool:
    """pgvector cosine distance — lower is closer. 0.35 is a pragmatic cut-off."""
    return distance <= max_distance


# ── Validators ──────────────────────────────────────────────

def validate_threshold(clause_text: str, rule: dict) -> RuleMatch | None:
    """If the rule defines a numeric threshold, check whether the clause exceeds it."""
    threshold = rule.get("threshold_value")
    if threshold is None:
        return None

    values = extract_percentages(clause_text)
    if not values:
        return None

    max_value = max(values)
    exceeded = max_value > float(threshold)

    return RuleMatch(
        rule_id=str(rule["rule_id"]),
        rule_type="threshold",
        content=rule["content"],
        distance=float(rule.get("distance", 0.0)),
        threshold_value=float(threshold),
        threshold_exceeded=exceeded,
        detected_value=max_value,
    )


def validate_semantic_match(clause_text: str, rule: dict) -> RuleMatch | None:
    """Accept a non-threshold rule if it is semantically close to the clause."""
    distance = float(rule.get("distance", 1.0))
    if not is_semantically_close(distance):
        return None

    return RuleMatch(
        rule_id=str(rule["rule_id"]),
        rule_type=rule["rule_type"],
        content=rule["content"],
        distance=distance,
    )
