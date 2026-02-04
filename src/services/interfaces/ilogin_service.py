from abc import ABC, abstractmethod
from src.schemas.loginschema import LoginRequest, LoginResponse


class ILoginService(ABC):
    @abstractmethod
    async def login(self, request: LoginRequest) -> LoginResponse:
        pass
