from fastapi import APIRouter, Depends, HTTPException

from src.services.interfaces.iquotation_service import IQuotationService
from src.depends.service_depends import get_quotation_service
from src.schemas.quotation_schema import (
    QuotationCreateRequest,
    QuotationResponse
)

router = APIRouter(prefix="/api/quotations",tags=["Quotations"]
)


@router.post("/createQuotation", response_model=QuotationResponse)
async def create_quotation(
    request: QuotationCreateRequest,
    service: IQuotationService = Depends(get_quotation_service)
):
    return await service.create_quotation(request)

@router.get("/getNextQuotationNo")
async def get_next_quotation_no(
    service: IQuotationService = Depends(get_quotation_service)
):
    return {
        "quotationNo": await service.get_next_quotation_no()
    }


@router.get("/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(
    quotation_id: int,
    service: IQuotationService = Depends(get_quotation_service)
):
    quotation = await service.get_quotation(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation


@router.get("/", response_model=list[QuotationResponse])
async def list_quotations(
    service: IQuotationService = Depends(get_quotation_service)
):
    return await service.list_quotations()


