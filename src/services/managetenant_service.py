from datetime import datetime

from requests import request
from src.models.tenant import Tenant
from src.services.interfaces.imanagetenant_service import IManageTenantService
from src.repositories.interfaces.imanagetenant_repository import IManageTenantRepository
from common.utils.systemadmin_security import hash_password
from src.core.tenant_provision import create_tenant_database
from src.core.tenant_schema_creator import create_tenant_schema
from src.core.tenant_seed_data import copy_master_data
from src.core.tenant_database_name import generate_database_name
from src.core.tenant_accounting_period import create_default_accounting_period
from src.core.tenant_initializer import initialize_new_tenant


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
    

    # approve tenant and create tenant database, schema, and seed data
    async def approve_tenant(self, tenant_id: int):

        tenant = await self.repository.get_tenant_by_id(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        if tenant.status == "Approved":
            return {"message": "Already approved"}

        # Create database name from email
        database_name = generate_database_name(tenant.email)

        # Create database
        await create_tenant_database(database_name)

        import asyncio

        await asyncio.sleep(5)

        # Create tables
        await create_tenant_schema(database_name)

        # Copy master data + create admin user
        await initialize_new_tenant(
            database_name,
            tenant,
        )

        tenant.databaseName = database_name
        tenant.status = "Approved"
        tenant.isActive = True

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
