from datetime import datetime

from requests import request
from src.models.tenant import Tenant
from src.services.interfaces.imanagetenant_service import IManageTenantService
from src.repositories.interfaces.imanagetenant_repository import IManageTenantRepository
from common.utils.systemadmin_security import hash_password
from src.core.tenant_provision import create_tenant_database
from src.core.tenant_schema_creator import create_tenant_schema
from src.core.tenant_seed_data import copy_master_data


class ManageTenantService(IManageTenantService):

    def __init__(self, repository: IManageTenantRepository):
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

    async def get_all_tenants(self):

        return await self.repository.get_all_tenants()

    async def update_tenant_status(self, tenant_id: int, request):

        tenant = await self.repository.get_tenant_by_id(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        tenant.status = request.status

        await self.repository.update_tenant_status(tenant)

        return {"message": "Status updated successfully"}

    async def get_tenant_by_id(self, tenant_id: int):
        return await self.repository.get_tenant_by_id(tenant_id)

    async def approve_tenant(self, tenant_id: int):

        # 1. Get tenant from master DB
        tenant = await self.repository.get_tenant_by_id(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        # Prevent duplicate provisioning
        if tenant.status == "Approved":

            return {"message": "Already approved"}

        # 2. Generate database name

        database_name = f"tenant_{tenant.tenantID}"

        # 3. Create SQL Server database

        await create_tenant_database(database_name)

        # SQL Server sometimes needs a moment
        import asyncio

        await asyncio.sleep(3)

        # 4. Create tables

        await create_tenant_schema(database_name)

        # 5. Copy master data

        await copy_master_data(database_name, tenant.email)

        # 6. Create admin user inside tenant DB

        await self.repository.create_tenant_admin_user(
            database_name=database_name,
            email=tenant.email,
            password_hash=tenant.passwordHash,
        )

        # 7. Update tenant status in master DB

        tenant.status = "Approved"
        tenant.databaseName = database_name
        tenant.isActive = True
        tenant.approvedDate = datetime.utcnow()

        await self.repository.update(tenant)

        return {
            "message": "Tenant approved successfully",
            "databaseName": database_name,
        }

    async def get_tenant_by_id(self, tenant_id: int):

        tenant = await self.repository.get_tenant_by_id(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        return tenant
