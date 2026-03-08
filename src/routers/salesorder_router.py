from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing import Optional
from fastapi import APIRouter, Depends, Query
from src.services.interfaces.isalesorder_service import ISalesOrderService
from src.depends.service_depends import get_sales_order_service
from src.schemas.salesorder_schema import (
    SalesOrderCreateRequest,
    SalesOrderResponse,
    SalesOrderUpdateRequest,
    SalesOrderStatusUpdateRequest
)

router = APIRouter(prefix="/api/salesorders",tags=["SalesOrders"])


@router.get("/getSalesOrderFilters")
async def get_sales_order(
    filterType: str = "ALL",
    salesOrderNo: str | None = None,
    page: int = 1,
    pageSize: int = 10,
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    return await service.get_filter_sales_order(
        filterType,
        salesOrderNo,
        page,
        pageSize
    )

@router.get("/", response_model=list[SalesOrderResponse])
async def list_sales_order(
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    return await service.list_sales_order()

@router.get("/loadSalesOrderTable")
async def load_sales_order_table(
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    return await service.load_sales_order_table()

@router.get("/getNextSalesOrderNo")
async def get_next_salesorder_no(
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    return {
        "salesOrderNo": await service.get_next_salesorder_no()
    }

@router.post("/createSalesOrder", response_model=SalesOrderResponse)
async def create_sales_order(
    request: SalesOrderCreateRequest,
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    return await service.create_sales_order(request)

@router.put("/updateSalesOrder/{salesorder_id}")
async def update_sales_order(
    salesorder_id: int,
    request: SalesOrderUpdateRequest,
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    result = await service.update_sales_order(salesorder_id, request)

    if not result:
        raise HTTPException(status_code=404, detail="Sales Order not found")

    return {"message": "Sales Order updated successfully"}

@router.put("/updateSalesOrderStatus/{salesorder_id}")
async def update_sales_order_status(
    salesorder_id: int,
    request: SalesOrderStatusUpdateRequest,
    service: ISalesOrderService = Depends(get_sales_order_service)
):

    result = await service.update_sales_order_status(
        salesorder_id,
        request.status
    )

    if not result:
        raise HTTPException(status_code=404, detail="Sales Order not found")

    return {"message": "Sales Order status updated successfully"}

@router.get("/{salesorder_id}", response_model=SalesOrderResponse)
async def get_sales_order(
    salesorder_id: int,
    service: ISalesOrderService = Depends(get_sales_order_service)
):
    salerorder = await service.get_sales_order(salesorder_id)
    if not salerorder:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    return salerorder








