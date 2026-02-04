# roledto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BankBase(BaseModel):
    bankName: str
    bankCode: Optional[str] = None
    address: Optional[str] = None
    isDeleted: Optional[bool] = None
    companyCode: Optional[str] = None

class BankCreate(BankBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None

class BankUpdate(BankBase):
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

class BankRead(BankBase):
    bankID: int
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

    class Config:
        from_attributes = True
