from datetime import datetime, timedelta
from fastapi import HTTPException

from common.utils.security import verify_password
from common.utils.otp_utils import generate_otp

from src.models.userotp import UserOTP

from src.schemas.loginschema import (
    LoginRequest,
    LoginOTPResponse,
)

class LoginService:

    def __init__(self, repo):
        self.repo = repo

    async def login(
        self,
        request: LoginRequest
    ) -> LoginOTPResponse:

        user = await self.repo.get_user_by_username(
            request.userName
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username"
            )

        is_valid, needs_rehash = verify_password(
            request.password,
            user.password
        )

        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        otp_code = generate_otp()

        expiry = datetime.utcnow() + timedelta(minutes=5)

        otp = UserOTP(
            userID=user.userID,
            otpCode=otp_code,
            expiryTime=expiry,
            isUsed=False
        )

        await self.repo.save_otp(otp)

        print("OTP:", otp_code)

        # Later:
        # send_sms(user.phoneNumber, otp_code)

        return LoginOTPResponse(
            message="OTP sent successfully",
            userID=user.userID
        )