# src/schemas/quotation_to_salesorder_schema.py
from pydantic import BaseModel
from typing import List

class SalesOrderItemFromQuotation(BaseModel):
    itemID: int
    itemDescription: str
    quantity: float
    unitPrice: float
    discountAmount: float
    lineTotal: float

class QuotationToSalesOrderResponse(BaseModel):
    quotationID: int
    customerID: int
    subtotalAmount: float
    discountAmount: float
    vATAmount: float
    totalAmount: float
    items: List[SalesOrderItemFromQuotation]

    model_config = {"from_attributes": True}