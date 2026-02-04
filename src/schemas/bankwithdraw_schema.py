# roledto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class BankWithdrawBase(BaseModel):
    bankAccountID: int
    accountNumber: Optional[str] = None
    withdrawType: int
    withdrawRefNo: Optional[str] = None
    withdrawDate: Optional[datetime] = None
    withdrawndBy: Optional[str] = None
    amount: Decimal
    shortNote: Optional[str] = None
    status: int
    isDeleted: Optional[bool] = None
    

class BankWithdrawCreate(BankWithdrawBase):
    createdBy: Optional[str] = None

class BankWithdrawRead(BankWithdrawBase):
    bankWithdrawID: int
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

    class Config:
        from_attributes = True
