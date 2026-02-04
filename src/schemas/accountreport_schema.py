from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class AccountReportRead(BaseModel):
    journalID: int
    journalDate: date
    journalType: str
    referenceNo: str
    description: str
    detailItemCode: str
    detailItemName: str
    debit: Decimal
    credit: Decimal
    balance: Decimal = 0
