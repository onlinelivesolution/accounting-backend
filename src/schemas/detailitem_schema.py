from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DetailItemBase(BaseModel):
    detailItemCode: str
    companyCode: Optional[str] = None
    accountID: int
    reportingItemCode: str
    detailItemName: str
    isActive: Optional[bool] = True
    isInventory: Optional[bool] = True
    isDeleted: Optional[bool] = True    
    accountStateID: int
    

class DetailItemCreate(DetailItemBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = datetime.utcnow()


class DetailItemUpdate(BaseModel):
    detailItemName: Optional[str] = None
    isActive: Optional[bool] = None
    companyCode: Optional[str] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = datetime.utcnow()


class DetailItemRead(DetailItemBase):
    reportingItemCode: Optional[str] = None
    reportingItemName: Optional[str] = None      # ← NEW FIELD
    companyName: Optional[str] = None          # ← NEW FIELD
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None
    isActive: Optional[bool] = False
    isDeleted: Optional[bool] = False
    accountStateID: Optional[int] = None
    accountID: Optional[int] = None
    
class DetailItemDropdown(BaseModel):
    detailItemCode: str
    detailItemName: str
    loadType: str | None

    class Config:
        from_attributes = True
