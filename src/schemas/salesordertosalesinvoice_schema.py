# src/schemas/quotation_to_salesorder_schema.py
from pydantic import BaseModel
from typing import List

class SalesInvoiceItemFromSalesOrder(BaseModel):
    itemID: int
    itemDescription: str
    quantity: float
    unitPrice: float
    discountAmount: float
    lineTotal: float

class SalesOrderToSalesInvoiceResponse(BaseModel):
    salesOrderID: int
    customerID: int
    exclusiveAmount: float
    discountAmount: float
    vatAmount: float
    totalAmount: float
    items: List[SalesInvoiceItemFromSalesOrder]

    model_config = {"from_attributes": True}