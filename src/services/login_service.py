from datetime import datetime, timedelta
from fastapi import HTTPException
from requests import request
from common.utils.jwt_handler import create_access_token
from common.utils.security import verify_password
from common.utils.otp_utils import generate_otp

from src.models.userotp import UserOTP
from common.utils.sms import send_sms
from src.schemas.loginschema import LoginRequest, LoginOTPResponse


class LoginService:

    def __init__(self, repository):
        self.repository = repository

    async def login(self, request: LoginRequest) -> LoginOTPResponse:

        user = await self.repository.get_user_by_username(request.userName)

        if not user:

            raise HTTPException(status_code=401, detail="Invalid username")

        # 🔴 CHECK LOCKED USER (IMPORTANT SECURITY FIX)
        if user.lockedUntil and user.lockedUntil > datetime.utcnow():

            raise HTTPException(status_code=403, detail="User is locked. Try later.")

        # ==============================
        # PASSWORD VERIFY
        # ==============================

        is_valid, needs_rehash = verify_password(request.password, user.passwordHash)

        if not is_valid:

            # 🔴 increase failed attempts
            await self.repository.increment_failed_attempts(user.userID)

            # optional lock after 5 attempts
        failed_attempts = user.failedLoginAttempts or 0

        if failed_attempts >= 4:
            await self.repository.lock_user(user.userID)

            raise HTTPException(status_code=401, detail="Invalid password")

        # reset failed attempts on success
        await self.repository.reset_failed_attempts(user.userID)

        # auto upgrade hash
        if needs_rehash:

            from common.utils.security import hash_password

            new_hash = hash_password(request.password)

            await self.repository.update_password_hash(user.userID, new_hash)

        # ==============================
        # OTP GENERATION
        # ==============================

        otp_code = generate_otp()

        expiry = datetime.utcnow() + timedelta(minutes=5)

        otp = UserOTP(
            userID=user.userID, otpCode=otp_code, expiryTime=expiry, isUsed=False
        )

        await self.repository.save_otp(otp)
        
        
        print("===================================")
        print("OTP CODE:", otp_code)
        print("===================================")

        return {
            "message": "OTP sent successfully",
            "userID": user.userID,
            "otp": otp_code   # TEMPORARY FOR DEVELOPMENT
        }

        # print("OTP:", otp_code)

        # return LoginOTPResponse(message="OTP sent successfully", userID=user.userID)

    async def verify_otp(self, request):

        otp = await self.repository.get_valid_otp(request.userID, request.otpCode)

        if not otp:
            raise HTTPException(status_code=401, detail="Invalid OTP")

        if otp.expiryTime < datetime.utcnow():

            raise HTTPException(status_code=401, detail="OTP expired")

        await self.repository.mark_otp_used(otp.otpID)

        user = await self.repository.get_user_by_id(request.userID)

        token = create_access_token({"userID": user.userID, "roleID": user.roleID})

        return {
            "token": token,
            "user": {
                "userID": user.userID,
                "userName": user.userName,
                "roleID": user.roleID,
            },
        }

    async def get_permissions(self, role_id: int):

        permissions = await self.repository.get_user_permissions(role_id)

        return permissions
