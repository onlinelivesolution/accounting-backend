from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repositories.interfaces.idetailitem_repository import IDetailItemRepository
from src.services.interfaces.idetailitem_service import IDetailItemService
from src.schemas.detailitemautocreate_schema import (
    DetailItemAutoCreateRequest,
    DetailItemRead
)


class DetailItemService(IDetailItemService):
    def __init__(
        self,
        repository: IDetailItemRepository,
        db: AsyncSession
    ):
        self.repository = repository
        self.db = db

    async def auto_create_detail_item(
        self,
        data: DetailItemAutoCreateRequest
    ) -> DetailItemRead:

        try:
            async with self.db.begin():  # transaction starts
                saved_item = await self.repository.auto_create_detail_item(data)

            # ✅ COMMIT happens automatically when exiting `begin()` without error

            return DetailItemRead.model_validate(
                saved_item,
                from_attributes=True
            )

        except ValueError as ex:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ex)
            )

