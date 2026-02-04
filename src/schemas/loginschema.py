from pydantic import BaseModel
from typing import List, Optional
from src.schemas.permission_schema import PermissionActionInfo

class UserPermission(BaseModel):
    permissionID: int
    permissionName: str
    isAllowed: bool

class UserInfoSchema(BaseModel):
    userID: int
    userName: str
    email: Optional[str] = None
    fullName: Optional[str] = None
    roleID: int
    companyCode: Optional[str] = None

    model_config = {
        "from_attributes": True  # allows automatic conversion from ORM objects
    }

class LoginRequest(BaseModel):
    userName: str
    password: str

class UserInfo(BaseModel):
    userID: int
    userName: str
    roleID: Optional[int]
    permissions: Optional[List[UserPermission]] = []

    model_config = {
        "from_attributes": True
    }

class LoginResponse(BaseModel):
    token: str
    user: UserInfo  # Pydantic model
    permissions: List[PermissionActionInfo]

    model_config = {
        "from_attributes": True  # allows automatic conversion from ORM objects
    }
