from abc import ABC, abstractmethod

from src.schemas.tenant_schema import TenantCreate


class ITenantRepository(ABC):

    @abstractmethod
    async def register_tenant(self, request: TenantCreate):
        pass

    @abstractmethod
    async def get_by_database_name(
        self,
        database_name: str,
    ):
        pass

    @abstractmethod
    async def update_banner_path(
        self,
        tenant,
        banner_path: str,
    ):
        pass


