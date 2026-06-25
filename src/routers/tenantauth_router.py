from fastapi import APIRouter, Depends
from src.schemas.tenantauth_schema import LoginRequest, VerifyOTPRequest
from src.depends.service_depends import get_tenant_auth_service
from src.services.interfaces.itenantauth_service import ITenantAuthService

router = APIRouter(prefix="/api/tenantauth", tags=["Authentication"])


@router.post("/tenantLogin")
async def tenant_login(
    request: LoginRequest,
    service: ITenantAuthService = Depends(get_tenant_auth_service),
):
    return await service.tenant_login(request)


@router.post("/verifyOTP")
async def verify_otp(
    request: VerifyOTPRequest,
    service: ITenantAuthService = Depends(get_tenant_auth_service),
):
    return await service.verify_otp(request)


@router.get("/permissions/{username}")
async def get_permissions(
    username: str, service: ITenantAuthService = Depends(get_tenant_auth_service)
):

    return await service.get_permissions(username)
