from typing import Optional
from pydantic import BaseModel, EmailStr


class TenantCreate(BaseModel):
    
    companyName: str
    adminName: str
    databaseName: str
    email: EmailStr
    password: str
    isActive: Optional[bool] = True
