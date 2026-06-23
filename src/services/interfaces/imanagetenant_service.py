from abc import ABC, abstractmethod

from src.models.tenant import Tenant


class IManageTenantService(ABC):

    @abstractmethod
    async def register(self, request):
        pass

    @abstractmethod
    async def approve_tenant(self, tenant_id: int):
        pass

    @abstractmethod
    async def get_all_tenants(self):
        pass
    
    @abstractmethod
    async def update_tenant_status(self, tenant_id: int, status: str):
        pass
    
    @abstractmethod
    async def get_tenant_by_id(self, tenant_id: int) -> Tenant | None:
        pass
