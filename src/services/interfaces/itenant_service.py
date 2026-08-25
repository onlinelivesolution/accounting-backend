from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile
from src.schemas.tenant_schema import TenantCreate


class ITenantService(ABC):

    @abstractmethod
    async def register_tenant(self, request: TenantCreate):
        pass

        # ==========================================================

    # Get Tenant
    # ==========================================================

    @abstractmethod
    async def get_tenant_by_database_name(
        self,
        database_name: str,
    ):
        pass

    # ==========================================================
    # Upload Tenant Banner
    # ==========================================================

    @abstractmethod
    async def upload_banner(
        self,
        database_name: str,
        file: UploadFile,
    ):
        pass

    # ==========================================================
    # Get Tenant Banner
    # ==========================================================

    @abstractmethod
    async def get_banner(
        self,
        database_name: str,
    ) -> Optional[str]:
        pass
