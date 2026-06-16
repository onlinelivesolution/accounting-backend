from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.tenant_dependency import get_current_tenant
from src.core.tenant_session_factory import get_tenant_session


async def get_tenant_db(
    tenant: str = Depends(get_current_tenant),
) -> AsyncGenerator[AsyncSession, None]:

    db = get_tenant_session(tenant)

    try:
        yield db
    finally:
        await db.close()
