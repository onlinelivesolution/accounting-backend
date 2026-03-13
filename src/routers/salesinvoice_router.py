from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing import Optional
from fastapi import APIRouter, Depends, Query
from src.services.interfaces.isalesinvoice_service import ISalesInvoiceService
from src.depends.service_depends import get_sales_invoice_service
from src.schemas.salesinvoice_schema import (
    SalesInvoiceCreateRequest,
    SalesInvoiceResponse,
    SalesInvoiceUpdateRequest
)

router = APIRouter(prefix="/api/salesinvoices",tags=["SalesInvoices"])

@router.post("/createSalesInvoice", response_model=SalesInvoiceResponse)
async def create_sales_invoice(
    request: SalesInvoiceCreateRequest,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service)
):
    return await service.create_sales_invoice(request)

@router.get("/getNextSalesInvoiceNo")
async def get_next_salesinvoice_no(
    service: ISalesInvoiceService = Depends(get_sales_invoice_service)
):
    return {
        "salesInvoiceNo": await service.get_next_salesinvoice_no()
    }