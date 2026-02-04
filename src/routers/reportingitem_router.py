from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.services.interfaces.ireportingitem_service import IReportingItemService
from src.depends.service_depends import get_reportingitem_service
from src.schemas.reportingitem_schema import ReportingItemRead, ReportingItemUpdate, ReportingItemCreate
from src.schemas.controlitem_schema import ControlItemDropdown

router = APIRouter(prefix="/api/reportingitems", tags=["ReportingItems"])

@router.post("/addNewReportingItem", response_model=ReportingItemRead)
async def add_reporting_item(
    reportingitem: ReportingItemCreate,
    service: IReportingItemService = Depends(get_reportingitem_service)
):
    return await service.add_reporting_item(reportingitem)

@router.put("/updateReportingItem/{reportingItemCode}", response_model=ReportingItemRead)
async def update_reporting_item(
    reportingItemCode: str,
    reportingitem: ReportingItemUpdate,
    service: IReportingItemService = Depends(get_reportingitem_service),
):
    updated_item = await service.update_reporting_item(reportingItemCode, reportingitem)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Reporting item not found")
    return updated_item

@router.get("/loadReportingItemTable", response_model=List[ReportingItemRead])
async def get_all_reporting_items(
    skip: int = 0,
    limit: int = 100,
    service: IReportingItemService = Depends(get_reportingitem_service)
):
    return await service.get_all_reporting_items(skip=skip, limit=limit)

@router.get("/loadAccountTypeDropdown", response_model=List[AccountTypeDropdown])
async def get_account_types(service: IReportingItemService = Depends(get_reportingitem_service)):
    return await service.get_account_types()

@router.get("/getControlItemsByAccountType/{accountTypeID}")
async def get_control_items_by_account_type(
    accountTypeID: int,
    service: IReportingItemService = Depends(get_reportingitem_service)
):
    return await service.get_control_items_by_account_type(accountTypeID)

@router.get("/loadControlItemDropdown", response_model=List[ControlItemDropdown])
async def get_controlitem_dropdown(service: IReportingItemService = Depends(get_reportingitem_service)):
    return await service.get_controlitem_dropdown()

@router.get("/getNextReportingItemCode/{controlItemCode}")
async def get_next_code(
    controlItemCode: str,
    service: IReportingItemService = Depends(get_reportingitem_service)
):
    return {
        "nextCode": await service.get_max_reporting_item_code(controlItemCode)
    }
