from sqlalchemy import select
from src.models.tenant import Tenant
from sqlalchemy.ext.asyncio import create_async_engine
from src.services.database import Base
from src.models.systemuser_model import SystemUser


class ManageTenantRepository:

    def __init__(self, db):
        self.db = db

    async def create_tenant(self, tenant):

        self.db.add(tenant)

        await self.db.commit()

        await self.db.refresh(tenant)

        return tenant

    async def get_by_email(self, email: str):

        stmt = select(Tenant).where(Tenant.email == email)

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all_tenants(self):

        stmt = select(Tenant)

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_tenant_by_id(self, tenant_id: int):
        stmt = select(Tenant).where(Tenant.tenantID == tenant_id)

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def update_tenant_status(self, tenant):

        self.db.add(tenant)

        await self.db.commit()

        await self.db.refresh(tenant)

        return tenant

    async def create_tenant_admin_user(
        self, database_name: str, email: str, password_hash: str
    ):

        engine = create_async_engine(f"mssql+aioodbc://.../{database_name}")

        async with engine.begin() as conn:

            await conn.run_sync(Base.metadata.create_all)

            await conn.execute(
                SystemUser.__table__.insert().values(
                    username=email,
                    passwordHash=password_hash,
                    role="TenantAdmin",
                    isActive=True,
                )
            )

    async def update(self, tenant: Tenant):

        self.db.add(tenant)

        await self.db.commit()

        await self.db.refresh(tenant)

        return tenant
