from common.utils.tenant_security import verify_password
from common.utils.otp_utils import generate_otp
from common.utils.jwt_handler import create_access_token
from src.services.interfaces.itenantauth_service import ITenantAuthService
from src.repositories.interfaces.itenantauth_repository import ITenantAuthRepository
from datetime import datetime, timedelta
import random
from src.core.tenant_database import get_tenant_session
from fastapi import HTTPException


class TenantAuthService(ITenantAuthService):

    def __init__(self, repository):
        self.repository = repository

    async def tenant_login(self, request):

        # Get tenant from master DB
        tenant = await self.repository.get_tenant_by_email(
            request.username.strip()
        )

        if not tenant:
            raise HTTPException(
                status_code=401,
                detail="Tenant not found"
            )

        # Create tenant DB session
        tenant_db = get_tenant_session(
            tenant.databaseName
        )

        # Get user from tenant DB
        user = await self.repository.get_user(
            tenant_db,
            request.username.strip()
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username"
            )

        print("================================")
        print("USERNAME:", repr(user.userName))
        print("INPUT PASSWORD:", repr(request.password))
        print("DB HASH:", repr(user.passwordHash))

        password_valid = verify_password(
            request.password.strip(),
            user.passwordHash.strip()
        )

        print("PASSWORD VALID:", password_valid)
        print("================================")

        # STOP HERE if password invalid
        if password_valid is not True:
            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        otp = str(random.randint(100000, 999999))

        user.otp = otp
        user.otpExpiry = datetime.utcnow() + timedelta(minutes=5)

        await tenant_db.commit()

        print("OTP:", otp)

        return {
            "message": "OTP sent successfully",
            "username": user.userName
        }
    
    async def verify_otp(self, request):

        tenant = await self.repository.get_tenant_by_email(request.username)

        tenant_db = get_tenant_session(tenant.databaseName)

        user = await self.repository.get_user(tenant_db, request.username)

        if user.otp != request.otp:
            raise Exception("Invalid OTP")

        if user.otpExpiry < datetime.utcnow():
            raise Exception("OTP expired")

        token = create_access_token({"sub": user.userName})

        permissions = await self.repository.get_permissions(tenant_db, user.roleID)

        return {
            "token": token,  # IMPORTANT: token, not access_token
            "tenant": tenant.databaseName,
            "user": {
                "userID": user.userID,
                "userName": user.userName,
                "roleID": user.roleID,
                "isSuperAdmin": False,
            },
            "permissions": permissions,
        }

    async def get_permissions(self, username: str):

        tenant = await self.repository.get_tenant_by_email(username)

        tenant_db = get_tenant_session(tenant.databaseName)

        user = await self.repository.get_user(tenant_db, username)

        permissions = await self.repository.get_permissions(tenant_db, user)

        return permissions
