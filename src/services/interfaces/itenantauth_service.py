from abc import ABC, abstractmethod


class ITenantAuthService(ABC):

    @abstractmethod
    async def tenant_login(self, request):
        pass

    @abstractmethod
    async def verify_otp(self, request):
        pass

    @abstractmethod
    async def get_permissions(self, username: str):
        pass
