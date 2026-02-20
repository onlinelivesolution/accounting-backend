from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing import Optional
from fastapi import APIRouter, Depends, Query
from common.enum.commenum import QuotationFilter
from src.services.interfaces.iquotation_service import IQuotationService
from src.depends.service_depends import get_quotation_service
from src.schemas.quotation_schema import (
    QuotationCreateRequest,
    QuotationResponse
)

router = APIRouter(prefix="/api/quotations",tags=["Quotations"])


@router.get("/getQuotationFilters")
async def get_quotations(
    filterType: str = "ALL",
    quotationNo: str | None = None,
    page: int = 1,
    pageSize: int = 10,
    service: IQuotationService = Depends(get_quotation_service)
):
    return await service.get_quotations(
        filterType,
        quotationNo,
        page,
        pageSize
    )

@router.get("/", response_model=list[QuotationResponse])
async def list_quotations(
    service: IQuotationService = Depends(get_quotation_service)
):
    return await service.list_quotations()

@router.get("/loadQuotationTable")
async def get_quotation_table(
    service: IQuotationService = Depends(get_quotation_service)
):
    return await service.get_quotation_table()

@router.get("/getNextQuotationNo")
async def get_next_quotation_no(
    service: IQuotationService = Depends(get_quotation_service)
):
    return {
        "quotationNo": await service.get_next_quotation_no()
    }

@router.post("/createQuotation", response_model=QuotationResponse)
async def create_quotation(
    request: QuotationCreateRequest,
    service: IQuotationService = Depends(get_quotation_service)
):
    return await service.create_quotation(request)

@router.get("/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(
    quotation_id: int,
    service: IQuotationService = Depends(get_quotation_service)
):
    quotation = await service.get_quotation(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation








