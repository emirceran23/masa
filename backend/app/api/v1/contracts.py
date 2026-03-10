"""Sözleşme yönetimi API endpoint'leri."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/contracts", tags=["contracts"])


class ContractUploadResponse(BaseModel):
    """Sözleşme yükleme yanıt modeli."""

    id: str
    filename: str
    status: str
    message: str


@router.post("/upload", response_model=ContractUploadResponse)
async def upload_contract(file: UploadFile = File(...)):
    """Sözleşme dosyası yükleme (PDF veya DOCX)."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Dosya adı belirtilmedi.")

    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen dosya formatı: {file.content_type}. Sadece PDF ve DOCX kabul edilir.",
        )

    # TODO: Dosyayı MinIO'ya yükle
    # TODO: Veritabanında kayıt oluştur
    # TODO: Ingestion Agent'ı tetikle

    return ContractUploadResponse(
        id="placeholder-id",
        filename=file.filename,
        status="uploaded",
        message="Sözleşme başarıyla yüklendi. İşleme alınacak.",
    )


@router.get("/")
async def list_contracts():
    """Tüm sözleşmeleri listele."""
    # TODO: Veritabanından sözleşmeleri çek
    return {"contracts": [], "total": 0}


@router.get("/{contract_id}")
async def get_contract(contract_id: str):
    """Belirli bir sözleşmenin detaylarını getir."""
    # TODO: Veritabanından sözleşmeyi çek
    return {"id": contract_id, "status": "not_found"}
