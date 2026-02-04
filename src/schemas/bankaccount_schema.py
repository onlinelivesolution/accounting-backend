# src/schemas/bankaccount_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


# -------------------------------
# CREATE
# -------------------------------
class BankAccountCreate(BaseModel):
    bankAccountName: str = Field(..., max_length=150)
    category: Optional[str] = None
    defaultPaymentMethod: int

    bankName: str
    accountNumber: str
    branchName: Optional[str] = None
    branchCode: Optional[str] = None
    description: Optional[str] = None

    isActive: bool = True
    isDefault: bool = False
    # Accounting
    openingBalance: Optional[float] = 0
    openingBalanceDate: Optional[date] = None


# -------------------------------
# READ
# -------------------------------
class BankAccountRead(BaseModel):
    bankAccountID: int
    bankAccountName: str
    bankName: str
    accountNumber: str
    detailItemCode: str
    isActive: bool
    isDefault: bool

class BankAccountDropdown(BaseModel):
    bankAccountID: int
    bankAccountName: str

    class Config:
        from_attributes = True
