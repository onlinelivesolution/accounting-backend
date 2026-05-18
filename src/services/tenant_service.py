from src.services.interfaces.itenant_service import ITenantService

from src.schemas.tenant_schema import TenantCreate

from src.repositories.interfaces.itenant_repository import ITenantRepository


class TenantService(ITenantService):

    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    async def register_tenant(self, request: TenantCreate):

        return await self.tenant_repository.register_tenant(request)
