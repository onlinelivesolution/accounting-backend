from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class SalesOrderItemRequest(BaseModel):
    itemID: int
    itemDescription: Optional[str] = None
    quantity: float = Field(..., gt=0)
    unitPrice: float = Field(..., ge=0)
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    lineTotal: float = Field(..., ge=0)
    vatAmount: float = Field(..., ge=0)
    model_config = {"from_attributes": True}

class SalesOrderCreateRequest(BaseModel):
    salesOrderNo: str
    salesOrderDate: date
    expireDate: date
    customerID: int
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vatAmount: float = Field(default=0, ge=0)
    totalAmount: float = Field(..., ge=0)
    remarks: Optional[str] = None
    createdBy: Optional[str] = None
    items: List[SalesOrderItemRequest]

    model_config = {"from_attributes": True}

class SalesOrderItemResponse(BaseModel):
    salesOrderDetailID: int
    itemID: int
    itemDescription: Optional[str] = None
    quantity: float
    unitPrice: float
    exclusiveAmount: float
    discountAmount: float
    vatAmount: float
    lineTotal: float

    model_config = {"from_attributes": True}

class SalesOrderResponse(BaseModel):
    salesOrderID: int
    quotationID:  Optional[int] = None
    salesOrderNo: str
    salesOrderDate: date
    customerID: int
    exclusiveAmount: float
    discountAmount: float
    vatAmount: float
    totalAmount: float
    status: str
    remarks: Optional[str] = None
    createdBy: str
    createdDate: datetime
    items: List[SalesOrderItemResponse]

    model_config = {"from_attributes": True}

class SalesOrderTableResponse(BaseModel):
    salesOrderID: int
    salesOrderNo: str
    salesOrderDate: date
    totalAmount: float
    customerName: str
    customerID: int
    status: str

    class Config:
        from_attributes = True   # REQUIRED for SQLAlchemy

class SalesOrderItemUpdateRequest(BaseModel):
    itemID: int = Field(..., gt=0)
    itemDescription: str
    quantity: float = Field(..., gt=0)
    unitPrice: float = Field(..., ge=0)
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vatAmount: float = Field(..., ge=0)
    lineTotal: float = Field(..., ge=0)

    class Config:
        from_attributes = True

class SalesOrderUpdateRequest(BaseModel):
    salesOrderDate: date
    expireDate: date | None = None
    customerID: int = Field(..., gt=0)
    exclusiveAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vatAmount: float = Field(..., ge=0)
    totalAmount: float = Field(..., ge=0)

    items: List[SalesOrderItemUpdateRequest]

    class Config:
        from_attributes = True
