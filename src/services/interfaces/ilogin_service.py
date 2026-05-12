from abc import ABC, abstractmethod


from src.schemas.loginschema import (
    LoginRequest,
    LoginOTPResponse,
    OTPVerifyResponse,
    OTPVerifyRequest
)


class ILoginService(ABC):

    @abstractmethod
    async def login(
        self,
        request: LoginRequest
    ) -> LoginOTPResponse:
        pass

    @abstractmethod
    async def verify_otp(self, request: OTPVerifyRequest) -> OTPVerifyResponse:
        pass