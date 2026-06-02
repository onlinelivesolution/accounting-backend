from pydantic import BaseModel
from typing import List


class LoginRequest(BaseModel):
    userName: str
    password: str


class LoginOTPResponse(BaseModel):
    message: str
    userID: int
    otp: str


class UserSchema(BaseModel):
    userID: int
    userName: str
    roleID: int


class PermissionSchema(BaseModel):
    permissionName: str
    actionName: str
    isAllowed: bool


class LoginResponse(BaseModel):
    token: str
    user: UserSchema
    
class OTPVerifyRequest(BaseModel):
    userID: int
    tenant: str
    otpCode: str    


class OTPVerifyResponse(BaseModel):
    token: str
    userName: str
    message: str