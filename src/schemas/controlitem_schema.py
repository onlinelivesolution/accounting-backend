from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ControlItemBase(BaseModel):
    controlItemCode: str   # 👈 PK, comes directly from model
    controlItemName: str
    isActive: Optional[bool] = True
    accountTypeID: Optional[int] = None
    fATypeID: Optional[int] = None
    companyCode: Optional[str] = None


class ControlItemCreate(ControlItemBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = datetime.utcnow()
    isDeleted: Optional[bool] = False


class ControlItemUpdate(BaseModel):
    controlItemName: Optional[str] = None
    isActive: Optional[bool] = None
    accountTypeID: Optional[int] = None
    fATypeID: Optional[int] = None
    companyCode: Optional[str] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = datetime.utcnow()


class ControlItemRead(ControlItemBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None
    isDeleted: Optional[bool] = False
    accountTypeName: Optional[str] = None
    companyName: Optional[str] = None
    
class ControlItemDropdownByType(BaseModel):
    controlItemCode: str
    controlItemName: str
    accountTypeID: int
    
class ControlItemDropdown(BaseModel):
    controlItemCode: str
    controlItemName: str
    accountTypeID: int

    class Config:
        from_attributes = True
        
        
