from fastapi import APIRouter, Depends, Query
from datetime import date
from typing import Optional, List

from src.services.interfaces.iaccountreport__service import IAccountReportService
from src.depends.service_depends import get_account_report_service
from src.schemas.accountreport_schema import AccountReportRead

router = APIRouter(prefix="/api/accountreports", tags=["AccountReports"])

@router.get("/balance-sheet")
async def get_balance_sheet(
    as_of_date: date,
    service = Depends(get_account_report_service)
):
    return await service.get_balance_sheet(as_of_date)

@router.get("/trial-balance")
async def get_trial_balance(
    as_of_date: date,
    service = Depends(get_account_report_service)
):
    return await service.get_trial_balance(as_of_date)

@router.get("/profit-loss")
async def get_profit_loss(
    as_of_date: date,
    service = Depends(get_account_report_service)
):
    return await service.get_profit_loss(as_of_date)

@router.get("")
async def ledger_report(
    detailItemCode: str = Query(..., description="Detail Item Code"),
    startDate: date | None = Query(None),
    endDate: date | None = Query(None),
    service: IAccountReportService = Depends(get_account_report_service),
):
    return await service.get_ledger(
        detailItemCode=detailItemCode,
        start_date=startDate,
        end_date=endDate
    )