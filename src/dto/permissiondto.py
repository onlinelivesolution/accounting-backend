from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PermissionBase(BaseModel):    
    permissionName: str
    moduleName: str
    description: Optional[str] = None
    isActive: Optional[bool] = None
    companyCode: Optional[str] = None

class PermissionCreate(PermissionBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None

class PermissionUpdate(BaseModel):
    permissionName: Optional[str] = Field(None)
    moduleName: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    updatedBy: Optional[str] = Field(None)
    updatedDate: Optional[datetime] = Field(default_factory=datetime.utcnow)

class PermissionRead(PermissionBase):
    permissionID: int
    createdBy: Optional[str]
    createdDate: Optional[datetime]
    updatedBy: Optional[str]
    updatedDate: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
