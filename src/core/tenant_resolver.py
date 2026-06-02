from sqlalchemy import select

from src.services.database import AsyncSessionLocal
from src.models.tenant import Tenant


async def get_database_by_email(email: str):

    async with AsyncSessionLocal() as db:

        result = await db.execute(select(Tenant).where(Tenant.email == email))

        tenant = result.scalars().first()

        if not tenant:
            return None

        return tenant.databaseName
