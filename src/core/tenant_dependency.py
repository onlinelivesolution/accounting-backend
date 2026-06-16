from fastapi import Depends, HTTPException
from src.core.auth_dependency import get_current_user


async def get_current_tenant(user: dict = Depends(get_current_user)):
    tenant = user.get("tenant")

    if not tenant:
        raise HTTPException(status_code=401, detail="Tenant missing")

    return tenant
