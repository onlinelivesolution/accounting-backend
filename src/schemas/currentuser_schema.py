from pydantic import BaseModel


class CurrentUser(BaseModel):
    userID: int
    userName: str
    fullName: str | None
    companyCode: str
    roleID: int
    isSuperAdmin: bool

    class Config:
        from_attributes = True
