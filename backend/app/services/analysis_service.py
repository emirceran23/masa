"""Analysis service — orchestrates the full contract analysis pipeline."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.clause_agent import run_clause_agent
from app.agents.orchestrator import run_risk_phase
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.redis import set_analysis_progress
from app.core.websocket_manager import ws_manager
from app.models.clause import Clause
from app.models.contract import Contract
from app.services.approval_service import promote_risky_clauses_to_review

logger = logging.getLogger(__name__)


async def validate_and_mark_processing(
    db: AsyncSession,
    contract_id: uuid.UUID,
    user_id: uuid.UUID,
    playbook_id: uuid.UUID | None = None,
) -> None:
    """Validate the contract and immediately set status to 'processing'.

    Called synchronously in the HTTP handler so the frontend sees the status
    change before the background task even starts.
    """
    stmt = select(Contract).where(Contract.id == contract_id, Contract.user_id == user_id)
    contract = (await db.execute(stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")
    if not contract.raw_text:
        raise BadRequestError("Sözleşme metni çıkarılamadı. Lütfen dosyayı tekrar yükleyin.")
    if contract.status == "processing":
        raise BadRequestError("Bu sözleşme zaten analiz ediliyor.")
    contract.status = "processing"
    if playbook_id:
        contract.playbook_id = playbook_id
    await db.flush()


async def start_analysis(
    db: AsyncSession,
    contract_id: uuid.UUID,
    user_id: uuid.UUID,
    playbook_id: uuid.UUID | None = None,
) -> None:
    """Run the full analysis pipeline for a contract.

    Phase 1 (this sprint): clause parsing + classification only.
    Phase 2 will add risk + negotiation agents.
    """
    # ── Fetch contract ───────────────────────────────────
    stmt = select(Contract).where(Contract.id == contract_id, Contract.user_id == user_id)
    contract = (await db.execute(stmt)).scalar_one_or_none()
    if not contract:
        raise NotFoundError("Sözleşme bulunamadı.")

    cid = str(contract_id)

    try:
        # ── Step 1: Clause Agent ─────────────────────────
        await ws_manager.send_progress(cid, "clause_parsing", 10, "Maddeler ayrıştırılıyor...")
        await set_analysis_progress(cid, {"status": "processing", "step": "clause_parsing", "progress": 10})

        clause_items = await run_clause_agent(contract.raw_text)

        await ws_manager.send_progress(
            cid, "clause_classification", 50,
            f"Sınıflandırma tamamlandı — {len(clause_items)} madde bulundu."
        )
        await set_analysis_progress(cid, {"status": "processing", "step": "clause_classification", "progress": 50})

        # ── Persist clauses ──────────────────────────────
        for item in clause_items:
            clause = Clause(
                contract_id=contract_id,
                sequence_no=item.sequence_no,
                original_text=item.original_text,
                category=item.category,
                confidence_score=item.confidence_score,
            )
            db.add(clause)

        contract.total_clauses = len(clause_items)
        await db.flush()

        # ── Step 2: Risk Phase (Clause embedding + Risk Agent + missing provisions) ──
        async def _progress(step: str, pct: int, msg: str) -> None:
            await ws_manager.send_progress(cid, step, pct, msg)
            await set_analysis_progress(cid, {"status": "processing", "step": step, "progress": pct})

        effective_playbook_id = contract.playbook_id or playbook_id
        risk_summary = await run_risk_phase(
            db,
            contract_id=contract_id,
            playbook_id=effective_playbook_id,
            progress_callback=_progress,
        )
        logger.info(
            "Risk phase complete for %s: %d high / %d medium / %d low · missing=%d",
            contract_id,
            risk_summary.high_count,
            risk_summary.medium_count,
            risk_summary.low_count,
            risk_summary.missing_provisions,
        )

        promoted = await promote_risky_clauses_to_review(db, contract_id)
        logger.info("Promoted %d clause(s) to in_review for contract %s", promoted, contract_id)

        contract.status = "analyzed"
        contract.analyzed_at = datetime.now(timezone.utc)
        await db.flush()

        await ws_manager.send_progress(cid, "completed", 100, "Analiz tamamlandı.")
        await set_analysis_progress(cid, {"status": "completed", "progress": 100})

    except Exception as exc:
        logger.exception("Analysis failed for contract %s", contract_id)
        await db.rollback()
        contract.status = "error"
        await db.commit()
        await ws_manager.send_progress(cid, "error", 0, f"Analiz hatası: {exc}")
        await set_analysis_progress(cid, {"status": "error", "progress": 0, "error": str(exc)})
        raise
