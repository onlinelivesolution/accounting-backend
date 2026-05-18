from abc import ABC, abstractmethod

from src.schemas.tenant_schema import TenantCreate


class ITenantRepository(ABC):

    @abstractmethod
    async def register_tenant(self, request: TenantCreate):
        pass
