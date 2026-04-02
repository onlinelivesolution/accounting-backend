from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class SalesInvoiceItemRequest(BaseModel):
    itemID: int
    itemDescription: Optional[str] = None
    quantity: float = Field(..., gt=0)
    unitPrice: float = Field(..., ge=0)
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    totalAmount: float = Field(..., ge=0)
    vatAmount: float = Field(..., ge=0)
    model_config = {"from_attributes": True}

class SalesInvoiceCreateRequest(BaseModel):
    salesOrderID: Optional[int] = None
    salesInvoiceNo: str
    salesInvoiceDate: date
    customerID: int
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vatAmount: float = Field(default=0, ge=0)
    totalAmount: float = Field(..., ge=0)
    remarks: Optional[str] = None
    createdBy: Optional[str] = None
    items: List[SalesInvoiceItemRequest]

    model_config = {"from_attributes": True}

class SalesInvoiceItemResponse(BaseModel):
    salesInvoiceDetailID: int
    itemID: int
    itemDescription: Optional[str] = None
    quantity: float
    unitPrice: float
    exclusiveAmount: float
    discountAmount: float
    vatAmount: float
    totalAmount: float

    model_config = {"from_attributes": True}

class SalesInvoiceResponse(BaseModel):
    salesInvoiceID: int
    salesOrderID:  Optional[int] = None
    salesInvoiceNo: str
    salesInvoiceDate: date
    customerID: int
    exclusiveAmount: float
    discountAmount: float
    vatAmount: float
    totalAmount: float
    status: str
    remarks: Optional[str] = None
    createdBy: str
    createdDate: datetime
    items: List[SalesInvoiceItemResponse]

    model_config = {"from_attributes": True}

class SalesInvoiceTableResponse(BaseModel):
    salesInvoiceID: int
    salesInvoiceNo: str
    salesInvoiceDate: date
    totalAmount: float
    customerName: str
    customerID: int
    status: str

    class Config:
        from_attributes = True   # REQUIRED for SQLAlchemy

class SalesInvoiceItemUpdateRequest(BaseModel):
    itemID: int = Field(..., gt=0)
    itemDescription: str
    quantity: float = Field(..., gt=0)
    unitPrice: float = Field(..., ge=0)
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vatAmount: float = Field(..., ge=0)
    totalAmount: float = Field(..., ge=0)

    class Config:
        from_attributes = True

class SalesInvoiceUpdateRequest(BaseModel):
    salesOrderDate: date
    expireDate: date | None = None
    customerID: int = Field(..., gt=0)
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vatAmount: float = Field(..., ge=0)
    totalAmount: float = Field(..., ge=0)

    items: List[SalesInvoiceItemUpdateRequest]

    class Config:
        from_attributes = True

class SalesInvoiceStatusUpdateRequest(BaseModel):
    status: str
