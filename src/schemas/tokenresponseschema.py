from pydantic import BaseModel
from typing import List, Optional

class PermissionData(BaseModel):
    permissionName: str
    actionKey: str

class UserData(BaseModel):
    userID: int
    username: str
    roleID: Optional[int]
    permissions: List[PermissionData]

class TokenResponse(BaseModel):
    token: str
    user: UserData
