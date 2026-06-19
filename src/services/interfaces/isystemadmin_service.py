from abc import ABC, abstractmethod


class ISystemAdminService(ABC):

    @abstractmethod
    async def login(self, request):
        pass

    @abstractmethod
    async def verify_otp(self, request):
        pass
