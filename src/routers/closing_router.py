from fastapi import APIRouter, Depends
from datetime import date
from src.services.closing_service import ClosingService
from src.repositories.closing_repository import ClosingRepository
from src.services.database import get_async_db

router = APIRouter(prefix="/api/closing", tags=["Closing"])

@router.post("/")
async def post_closing(
    closing_date: date,
    db=Depends(get_async_db),
):
    repo = ClosingRepository(db)
    service = ClosingService(repo, db)
    return await service.post_closing_journal(closing_date)
