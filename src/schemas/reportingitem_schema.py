from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReportingItemBase(BaseModel):
    reportingItemCode: str
    controlItemCode: str
    reportingItemName: str
    isActive: Optional[bool] = True
    isDeleted: Optional[bool] = True
    companyCode: Optional[str] = None


class ReportingItemCreate(ReportingItemBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = datetime.utcnow()


class ReportingItemUpdate(BaseModel):
    reportingItemName: Optional[str] = None
    isActive: Optional[bool] = None
    companyCode: Optional[str] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = datetime.utcnow()


class ReportingItemRead(ReportingItemBase):
    controlItemCode: Optional[str] = None
    controlItemName: Optional[str] = None      # ← NEW FIELD
    companyName: Optional[str] = None          # ← NEW FIELD
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None
    isActive: Optional[bool] = False
    isDeleted: Optional[bool] = False
    
class ReportingItemResponse(BaseModel):
    reportingItemCode: str
    reportingItemName: str
    controlItemCode: str
    accountTypeID: int

    class Config:
        from_attributes = True
