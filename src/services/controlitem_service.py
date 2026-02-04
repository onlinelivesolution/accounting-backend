from src.repositories.interfaces.icontrolitem_repository import IControlItemRepository
from src.services.interfaces.icontrolitem_service import IControlItemService
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.fatype_schema import FATypeDropdown
from src.schemas.controlitem_schema import ControlItemRead, ControlItemCreate, ControlItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from typing import List
from src.models.controlitem import ControlItem


class ControlItemService(IControlItemService):
    def __init__(self, repository: IControlItemRepository):
        self.repository = repository
        
    async def add_controlitem(self, data: ControlItemCreate) -> ControlItemRead:

        new_item = ControlItem(
            controlItemCode=data.controlItemCode,
            controlItemName=data.controlItemName,
            isActive=data.isActive,
            accountTypeID=data.accountTypeID,
            isDeleted=data.isDeleted,
            createdBy=data.createdBy,
            createdDate=data.createdDate,
            fATypeID=data.fATypeID,
            companyCode=data.companyCode,
        )

        saved_item = await self.repository.add_controlitem(new_item)
        return ControlItemRead.model_validate(saved_item, from_attributes=True)
    
    
    async def update_control_item(
        self, controlItemCode: str, controlitem: ControlItemUpdate
    ) -> Optional[ControlItemRead]:
        updated = await self.repository.update_control_item(controlItemCode, controlitem)
        if updated:
            return ControlItemRead.model_validate(updated, from_attributes=True)
        return None

    async def get_all_controlitems(self, skip: int = 0, limit: int = 100) -> List[ControlItemRead]:
        controlitems = await self.repository.get_all_controlitems(skip=skip, limit=limit)
        return [ControlItemRead.model_validate(ci) for ci in controlitems["data"]]
    
    async def get_next_control_item_code(self) -> str:
        return await self.repository.get_next_control_item_code()
    
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        return await self.repository.get_account_types()
    
    async def get_fa_types(self) -> List[FATypeDropdown]:
        return await self.repository.get_fa_types()

    async def get_controlitem_by_id(self, controlItemCode: str) -> ControlItem | None:
        controlitem = await self.repository.get_by_id( id=controlItemCode)
        if controlitem:
            return ControlItem.model_validate(controlitem)
        return None

    async def create_controlitem(self, db: AsyncSession, controlitem: ControlItem) -> ControlItem:
        new_controlitem = await self.repository.create(db=db, obj_in=controlitem)
        return ControlItem.model_validate(new_controlitem)

    async def update_controlitem(self, db: AsyncSession, controlItemCode: str, controlitem: ControlItem) -> ControlItem | None:
        updated = await self.repository.update(db=db, id=controlItemCode, obj_in=controlitem)
        if updated:
            return ControlItem.model_validate(updated)
        return None

    async def delete_controlitem(self, db: AsyncSession, controlItemCode: str) -> bool:
        return await self.repository.delete(db=db, id=controlItemCode)
