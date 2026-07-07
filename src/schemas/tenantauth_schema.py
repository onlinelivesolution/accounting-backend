from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str = Field(alias="userName")
    password: str
    
class VerifyOTPRequest(BaseModel):
    username: str
    otp: str