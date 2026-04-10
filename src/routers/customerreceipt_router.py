from fastapi import APIRouter, Depends
from src.services.interfaces.icustomerreceipt_service import ICustomerReceiptService
from src.depends.service_depends import get_customer_receipt_service
from src.schemas.customerreceipt_schema import CustomerReceiptCreate

router = APIRouter(prefix="/api/customerreceipts", tags=["CustomerReceipts"])


# ✅ Load invoices by customer
@router.get("/getCustomerInvoices/{customer_id}")
async def get_customer_invoices(
    customer_id: int,
    service: ICustomerReceiptService = Depends(get_customer_receipt_service)
):
    return await service.get_customer_invoices(customer_id)


# ✅ Create receipt
@router.post("/createCustomerReceipt")
async def create_customer_receipt(
    request: CustomerReceiptCreate,
    service: ICustomerReceiptService = Depends(get_customer_receipt_service)
):
    return await service.create_customer_receipt(request)

@router.get("/getCustomerBalance/{customer_id}")
async def get_customer_balance(
    customer_id: int,
    service: ICustomerReceiptService = Depends(get_customer_receipt_service)
):
    return await service.get_customer_balance(customer_id)