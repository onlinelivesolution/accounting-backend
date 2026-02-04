from fastapi import APIRouter, Depends, Query
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.period__service import PeriodService
from src.services.interfaces.iperiod__service import IPeriodService
from src.depends.service_depends import get_period_service
from src.depends.service_depends import get_db_period_service
from src.services.database import get_async_db

router = APIRouter(prefix="/api/period", tags=["Accounting Period"]
)

@router.post("/create")
async def create_period(
    start: date = Query(...),
    end: date = Query(...),
    service: IPeriodService = Depends(get_period_service)
):
    return await service.create_period(start, end)

@router.post("/close")
async def close_period(
    end: date,
    db: AsyncSession = Depends(get_async_db),
    service: PeriodService = Depends(get_db_period_service),
):
    result = await service.close_period(end)
    await db.commit()     # ✅ REQUIRED
    return result

