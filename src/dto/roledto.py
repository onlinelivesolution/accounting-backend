# roledto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    roleName: str
    description: Optional[str] = None
    isActive: Optional[bool] = None
    companyCode: Optional[str] = None

class RoleCreate(RoleBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None

class RoleUpdate(RoleBase):
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

class RoleRead(RoleBase):
    roleID: int
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

    class Config:
        from_attributes = True
