from pydantic import BaseModel

class OTPVerifyRequest(BaseModel):
    userID: int
    otpCode: str


class OTPVerifyResponse(BaseModel):
    token: str
    userName: str
    message: str