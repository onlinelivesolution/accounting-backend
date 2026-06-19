from sqlalchemy import select
from src.models.tenant import Tenant


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

    async def get_pending_tenants(self):

        stmt = select(Tenant).where(Tenant.status == "Pending")

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
