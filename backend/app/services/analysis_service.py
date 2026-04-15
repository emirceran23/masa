"""Analysis service — orchestrates the full contract analysis pipeline."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.clause_agent import run_clause_agent
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.redis import set_analysis_progress
from app.core.websocket_manager import ws_manager
from app.models.clause import Clause
from app.models.contract import Contract

logger = logging.getLogger(__name__)


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
    if not contract.raw_text:
        raise BadRequestError("Sözleşme metni çıkarılamadı. Lütfen dosyayı tekrar yükleyin.")
    if contract.status == "processing":
        raise BadRequestError("Bu sözleşme zaten analiz ediliyor.")

    # ── Mark as processing ───────────────────────────────
    contract.status = "processing"
    if playbook_id:
        contract.playbook_id = playbook_id
    await db.flush()

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
        contract.status = "analyzed"
        contract.analyzed_at = datetime.now(timezone.utc)
        await db.flush()

        await ws_manager.send_progress(cid, "completed", 100, "Analiz tamamlandı.")
        await set_analysis_progress(cid, {"status": "completed", "progress": 100})

    except Exception as exc:
        logger.exception("Analysis failed for contract %s", contract_id)
        contract.status = "error"
        await db.flush()
        await ws_manager.send_progress(cid, "error", 0, f"Analiz hatası: {exc}")
        await set_analysis_progress(cid, {"status": "error", "progress": 0, "error": str(exc)})
        raise
