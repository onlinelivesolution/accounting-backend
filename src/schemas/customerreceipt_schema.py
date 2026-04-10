# schemas/customer_receipt_schema.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date


# ===============================
# Detail Schema
# ===============================
class CustomerReceiptDetailBase(BaseModel):
    salesInvoiceID: int
    paidAmount: float
    narration: Optional[str] = None


class CustomerReceiptDetailCreate(CustomerReceiptDetailBase):
    pass


class CustomerReceiptDetailResponse(CustomerReceiptDetailBase):
    customerReceiptDetailID: int

    model_config = ConfigDict(from_attributes=True)


# ===============================
# Master Schema
# ===============================
class CustomerReceiptBase(BaseModel):
    receiptNo: str
    receiptDate: date
    customerID: int
    totalAmount: float
    status: Optional[str] = "DRAFT"


class CustomerReceiptCreate(CustomerReceiptBase):
    details: List[CustomerReceiptDetailCreate]


class CustomerReceiptResponse(CustomerReceiptBase):
    customerReceiptID: int
    details: List[CustomerReceiptDetailResponse]

    model_config = ConfigDict(from_attributes=True)