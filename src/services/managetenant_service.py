from datetime import datetime

from requests import request
from src.models.tenant import Tenant
from src.services.interfaces.imanagetenant_service import IManageTenantService
from src.repositories.interfaces.imanagetenant_repository import IManageTenantRepository
from common.utils.systemadmin_security import hash_password


class ManageTenantService(IManageTenantService):

    def __init__(self, repository):
        self.repository = repository

    async def register(self, request):

        existing = await self.repository.get_by_email(request.email)

        if existing:
            raise Exception("Email already exists")

        tenant = Tenant(
            companyName=request.companyName,
            adminName=request.adminName,
            databaseName=request.databaseName,
            email=request.email,
            # HASH PASSWORD
            passwordHash=hash_password(request.password),
            isActive=request.isActive,
            status="Pending",            
            createdDate=datetime.utcnow(),
        )

        return await self.repository.create_tenant(tenant)

    async def get_pending_tenants(self):

        return await self.repository.get_pending_tenants()

    async def update_tenant_status(self, tenant_id: int, request):

        tenant = await self.repository.get_tenant_by_id(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        tenant.status = request.status

        await self.repository.update_tenant_status(tenant)

        return {"message": "Status updated successfully"}

    async def get_tenant_by_id(self, tenant_id: int):
        return await self.repository.get_tenant_by_id(tenant_id)

    async def approve(self, tenant_id: int):

        tenant = await self.repository.get_tenant_by_id(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        tenant.status = "Approved"

        await self.repository.update_tenant_status(tenant)

        return {"message": "Tenant approved successfully"}
