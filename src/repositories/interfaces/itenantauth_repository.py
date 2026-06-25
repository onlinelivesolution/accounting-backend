from abc import ABC, abstractmethod


class ITenantAuthRepository(ABC):

    @abstractmethod
    async def get_tenant_by_email(self, email: str):
        pass

    @abstractmethod
    async def get_user(self, tenant_db, username: str):
        pass

    @abstractmethod
    async def get_permissions(self, tenant_db, role_id: int):
        pass
