from fastapi import APIRouter, Depends, HTTPException
from src.models.tenant import Tenant
from src.depends.service_depends import get_manage_tenant_service
from src.schemas.managetenant_schema import (
    TenantRegisterRequest,
    TenantResponse,
    TenantStatusUpdateRequest,
)
from src.services.interfaces.imanagetenant_service import IManageTenantService

router = APIRouter(prefix="/api/managetenants", tags=["Manage Tenants"])


@router.post("/registerTenant")
async def register(
    request: TenantRegisterRequest,
    service: IManageTenantService = Depends(get_manage_tenant_service),
):
    return await service.register(request)


@router.get("/getPendingTenants")
async def get_pending_tenants(
    service: IManageTenantService = Depends(get_manage_tenant_service),
):
    return await service.get_pending_tenants()


@router.put("/updateTenantStatus/{tenant_id}")
async def update_tenant_status(
    tenant_id: int,
    request: TenantStatusUpdateRequest,
    service: IManageTenantService = Depends(get_manage_tenant_service),
):
    return await service.update_tenant_status(tenant_id, request)


@router.put("/approveTenant/{tenant_id}")
async def approve(
    tenant_id: int, service: IManageTenantService = Depends(get_manage_tenant_service)
):
    return await service.approve(tenant_id)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    service: IManageTenantService = Depends(get_manage_tenant_service),
):
    tenant = await service.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant
