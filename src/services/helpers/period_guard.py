from fastapi import HTTPException, status
from src.repositories.interfaces.iperiod__repository import IPeriodRepository

async def ensure_open_period(period_repo: IPeriodRepository):
    period = await period_repo.get_open_period()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No open accounting period. Please open a period first."
        )
    return period
