from fastapi import Depends, HTTPException

from src.depends.auth_depends import get_current_user

from src.core.tenant_database import get_tenant_session


async def get_tenant_db(current_user=Depends(get_current_user)):

    database_name = current_user.get("tenant")

    if not database_name:

        raise HTTPException(status_code=401, detail="Tenant not found in token")

    tenant_db = get_tenant_session(database_name)

    try:

        yield tenant_db

    finally:

        await tenant_db.close()
