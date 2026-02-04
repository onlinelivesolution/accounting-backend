# roledto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class BankDepositBase(BaseModel):
    bankAccountID: int
    accountNumber: Optional[str] = None
    depositType: int
    depositRefNo: Optional[str] = None
    depositDate: Optional[datetime] = None
    depositedBy: Optional[str] = None
    amount: Decimal
    shortNote: Optional[str] = None
    status: int
    isDeleted: Optional[bool] = None
    

class BankDepositCreate(BankDepositBase):
    createdBy: Optional[str] = None

class BankDepositRead(BankDepositBase):
    bankDepositID: int
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

    class Config:
        from_attributes = True
