from abc import ABC, abstractmethod

from src.schemas.tenant_schema import TenantCreate


class ITenantRepository(ABC):

    @abstractmethod
    async def register_tenant(self, request: TenantCreate):
        pass
    
    # @abstractmethod
    # async def create_tenant(self, tenant):
    #     pass


    # @abstractmethod
    # async def get_by_email(self, email: str):
    #     pass


    # @abstractmethod
    # async def get_pending_tenants(self):
    #     pass


    # @abstractmethod
    # async def get_by_id(self, tenant_id: int):
    #     pass
    
    
