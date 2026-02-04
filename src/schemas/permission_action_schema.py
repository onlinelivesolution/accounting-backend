from pydantic import BaseModel
from typing import List, Optional

class PermissionActionBase(BaseModel):
    permissionActionID: int
    actionName: str
    actionKey: str
    isActive: bool

    class Config:
        from_attributes = True


class PermissionTreeChild(PermissionActionBase):
    """For nested tree display in React."""
    pass


class PermissionTreeParent(BaseModel):
    permissionID: int
    permissionName: str
    children: List[PermissionTreeChild]

    class Config:
        from_attributes = True
