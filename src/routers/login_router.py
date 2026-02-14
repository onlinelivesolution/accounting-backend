from fastapi import APIRouter, Depends

from src.depends.service_depends import get_login_service
from src.services.interfaces.ilogin_service import ILoginService
from src.schemas.loginschema import LoginRequest, LoginResponse


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, service: ILoginService = Depends(get_login_service)):
    """
    Handle user login.
    Input: { "username": "raju", "password": "123" }
    Output: token + user info + permissions
    """
    return await service.login(request)
