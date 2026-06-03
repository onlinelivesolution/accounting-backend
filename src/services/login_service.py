from datetime import datetime, timedelta

from fastapi import HTTPException

from common.utils.jwt_handler import create_access_token
from common.utils.security import verify_password
from common.utils.otp_utils import generate_otp

from src.models.userotp import UserOTP

from src.core.tenant_session import get_tenant_db_by_email
from src.core.tenant_session import get_tenant_db_by_database
from src.repositories.login_repository import LoginRepository


class LoginService:
    def __init__(self, repository):
        self.repository = repository

    async def login(self, request):

        # =====================================
        # GET TENANT DB
        # =====================================

        tenant_db, database_name = await get_tenant_db_by_email(request.userName)

        if not tenant_db:

            raise HTTPException(status_code=404, detail="Tenant not found")

        try:

            # =====================================
            # CREATE TENANT REPOSITORY
            # =====================================

            repository = LoginRepository(tenant_db)

            # =====================================
            # GET USER
            # =====================================

            user = await repository.get_user_by_username(request.userName)

            if not user:

                raise HTTPException(status_code=401, detail="Invalid username")

            # =====================================
            # VERIFY PASSWORD
            # =====================================

            is_valid, needs_rehash = verify_password(
                request.password, user.passwordHash
            )

            if not is_valid:

                await repository.increment_failed_attempts(user.userID)

                raise HTTPException(status_code=401, detail="Invalid password")

            # =====================================
            # RESET FAILED ATTEMPTS
            # =====================================

            await repository.reset_failed_attempts(user.userID)

            # =====================================
            # GENERATE OTP
            # =====================================

            otp_code = generate_otp()

            expiry = datetime.utcnow() + timedelta(minutes=5)

            otp = UserOTP(
                userID=user.userID, otpCode=otp_code, expiryTime=expiry, isUsed=False
            )

            await repository.save_otp(otp)

            print("DATABASE NAME:", database_name)

            return {
                "message": "OTP sent successfully",
                "userID": user.userID,
                "tenant": database_name,
                "otp": otp_code,
            }

        finally:

            await tenant_db.close()


    async def verify_otp(self, request):

        tenant_db, database_name = await get_tenant_db_by_database(
            request.tenant
        )

        if not tenant_db:
            raise HTTPException(status_code=404, detail="Tenant not found")

        try:

            repository = LoginRepository(tenant_db)

            otp = await repository.get_valid_otp(
                request.userID,
                request.otpCode
            )

            if not otp:
                raise HTTPException(status_code=401, detail="Invalid OTP")

            if otp.expiryTime < datetime.utcnow():
                raise HTTPException(status_code=401, detail="OTP expired")

            await repository.mark_otp_used(otp.otpID)

            user = await repository.get_user_by_id(request.userID)
            
            print("===================================")
            print("USER ID:", user.userID)
            print("USERNAME:", user.userName)
            print("ROLE ID:", user.roleID)
            print("===================================")

            token = create_access_token(
                {
                    "userID": user.userID,
                    "roleID": user.roleID,
                    "tenant": database_name,
                }
            )

            return {
                "token": token,
                "tenant": database_name,
                "user": {
                    "userID": user.userID,
                    "userName": user.userName,
                    "roleID": user.roleID,
                },
            }

        finally:
            await tenant_db.close()
    
    async def get_permissions(self, role_id: int):

        return await self.repository.get_user_permissions(role_id)
