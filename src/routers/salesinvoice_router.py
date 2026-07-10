from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.tenant_database import get_tenant_db
from typing import List
from typing import Optional
from src.core.auth_dependency import get_current_user
from src.schemas.commonemail_schema import SendSalesInvoiceEmailRequest
from fastapi import APIRouter, Depends, Query
from src.schemas.commondropdown_schema import SalesOrderDropdown
from src.schemas.salesordertosalesinvoice_schema import SalesOrderToSalesInvoiceResponse
from src.services.interfaces.isalesinvoice_service import ISalesInvoiceService
from src.depends.service_depends import get_sales_invoice_service
from src.schemas.salesinvoice_schema import (
    SalesInvoiceCreateRequest,
    SalesInvoiceResponse,
    SalesInvoiceUpdateRequest,
    SalesInvoiceStatusUpdateRequest,
)

router = APIRouter(prefix="/api/salesinvoices", tags=["SalesInvoices"])


@router.get("/getSalesInvoiceFilters")
async def get_sales_invoice(
    filterType: str = "ALL",
    salesInvoiceNo: str | None = None,
    page: int = 1,
    pageSize: int = 10,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return await service.get_filter_sales_invoice(
        filterType, salesInvoiceNo, page, pageSize
    )


@router.get("/", response_model=list[SalesInvoiceResponse])
async def list_sales_invoice(
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return await service.list_sales_invoice()


@router.get("/loadSalesInvoiceTable")
async def load_sales_invoice_table(
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return await service.load_sales_invoice_table()


@router.post("/createSalesInvoice", response_model=SalesInvoiceResponse)
async def create_sales_invoice(
    request: SalesInvoiceCreateRequest,
    current_user: dict = Depends(get_current_user),
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return await service.create_sales_invoice(request, current_user)


@router.put("/updateSalesInvoice/{id}")
async def update_sales_invoice(
    id: int,
    payload: SalesInvoiceUpdateRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_sales_invoice_service),
):
    return await service.update_sales_invoice(id, payload, current_user)

@router.put("/approveSalesInvoice/{salesInvoiceID}")
async def approve_sales_invoice(
    salesInvoiceID: int,
    current_user: dict = Depends(get_current_user),
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    try:
        result = await service.approve_sales_invoice(salesInvoiceID, current_user)
        return {
            "success": True,
            "message": "Sales Invoice approved successfully",
            "data": result,
        }

    except Exception as e:
        import traceback

        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/send-email")
async def send_invoice_email(
    request: SendSalesInvoiceEmailRequest,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    await service.send_invoice_email(request)
    return {"message": "Email sent successfully"}


@router.get("/getNextSalesInvoiceNo")
async def get_next_salesinvoice_no(
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return {"salesInvoiceNo": await service.get_next_salesinvoice_no()}


@router.put("/updateSalesInvoiceStatus/{salesinvoice_id}")
async def update_sales_invoice_status(
    salesinvoice_id: int,
    request: SalesInvoiceStatusUpdateRequest,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):

    result = await service.update_sales_invoice_status(salesinvoice_id, request.status)

    if not result:
        raise HTTPException(status_code=404, detail="Sales Invoice not found")

    return {"message": "Sales Invoice status updated successfully"}


@router.get("/salesOrderDropdown", response_model=List[SalesOrderDropdown])
async def get_sales_order_dropdown(
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return await service.get_sales_order_dropdown()


@router.get(
    "/{salesOrderID}/to-sales-invoice", response_model=SalesOrderToSalesInvoiceResponse
)
async def get_sales_order_to_sales_invoice(
    salesOrderID: int,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    return await service.get_sales_order_for_sales_invoice(salesOrderID)


@router.post("/{salesinvoice_id}/copy")
async def copy_sales_invoice(
    salesinvoice_id: int,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    result = await service.copy_sales_invoice(salesinvoice_id)

    if not result:
        raise HTTPException(status_code=404, detail="Sales Invoice not found")

    return result


@router.get("/{salesinvoice_id}", response_model=SalesInvoiceResponse)
async def get_sales_invoice(
    salesinvoice_id: int,
    service: ISalesInvoiceService = Depends(get_sales_invoice_service),
):
    salesinvoice = await service.get_sales_invoice_by_id(salesinvoice_id)
    if not salesinvoice:
        raise HTTPException(status_code=404, detail="Sales Invoice not found")
    return salesinvoice
