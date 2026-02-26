from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date


class JournalDetailRequest(BaseModel):
    debitItemCode: str
    creditItemCode: str
    amount: Decimal
    vATRateID: Optional[int] = None   # ✅ REQUIRED
    ratePercent: Optional[Decimal] = None
    narration: Optional[str] = None

class JournalCreateRequest(BaseModel):
    journalDate: date
    journalType: str
    referenceNo: Optional[str] = None
    description: Optional[str] = None
    details: List[JournalDetailRequest]
