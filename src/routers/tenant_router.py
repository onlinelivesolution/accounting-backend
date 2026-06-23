from fastapi import APIRouter, Depends

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
    tenant_id: int,
    service: ITenantService = Depends(get_tenant_service)
):

    return await service.approve_tenant(tenant_id)