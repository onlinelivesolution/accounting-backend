# src/schemas/loginschema.py
from pydantic import BaseModel
from typing import List, Optional
from src.schemas.permission_schema import PermissionActionInfo


class UserPermission(BaseModel):
    permissionID: int
    permissionName: str
    isAllowed: bool


class UserInfo(BaseModel):
    userID: int
    userName: str
    email: Optional[str] = None
    fullName: Optional[str] = None
    roleID: int
    companyCode: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):
    userName: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserInfo
    permissions: List[PermissionActionInfo]

    model_config = {
        "from_attributes": True
    }
