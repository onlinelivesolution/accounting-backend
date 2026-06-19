from pydantic import BaseModel

class SystemAdminLoginRequest(BaseModel):
    username: str
    password: str


class SystemAdminVerifyOTPRequest(BaseModel):
    username: str
    otp: str