from fastapi import APIRouter, Depends
from src.services.interfaces.ibalancesheet__service import IBalanceSheetService
from src.depends.service_depends import get_balance_sheet_service

router = APIRouter(prefix="/api/balance-sheet", tags=["Balance Sheet"]
)


@router.get("")
async def get_balance_sheet(
    service: IBalanceSheetService = Depends(get_balance_sheet_service),
):
    return await service.get_balance_sheet()
