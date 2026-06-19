from src.schemas.systemadmin_schema import (
    SystemAdminLoginRequest,
    SystemAdminVerifyOTPRequest
)

from src.services.interfaces.isystemadmin_service import ISystemAdminService
from src.depends.service_depends import get_systemadmin_service

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/admin", tags=["System Admin"])


@router.post("/login")
async def login(
    request: SystemAdminLoginRequest,
    service: ISystemAdminService = Depends(get_systemadmin_service)
):
    return await service.login(request)


@router.post("/verify-otp")
async def verify_otp(
    request: SystemAdminVerifyOTPRequest,
    service: ISystemAdminService = Depends(get_systemadmin_service)
):
    return await service.verify_otp(request)
