from src.services.interfaces.itenant_service import ITenantService
from fastapi import (
    HTTPException,
    UploadFile,
    status,
)

from src.services.tenant_banner_service import (
    TenantBannerService,
)
from src.schemas.tenant_schema import TenantCreate

from src.repositories.interfaces.itenant_repository import ITenantRepository


class TenantService(ITenantService):

    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    async def register_tenant(self, request: TenantCreate):

        return await self.tenant_repository.register_tenant(request)
    
    async def get_tenant_by_database_name(
        self,
        database_name: str,
    ):
        return await self.tenant_repository.get_by_database_name(
            database_name
        )

    async def upload_banner(
        self,
        database_name: str,
        file: UploadFile,
    ):

        # -----------------------------------------
        # Find tenant
        # -----------------------------------------

        tenant = await self.tenant_repository.get_by_database_name(database_name)

        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found.",
            )

        # -----------------------------------------
        # Save physical file
        # -----------------------------------------

        banner_path = await self.banner_service.save_banner(
            file=file,
            tenant_name=database_name,
        )

        # -----------------------------------------
        # Save path in master DB
        # -----------------------------------------

        tenant = await self.tenant_repository.update_banner_path(
            tenant=tenant,
            banner_path=banner_path,
        )

        return {
            "message": "Tenant banner uploaded successfully.",
            "bannerPath": tenant.bannerPath,
        }
    
    async def get_banner(
        self,
        database_name: str,
    ):
        tenant = await self.tenant_repository.get_by_database_name(
            database_name
        )

        if not tenant:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found.",
            )

        return {
            "bannerPath": tenant.bannerPath
        }
