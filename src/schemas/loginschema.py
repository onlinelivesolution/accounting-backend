from pydantic import BaseModel
from typing import List, Optional


class LoginRequest(BaseModel):
    userName: str
    password: str


class LoginOTPResponse(BaseModel):
    message: str
    userID: int


class VerifyOTPRequest(BaseModel):
    userID: int
    otp: str


class PermissionSchema(BaseModel):
    permissionName: str
    actionName: str


class UserSchema(BaseModel):
    userID: int
    userName: str


class LoginResponse(BaseModel):
    token: str
    user: UserSchema
    permissions: List[PermissionSchema]