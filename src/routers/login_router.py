from fastapi import APIRouter, Depends

from src.depends.service_depends import get_login_service
from src.services.interfaces.ilogin_service import ILoginService

from src.schemas.loginschema import (
    LoginRequest,
    LoginOTPResponse,
    VerifyOTPRequest,
    LoginResponse
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=LoginOTPResponse
)
async def login(
    request: LoginRequest,
    service: ILoginService = Depends(get_login_service)
):

    return await service.login(request)


@router.post(
    "/verify-otp",
    response_model=LoginResponse
)
async def verify_otp(
    request: VerifyOTPRequest,
    service: ILoginService = Depends(get_login_service)
):

    return await service.verify_otp(request)