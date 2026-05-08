from abc import ABC, abstractmethod

from src.schemas.loginschema import (
    LoginRequest,
    LoginOTPResponse,
    VerifyOTPRequest,
    LoginResponse
)


class ILoginService(ABC):

    @abstractmethod
    async def login(
        self,
        request: LoginRequest
    ) -> LoginOTPResponse:
        pass

    @abstractmethod
    async def verify_otp(
        self,
        request: VerifyOTPRequest
    ) -> LoginResponse:
        pass