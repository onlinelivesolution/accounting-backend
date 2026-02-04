from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class RolePermissionBase(BaseModel):
    roleID: int = Field(..., description="ID of the role")
    permissionID: int = Field(..., description="ID of the permission")
    companyCode: Optional[str] = None

class RolePermissionCreate(RolePermissionBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None

class RolePermissionUpdate(BaseModel):
    roleID: Optional[int] = Field(None)
    permissionID: Optional[int] = Field(None)
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

class RolePermissionRead(RolePermissionBase):
    rolePermissionID: int
    roleName: Optional[str] = Field(None, description="Name of the role (joined for display)")
    permissionName: Optional[str] = Field(None, description="Name of the permission (joined for display)")
    createdBy: Optional[str]
    createdDate: Optional[datetime]
    updatedBy: Optional[str]
    updatedDate: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
