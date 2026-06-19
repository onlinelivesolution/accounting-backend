from abc import ABC, abstractmethod

from src.models.tenant import Tenant


class IManageTenantRepository(ABC):

    @abstractmethod
    async def create_tenant(self, tenant):
        pass

    @abstractmethod
    async def get_by_email(self, email: str):
        pass

    @abstractmethod
    async def get_pending_tenants(self):
        pass

    @abstractmethod
    async def get_tenant_by_id(self, tenant_id: int) -> Tenant | None:
        pass

    @abstractmethod
    async def update_tenant_status(self, tenant):
        pass
