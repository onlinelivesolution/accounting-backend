from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.interfaces.itenant_repository import ITenantRepository

from src.schemas.tenant_schema import TenantCreate

# from src.core.tenant_table_creator import create_tenant_tables
from src.core.tenant_schema_creator import create_tenant_schema
from src.core.tenant_seed_data import copy_master_data

from src.models.tenant import Tenant

from src.core.tenant_provision import create_tenant_database


class TenantRepository(ITenantRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_tenant(self, request: TenantCreate):

        try:

            # ==================================
            # CREATE DATABASE
            # ==================================

            database_name = await create_tenant_database(request.email)

            # ==================================
            # CREATE ALL TABLES
            # ==================================

            await create_tenant_schema(database_name)

            # ==================================
            # SEED DATA
            # ==================================

            await copy_master_data(database_name, request.email)

            # ==================================
            # SAVE TENANT INFO
            # ==================================

            tenant = Tenant(
                companyName=request.companyName,
                email=request.email,
                databaseName=database_name,
            )

            self.db.add(tenant)

            await self.db.commit()

            return {
                "databaseName": database_name,
                "message": "Tenant created successfully",
            }

        except Exception:

            await self.db.rollback()
            raise
