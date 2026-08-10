"""Orchestrator — coordinates Clause → Risk → Negotiation agents over a contract.

Phase 3 adds the Negotiation Agent: after risk assessments are written, every
medium/high clause gets a revision suggestion persisted to the `revisions` table.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.negotiation_agent import run_negotiation_agent
from app.agents.risk_agent import detect_missing_provisions, run_risk_agent
from app.models.clause import Clause
from app.models.revision import Revision
from app.models.risk_assessment import RiskAssessment
from app.rag.vector_store import index_clause
from app.utils.diff import compute_diff_html

logger = logging.getLogger(__name__)


@dataclass
class AnalysisSummary:
    total_clauses: int
    evaluated: int
    high_count: int
    medium_count: int
    low_count: int
    missing_provisions: int
    revisions_proposed: int = field(default=0)


# Keep the old name as an alias so existing callers don't break.
RiskPhaseSummary = AnalysisSummary


async def _index_clause_embeddings(db: AsyncSession, clauses: list[Clause]) -> None:
    for clause in clauses:
        try:
            async with db.begin_nested():
                await index_clause(db, clause.id, clause.original_text)
        except Exception:
            logger.exception("Clause embedding failed for %s — continuing", clause.id)


async def run_risk_phase(
    db: AsyncSession,
    contract_id: uuid.UUID,
    playbook_id: uuid.UUID | None,
    progress_callback=None,
) -> AnalysisSummary:
    """Run Risk + Negotiation phases for every clause of a contract."""

    stmt = (
        select(Clause)
        .where(Clause.contract_id == contract_id)
        .order_by(Clause.sequence_no.asc())
    )
    clauses = (await db.execute(stmt)).scalars().all()

    # ── Clause embedding ────────────────────────────────────
    if progress_callback:
        await progress_callback("clause_indexing", 55, "Madde gömülmeleri indeksleniyor...")
    await _index_clause_embeddings(db, clauses)

    if progress_callback:
        await progress_callback("risk_analysis", 65, "Risk değerlendirmesi çalışıyor...")

    high = medium = low = 0
    risk_map: dict[uuid.UUID, RiskAssessment] = {}

    # ── Risk phase ──────────────────────────────────────────
    for idx, clause in enumerate(clauses, start=1):
        try:
            result = await run_risk_agent(db, clause, playbook_id)
        except Exception:
            logger.exception("Risk Agent failed for clause %s", clause.id)
            continue

        a = result.assessment
        existing = (
            await db.execute(
                select(RiskAssessment).where(RiskAssessment.clause_id == clause.id)
            )
        ).scalar_one_or_none()

        if existing:
            existing.risk_level = a.risk_level
            existing.commercial_score = a.commercial_score
            existing.legal_score = a.legal_score
            existing.rationale = a.rationale
            existing.policy_compliance = a.policy_compliance
            existing.cross_validated = a.cross_validated
            risk_map[clause.id] = existing
        else:
            ra = RiskAssessment(
                clause_id=clause.id,
                risk_level=a.risk_level,
                commercial_score=a.commercial_score,
                legal_score=a.legal_score,
                rationale=a.rationale,
                policy_compliance=a.policy_compliance,
                cross_validated=a.cross_validated,
            )
            db.add(ra)
            risk_map[clause.id] = ra

        if a.risk_level == "high":
            high += 1
        elif a.risk_level == "medium":
            medium += 1
        else:
            low += 1

        if progress_callback and clauses:
            pct = 65 + int(20 * idx / len(clauses))
            await progress_callback(
                "risk_analysis",
                pct,
                f"Risk değerlendiriliyor ({idx}/{len(clauses)})...",
            )

    await db.flush()

    # ── Missing provisions ──────────────────────────────────
    missing_count = 0
    if playbook_id:
        if progress_callback:
            await progress_callback("missing_provisions", 88, "Eksik hükümler taranıyor...")
        missing = await detect_missing_provisions(db, contract_id, playbook_id, list(clauses))
        if missing:
            await _persist_missing_provisions(db, contract_id, missing)
            missing_count = len(missing)

    # ── Negotiation phase ───────────────────────────────────
    if progress_callback:
        await progress_callback("negotiation", 92, "Revizyon önerileri üretiliyor...")

    revisions_proposed = 0
    for clause in clauses:
        ra = risk_map.get(clause.id)
        if ra is None or ra.risk_level == "low":
            continue
        try:
            output = await run_negotiation_agent(db, clause, ra, playbook_id)
        except Exception:
            logger.exception("Negotiation Agent failed for clause %s", clause.id)
            continue

        if output is None:
            continue

        diff_html = compute_diff_html(clause.original_text, output.suggested_text)

        # Delete any prior pending revision to avoid duplicates on re-run.
        await db.execute(
            text(
                "DELETE FROM revisions WHERE clause_id = :cid AND status = 'pending'"
            ),
            {"cid": clause.id},
        )
        db.add(
            Revision(
                clause_id=clause.id,
                suggested_text=output.suggested_text,
                context_used=output.context_used,
                diff_html=diff_html,
                status="pending",
            )
        )
        revisions_proposed += 1

    await db.flush()

    return AnalysisSummary(
        total_clauses=len(clauses),
        evaluated=high + medium + low,
        high_count=high,
        medium_count=medium,
        low_count=low,
        missing_provisions=missing_count,
        revisions_proposed=revisions_proposed,
    )


async def _persist_missing_provisions(
    db: AsyncSession,
    contract_id: uuid.UUID,
    items: list[dict],
) -> None:
    await db.execute(
        text("DELETE FROM missing_provisions WHERE contract_id = :cid"),
        {"cid": contract_id},
    )
    for item in items:
        await db.execute(
            text(
                "INSERT INTO missing_provisions (contract_id, playbook_rule_id, description) "
                "VALUES (:cid, :rid, :desc)"
            ),
            {
                "cid": contract_id,
                "rid": item["playbook_rule_id"],
                "desc": item["description"],
            },
        )
