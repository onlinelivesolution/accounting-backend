from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from typing import Literal, Optional


class BankTransactionRequest(BaseModel):
    bankDetailItemCode: str = Field(..., min_length=1)
    contraDetailItemCode: str = Field(..., min_length=1)
    transactionType: str
    amount: float = Field(..., gt=0)
    transactionDate: date
    referenceNo: str | None = None
    description: str | None = None
