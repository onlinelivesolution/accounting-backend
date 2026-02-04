# src/schemas/commonjournal_schema.py
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date

class JournalEntryRequest(BaseModel):
    companyCode: str
    accountID: int        # 12 = Bank
    amount: Decimal
    referenceID: str
    createdBy: str
    
class GeneralJournalEntryRequest(BaseModel):
    debitDetailItemCode: str = Field(..., min_length=1)
    creditDetailItemCode: str = Field(..., min_length=1)
    transactionType: str
    amount: float = Field(..., gt=0)
    transactionDate: date
    referenceNo: str | None = None
    description: str | None = None
