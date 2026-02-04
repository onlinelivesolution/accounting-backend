from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class JournalDetailRequest(BaseModel):
    debitItemCode: str
    creditItemCode: str
    amount: float
    narration: Optional[str] = None


class JournalRequest(BaseModel):
    journalDate: date
    journalType: str
    referenceNo: Optional[str] = None
    description: Optional[str] = None
    details: List[JournalDetailRequest]

    class Config:
        from_attributes = True
