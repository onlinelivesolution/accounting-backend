from fastapi import APIRouter, Depends
from src.schemas.commondropdown_schema import CustomerDropdown, LineItemDropdown
from src.services.interfaces.icommondropdown_service import ICommonDropdownService
from src.depends.service_depends import get_common_dropdown_service
from typing import List, Dict


router = APIRouter(prefix="/api/commondropdown", tags=["Common Dropdown Router"])

@router.get("/loadVatRateDropdown")
async def get_vat_rate_dropdown(
    service: ICommonDropdownService = Depends(get_common_dropdown_service),
):
    return await service.get_vat_rate_dropdown(company_code="01")

@router.get("/loadLineItemDropdown", response_model=List[LineItemDropdown])
async def get_lineitem_dropdown(
    service: ICommonDropdownService = Depends(get_common_dropdown_service)
):
    return await service.get_lineitem_dropdown()

@router.get("/loadCustomerDropdown", response_model=List[CustomerDropdown])
async def get_customer_dropdown(
    service: ICommonDropdownService = Depends(get_common_dropdown_service)
):
    return await service.get_customer_dropdown()