from fastapi import APIRouter, Depends
from src.services.interfaces.itrialbalance__service import ITrialBalanceService
from src.depends.service_depends import get_trial_balance_service

router = APIRouter(prefix="/api/trial-balance", tags=["Trial Balance"]
)


@router.get("")
async def get_trial_balance(
    service: ITrialBalanceService = Depends(get_trial_balance_service),
):
    return await service.get_trial_balance()
