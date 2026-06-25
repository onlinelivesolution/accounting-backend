from common.utils.security import verify_password
from common.utils.otp_utils import generate_otp
from common.utils.jwt_handler import create_access_token
from src.services.interfaces.itenantauth_service import ITenantAuthService
from src.repositories.interfaces.itenantauth_repository import ITenantAuthRepository
from datetime import datetime, timedelta
from src.core.tenant_database import get_tenant_session


class TenantAuthService(ITenantAuthService):

    def __init__(self, repository):
        self.repository = repository

    async def tenant_login(self, request):

        # Master DB
        tenant = await self.repository.get_tenant_by_email(request.username)

        if not tenant:
            raise Exception("Tenant not found")

        if tenant.status != "Approved":
            raise Exception(f"Tenant status is {tenant.status}")

        # Open tenant DB dynamically
        tenant_db = get_tenant_session(tenant.databaseName)

        # Get user from tenant DB
        user = await self.repository.get_user(tenant_db, request.username)

        if not user:
            raise Exception("Invalid username")

        password_valid = verify_password(request.password, user.passwordHash)

        if not password_valid:
            raise Exception("Invalid password")

        # Generate OTP
        otp = generate_otp()

        user.otp = otp
        user.otpExpiry = datetime.utcnow() + timedelta(minutes=5)

        await tenant_db.commit()

        # Send email here
        print("OTP:", otp)

        return {"message": "OTP sent successfully", "otp": otp}

    async def verify_otp(self, request):

        tenant = await self.repository.get_tenant_by_email(request.username)

        tenant_db = get_tenant_session(tenant.databaseName)

        user = await self.repository.get_user(tenant_db, request.username)

        if user.otp != request.otp:
            raise Exception("Invalid OTP")

        if user.otpExpiry < datetime.utcnow():
            raise Exception("OTP expired")

        token = create_access_token(data={"sub": user.userName})

        return {"access_token": token, "token_type": "bearer"}

    async def get_permissions(self, username: str):

        tenant = await self.repository.get_tenant_by_email(username)

        tenant_db = get_tenant_session(tenant.databaseName)

        user = await self.repository.get_user(tenant_db, username)

        permissions = await self.repository.get_permissions(tenant_db, user)

        return permissions
