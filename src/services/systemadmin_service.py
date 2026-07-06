from src.services.interfaces.isystemadmin_service import ISystemAdminService
from src.repositories.interfaces.isystemadmin_repository import ISystemAdminRepository
from common.utils.jwt_handler import create_access_token
from common.utils.systemadmin_security import verify_password
from datetime import datetime, timedelta
from fastapi import HTTPException
import random


class SystemAdminService:

    def __init__(self, repository):
        self.repository = repository

    async def login(self, request):

        user = await self.repository.get_by_username(request.username)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username")

        password_valid = verify_password(request.password, user.passwordHash)

        if not password_valid:
            raise HTTPException(status_code=401, detail="Invalid password")

        otp = str(random.randint(100000, 999999))

        user.otp = otp
        user.otpExpiry = datetime.utcnow() + timedelta(minutes=5)

        await self.repository.update(user)

        return {
            "message": "OTP sent",
            "username": user.username,
            "otp": otp   # Development only
        }

    async def verify_otp(self, request):

        user = await self.repository.get_by_username(request.username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.otp != request.otp:
            raise HTTPException(status_code=401, detail="Invalid OTP")

        if datetime.utcnow() > user.otpExpiry:
            raise HTTPException(status_code=401, detail="OTP expired")

        token = create_access_token({"sub": user.username, "role": "SystemAdmin"})

        return {
            "token": token,
            "user": {
                "userID": user.systemUserID,
                "userName": user.username,
                "roleID": user.role,
                "isSuperAdmin": True,
            },
            "permissions": [],
            "message": "Login successful",
        }
