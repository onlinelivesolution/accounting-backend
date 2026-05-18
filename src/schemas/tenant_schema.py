from pydantic import BaseModel, EmailStr


class TenantCreate(BaseModel):

    companyName: str

    email: EmailStr

    password: str
