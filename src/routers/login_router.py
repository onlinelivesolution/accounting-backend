from fastapi import APIRouter, Depends, HTTPException

from src.depends.service_depends import get_login_service
from src.services.interfaces.ilogin_service import ILoginService


from src.schemas.loginschema import (
    LoginRequest,
    LoginOTPResponse,
    LoginResponse,
    OTPVerifyRequest,
    OTPVerifyResponse,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginOTPResponse)
async def login(
    request: LoginRequest, service: ILoginService = Depends(get_login_service)
):

    return await service.login(request)


@router.post("/verify-otp", response_model=LoginResponse)
async def verify_otp(
    request: OTPVerifyRequest, service: ILoginService = Depends(get_login_service)
):
    """
    Verify OTP and return JWT + user + permissions
    """

    try:
        result = await service.verify_otp(request)
        return result

    except HTTPException as ex:
        raise ex

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/permissions/{role_id}")
async def get_permissions(
    role_id: int, service: ILoginService = Depends(get_login_service)
):
    return await service.get_permissions(role_id)
