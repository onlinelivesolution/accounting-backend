from pydantic import BaseModel
from typing import Optional

class RolePermissionActionBase(BaseModel):
    rolePermissionActionID: int
    roleID: int
    permissionActionID: int
    isAllowed: bool

    class Config:
        from_attributes = True
