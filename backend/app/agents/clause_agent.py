"""Clause Agent — parses contract text into clauses and classifies each one."""

from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI

from app.config import settings
from app.agents.prompts.clause_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.agents.schemas.clause_schema import ClauseAgentOutput, ClauseItem

logger = logging.getLogger(__name__)

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


async def run_clause_agent(contract_text: str) -> list[ClauseItem]:
    """Send the contract text to GPT-4o, get structured clause list back.

    Uses OpenAI's JSON mode / structured outputs for reliable parsing.
    """
    client = _get_client()

    user_message = USER_PROMPT_TEMPLATE.format(contract_text=contract_text)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content
    logger.info("Clause Agent raw response length: %d", len(raw or ""))

    try:
        data = json.loads(raw)
        output = ClauseAgentOutput.model_validate(data)
    except Exception:
        logger.exception("Failed to parse Clause Agent output")
        raise ValueError("Clause Agent çıktısı ayrıştırılamadı. Lütfen tekrar deneyin.")

    # Enforce confidence threshold → mark as 'belirsiz'
    for clause in output.clauses:
        if clause.confidence_score < 0.7:
            clause.category = "belirsiz"

    return output.clauses
