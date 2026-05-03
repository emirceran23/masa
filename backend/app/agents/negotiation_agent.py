"""Negotiation Agent — proposes balanced revision text for risky clauses.

Only called for clauses with risk_level == 'medium' or 'high'.
Low-risk clauses are skipped (no revision needed).
"""

from __future__ import annotations

import json
import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.client import get_openai_client
from app.agents.prompts.negotiation_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.agents.schemas.negotiation_schema import NegotiationAgentOutput
from app.config import settings
from app.models.clause import Clause
from app.models.risk_assessment import RiskAssessment
from app.rag.retriever import retrieve_relevant_rules

logger = logging.getLogger(__name__)


def _format_rules_context(rules: list[dict]) -> str:
    if not rules:
        return "(Eşleşen kural bulunamadı.)"
    return "\n".join(
        f"- [{r['rule_type']}] {r['content']}" for r in rules
    )


async def run_negotiation_agent(
    db: AsyncSession,
    clause: Clause,
    risk_assessment: RiskAssessment,
    playbook_id: uuid.UUID | None,
) -> NegotiationAgentOutput | None:
    """Return a revision suggestion, or None if the clause is low-risk."""
    if risk_assessment.risk_level == "low":
        return None

    rules = await retrieve_relevant_rules(
        db,
        clause_text=clause.original_text,
        playbook_id=playbook_id,
        limit=3,
    )

    user_message = USER_PROMPT_TEMPLATE.format(
        sequence_no=clause.sequence_no,
        category=clause.category or "belirsiz",
        risk_level=risk_assessment.risk_level,
        rationale=risk_assessment.rationale,
        original_text=clause.original_text,
        rules_context=_format_rules_context(rules),
    )

    client = get_openai_client()
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
    logger.debug("Negotiation Agent output for clause %s: %s", clause.id, raw[:200])

    try:
        data = json.loads(raw)
        return NegotiationAgentOutput.model_validate(data)
    except Exception:
        logger.exception("Failed to parse Negotiation Agent output for clause %s", clause.id)
        return None
