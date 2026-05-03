"""Report & export endpoints.

POST /contracts/{id}/reports         — generate a report (PDF or DOCX)
GET  /contracts/{id}/reports         — list reports for a contract
GET  /reports/{id}/download          — download a previously generated report
GET  /contracts/{id}/export          — export revised contract DOCX (inline download)
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.report import ReportGenerateRequest, ReportResponse
from app.services import export_service, report_service
from app.storage.minio_client import download_file

router = APIRouter(tags=["Reports"])

# ── Report generation ─────────────────────────────────────────────────────────


@router.post(
    "/contracts/{contract_id}/reports",
    response_model=ReportResponse,
    status_code=201,
)
async def generate_report(
    contract_id: UUID,
    body: ReportGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Analiz edilmiş sözleşme için PDF veya DOCX rapor oluşturur."""
    report = await report_service.generate_report(
        db,
        contract_id=contract_id,
        user_id=current_user.id,
        report_type=body.report_type,
        fmt=body.fmt,
    )
    await db.commit()
    return ReportResponse.model_validate(report)


@router.get("/contracts/{contract_id}/reports", response_model=list[ReportResponse])
async def list_reports(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Sözleşme için oluşturulan raporları listeler."""
    reports = await report_service.list_reports(db, contract_id, current_user.id)
    return [ReportResponse.model_validate(r) for r in reports]


@router.get("/reports/{report_id}/download")
async def download_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Önceden oluşturulmuş bir raporu indirir."""
    report = await report_service.get_report(db, report_id, current_user.id)
    if not report.storage_path:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Rapor dosyası bulunamadı.")

    # storage_path = "bucket/object_name" — strip bucket prefix
    object_name = report.storage_path.split("/", 1)[1]

    file_bytes = download_file(object_name)

    is_pdf = object_name.endswith(".pdf")
    media_type = "application/pdf" if is_pdf else (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    ext = "pdf" if is_pdf else "docx"
    filename = f"report_{report.report_type}_{str(report.id)[:8]}.{ext}"

    return Response(
        content=file_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Contract export ───────────────────────────────────────────────────────────


@router.get("/contracts/{contract_id}/export")
async def export_contract(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kabul edilen revizyonlar uygulanmış sözleşmeyi DOCX olarak indirir."""
    file_bytes, _ = await export_service.export_revised_contract(
        db, contract_id, current_user.id
    )
    # No DB commit needed — export doesn't persist a new row

    media_type = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    filename = f"revised_contract_{str(contract_id)[:8]}.docx"

    return Response(
        content=file_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
