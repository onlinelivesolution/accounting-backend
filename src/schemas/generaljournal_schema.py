from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date


class JournalDetailRequest(BaseModel):
    debitItemCode: str
    creditItemCode: str
    amount: Decimal
    vatRateID: int
    vatPercent: Decimal
    vatRate: Decimal
    vatAmount: Decimal
    totalAmount: Decimal
    narration: Optional[str] = None


class JournalCreateRequest(BaseModel):
    journalDate: date
    journalType: str
    referenceNo: Optional[str] = None
    description: Optional[str] = None
    details: List[JournalDetailRequest]
