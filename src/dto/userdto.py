from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserBaseDTO(BaseModel):
    userName: str = Field(..., description="Login username")
    email: Optional[str] = Field(None, description="User email address")
    fullName: Optional[str] = Field(None, description="Full name of the user")
    isActive: Optional[bool] = Field(default=True, description="Is the user active?")
    isSuperAdmin: Optional[bool] = Field(default=True, description="Is the user active?")
    companyCode: Optional[str] = Field(None, description="Company code (if multi-company setup)")
    
class Permission(BaseModel):
    permissionName: str
    actionKey: str

class UserLogin(BaseModel):
    username: str
    password: str      

class UserCreate(UserBaseDTO):
    userName: str
    email: Optional[str] = None
    fullName: Optional[str] = None
    passwordHash: str
    roleID: Optional[int] = None
    isActive: Optional[bool] = True
    isSuperAdmin: Optional[bool] = False
    companyCode: Optional[str] = None
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None

class UserRoleUpdate(BaseModel):
    userID: int
    roleID: int  # e.g. "1,2,3"
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None

class UserUpdate(UserBaseDTO):
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None
    roleID: Optional[int] = None
    isActive: Optional[bool] = None

class UserRead(UserBaseDTO):
    userID: int
    email: Optional[str]
    isActive: Optional[bool]
    createdBy: Optional[str]
    createdDate: Optional[datetime]
    updatedBy: Optional[str]
    updatedDate: Optional[datetime]
    roleName: Optional[str] = None
    companyName: Optional[str] = None
    
class UserResponse(BaseModel):
    userID: int
    userName: str
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    isActive: Optional[bool] = None
    isSuperAdmin: Optional[bool] = None
    companyCode: Optional[str] = None
    roleID: Optional[int] = None
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None
    roleName: Optional[str] = None
    companyName: Optional[str] = None
    permissions: List[Permission]
    
class ChangePasswordRequest(BaseModel):
    userID: int = Field(..., description="Logged-in user ID")
    oldPassword: str
    newPassword: str

class Config:
        from_attributes = True
