"""Review (inceleme) API endpoint'leri."""

from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def list_reviews():
    """Tüm incelemeleri listele."""
    # TODO: Veritabanından incelemeleri çek
    return {"reviews": [], "total": 0}


@router.get("/{review_id}")
async def get_review(review_id: str):
    """Belirli bir incelemenin detaylarını getir."""
    # TODO: Review detaylarını çek
    return {"id": review_id, "status": "not_found"}


@router.get("/{review_id}/clauses")
async def get_review_clauses(review_id: str):
    """Bir incelemeye ait maddeleri ve risk skorlarını getir."""
    # TODO: İnceleme maddelerini çek
    return {"review_id": review_id, "clauses": []}
