from pydantic import BaseModel, EmailStr
from typing import Optional

class TenantRegisterRequest(BaseModel):
    companyName: str
    adminName: str
    databaseName: str
    email: EmailStr
    password: str
    isActive: Optional[bool] = True


class TenantResponse(BaseModel):
    tenantID: int
    companyName: str
    databaseName: str
    email: str
    status: str

class TenantStatusUpdateRequest(BaseModel):
    status: str

    model_config = {
        "from_attributes": True
    }