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
    async def get_all_tenants(self):
        pass


    @abstractmethod
    async def update_tenant_status(self, tenant):
        pass

    @abstractmethod
    async def get_by_id(self, tenant_id: int) -> Tenant | None:
        pass

    @abstractmethod
    async def get_tenant_by_id(self, tenant_id: int):
        pass

    @abstractmethod
    async def update(self, tenant: Tenant):
        pass

    @abstractmethod
    async def create_tenant_admin_user(
        self, database_name: str, email: str, password_hash: str
    ):
        pass
