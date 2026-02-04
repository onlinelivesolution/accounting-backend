from fastapi import APIRouter, Depends, Query
from datetime import date
from typing import Optional, List

from src.services.interfaces.iaccountreport__service import IAccountReportService
from src.depends.service_depends import get_account_report_service
from src.schemas.accountreport_schema import AccountReportRead

router = APIRouter(prefix="/accountreports", tags=["AccountReports"]
)

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

# @router.get("/", response_model=List[AccountReportRead])
# async def ledger_report(
#     detailItemCode: Optional[str] = None,
#     start_date: Optional[date] = None,
#     end_date: Optional[date] = None,
#     service: IAccountReportService = Depends(get_account_report_service)
# ):
#     return await service.get_ledger(
#         detailItemCode=detailItemCode,
#         start_date=start_date,
#         end_date=end_date
#     )
