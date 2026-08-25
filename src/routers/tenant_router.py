from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from src.core.auth_dependency import (
    get_current_user,
)
from src.schemas.tenant_schema import TenantCreate

from src.services.interfaces.itenant_service import ITenantService

from src.depends.service_depends import get_tenant_service

router = APIRouter(prefix="/api/tenant", tags=["Tenant"])


@router.post("/register")
async def register_tenant(
    request: TenantCreate, service: ITenantService = Depends(get_tenant_service)
):

    result = await service.register_tenant(request)

    return {"message": "Tenant created successfully", "data": result}


@router.put("/approve/{tenant_id}")
async def approve_tenant(
    tenant_id: int, service: ITenantService = Depends(get_tenant_service)
):

    return await service.approve_tenant(tenant_id)


@router.post("/banner")
async def upload_tenant_banner(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    service=Depends(get_tenant_service),
):
    tenant_name = current_user.get("tenant")

    if not tenant_name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant information is missing.",
        )

    return await service.upload_banner(
        database_name=tenant_name,
        file=file,
    )
