# src/schemas/journal_schema.py
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class JournalCreate(BaseModel):
    journalDate: datetime
    companyCode: str
    activityCenterCode: str
    respCenterCode: str
    aBType: int
    fAType: int
    controlItemCode: str
    reportingItemCode: str
    detailItemCode: str
    debitAmount: Decimal
    creditAmount: Decimal
    referenceNo: int
    fiscalYear: str
    accountNumber: str
    referenceID: str
    period: int
    createdBy: str
    projectCode: str
