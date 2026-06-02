from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.interfaces.itenant_repository import ITenantRepository

from src.schemas.tenant_schema import TenantCreate
from src.core.tenant_table_creator import create_tenant_tables
from src.core.tenant_seed_data import copy_master_data

from src.models.tenant import Tenant

from src.core.tenant_database import create_tenant_database


class TenantRepository(ITenantRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_tenant(self, request: TenantCreate):

        # Create Database
        database_name = await create_tenant_database(request.email)

        # Create tables
        await create_tenant_tables(database_name)
        await copy_master_data(database_name, request.email)

        # Save Tenant Info
        tenant = Tenant(
            companyName=request.companyName,
            email=request.email,
            databaseName=database_name,
        )

        self.db.add(tenant)

        await self.db.commit()

        return {"databaseName": database_name}
