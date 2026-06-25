from pydantic import BaseModel


class LoginRequest(BaseModel):

    username:str
    password:str
    
class VerifyOTPRequest(BaseModel):
    username: str
    otp: str