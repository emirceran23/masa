"""Risk Agent — evaluates a single clause against playbook rules + rubric.

Pipeline per clause:
  1. Retrieve top-K semantically similar playbook rules via RAG.
  2. Ask GPT-4o to produce a structured risk assessment.
  3. Run the deterministic rule engine to cross-validate / escalate.

Missing-provision detection is a separate pass over the whole contract — see
detect_missing_provisions below.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.client import get_openai_client
from app.agents.prompts.risk_prompts import (
    MISSING_PROVISIONS_SYSTEM_PROMPT,
    MISSING_PROVISIONS_USER_PROMPT,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)
from app.agents.schemas.risk_schema import (
    MissingProvisionsOutput,
    RiskAgentOutput,
)
from app.config import settings
from app.models.clause import Clause
from app.models.playbook import PlaybookRule
from app.rag.retriever import retrieve_relevant_rules
from app.rules.engine import FinalAssessment, cross_validate

logger = logging.getLogger(__name__)


@dataclass
class ClauseRiskResult:
    clause_id: uuid.UUID
    assessment: FinalAssessment


# ── Helpers ────────────────────────────────────────────────

def _format_rules_block(rules: list[dict]) -> str:
    if not rules:
        return "(Eşleşen kural bulunamadı — genel değerlendirme yap.)"
    lines = []
    for r in rules:
        threshold = (
            f" (eşik: %{r['threshold_value']})" if r.get("threshold_value") is not None else ""
        )
        lines.append(
            f"- id={r['rule_id']} · tip={r['rule_type']}{threshold} · "
            f"mesafe={r['distance']:.3f}\n  {r['content']}"
        )
    return "\n".join(lines)


async def _call_llm(clause: Clause, rules: list[dict]) -> RiskAgentOutput:
    client = get_openai_client()
    user_message = USER_PROMPT_TEMPLATE.format(
        sequence_no=clause.sequence_no,
        category=clause.category or "belirsiz",
        clause_text=clause.original_text,
        rules_block=_format_rules_block(rules),
    )

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content or "{}"
    logger.debug("Risk Agent raw output for clause %s: %s", clause.id, raw[:200])

    try:
        data = json.loads(raw)
        return RiskAgentOutput.model_validate(data)
    except Exception:
        logger.exception("Failed to parse Risk Agent output for clause %s", clause.id)
        return RiskAgentOutput(
            risk_level="medium",
            commercial_score=0.5,
            legal_score=0.5,
            rationale="LLM çıktısı ayrıştırılamadı — otomatik olarak orta risk atandı.",
            policy_compliance=True,
            matched_rule_ids=[],
        )


# ── Public API ─────────────────────────────────────────────

async def run_risk_agent(
    db: AsyncSession,
    clause: Clause,
    playbook_id: uuid.UUID | None,
) -> ClauseRiskResult:
    """Evaluate a single clause and return the cross-validated FinalAssessment."""
    rules = await retrieve_relevant_rules(
        db,
        clause_text=clause.original_text,
        playbook_id=playbook_id,
        limit=5,
    )

    llm_output = await _call_llm(clause, rules)

    assessment = cross_validate(
        llm_risk_level=llm_output.risk_level,
        llm_commercial=llm_output.commercial_score,
        llm_legal=llm_output.legal_score,
        llm_rationale=llm_output.rationale,
        llm_policy_compliance=llm_output.policy_compliance,
        clause_text=clause.original_text,
        candidate_rules=rules,
    )

    return ClauseRiskResult(clause_id=clause.id, assessment=assessment)


async def detect_missing_provisions(
    db: AsyncSession,
    contract_id: uuid.UUID,
    playbook_id: uuid.UUID,
    clauses: list[Clause],
) -> list[dict]:
    """Return a list of {playbook_rule_id, description} for required rules with no clause coverage."""
    # Load required rules for the playbook
    stmt = select(PlaybookRule).where(
        PlaybookRule.playbook_id == playbook_id,
        PlaybookRule.rule_type == "required",
    )
    required_rules = (await db.execute(stmt)).scalars().all()
    if not required_rules:
        return []

    required_block = "\n".join(
        f"- id={r.id} · {r.content}" for r in required_rules
    )
    clauses_summary = "\n".join(
        f"- [{c.sequence_no}] kategori={c.category or 'belirsiz'} · "
        f"{c.original_text[:220].strip()}..."
        for c in clauses
    ) or "(Madde bulunamadı.)"

    client = get_openai_client()
    user_message = MISSING_PROVISIONS_USER_PROMPT.format(
        required_rules_block=required_block,
        clauses_summary_block=clauses_summary,
    )

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": MISSING_PROVISIONS_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content or "{}"
    try:
        data = json.loads(raw)
        parsed = MissingProvisionsOutput.model_validate(data)
    except Exception:
        logger.exception("Failed to parse missing-provisions output")
        return []

    required_ids = {r.id for r in required_rules}
    return [
        {
            "playbook_rule_id": item.playbook_rule_id,
            "description": item.description,
        }
        for item in parsed.missing
        if item.playbook_rule_id in required_ids
    ]
