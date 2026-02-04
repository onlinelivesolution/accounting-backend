from typing import List
from pydantic import BaseModel, Field

class RolePermissionAssign(BaseModel):
    """
    Used when Super Admin assigns multiple permissions to a role.
    Example payload:
    {
        "roleID": 2,
        "permissionIDs": [1, 3, 5, 7],
        "assignedBy": "superadmin"
    }
    """
    roleID: int = Field(..., description="ID of the role to assign permissions to")
    permissionIDs: List[int] = Field(..., description="List of permission IDs to assign to the role")
    updatedBy: str = Field(..., description="Username of the admin performing the assignment")
