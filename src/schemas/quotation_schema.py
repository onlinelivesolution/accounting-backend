from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class QuotationItemRequest(BaseModel):
    itemID: int
    itemDescription: Optional[str] = None
    quantity: float = Field(..., gt=0)
    unitPrice: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    lineTotal: float = Field(..., ge=0)

class QuotationCreateRequest(BaseModel):
    quotationNo: str
    quotationDate: date
    customerID: int
    subtotalAmount: float = Field(..., ge=0)
    discountAmount: float = Field(default=0, ge=0)
    vATAmount: float = Field(default=0, ge=0)
    totalAmount: float = Field(..., ge=0)
    remarks: Optional[str] = None
    createdBy: Optional[str] = None
    items: List[QuotationItemRequest]

    model_config = {
        "from_attributes": True
    }

class QuotationItemResponse(BaseModel):
    quotationDetailID: int
    itemID: int
    itemDescription: Optional[str] = None
    quantity: float
    unitPrice: float
    discountAmount: float
    lineTotal: float

    model_config = {
        "from_attributes": True
    }

class QuotationResponse(BaseModel):
    quotationID: int
    quotationNo: str
    quotationDate: date
    customerID: int
    subtotalAmount: float
    discountAmount: float
    vATAmount: float
    totalAmount: float
    status: str
    remarks: Optional[str] = None
    createdBy: str
    createdDate: datetime
    items: List[QuotationItemResponse]

    model_config = {
        "from_attributes": True
    }
