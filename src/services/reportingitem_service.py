from src.repositories.interfaces.ireportingitem_repository import IReportingItemRepository
from src.services.interfaces.ireportingitem_service import IReportingItemService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.models.reportingitem import ReportingItem
from src.schemas.controlitem_schema import ControlItemDropdown

from src.schemas.reportingitem_schema import (
    ReportingItemCreate,
    ReportingItemUpdate,
    ReportingItemRead,
)

class ReportingItemService(IReportingItemService):
    def __init__(self, repository: IReportingItemRepository):
        self.repository = repository

    async def add_reporting_item(self, data: ReportingItemCreate) -> ReportingItemRead:

        new_item = ReportingItem(
            reportingItemCode=data.reportingItemCode,
            controlItemCode=data.controlItemCode,
            reportingItemName=data.reportingItemName,
            isActive=data.isActive,
            isDeleted=data.isDeleted,
            createdBy=data.createdBy,
            createdDate=data.createdDate,
            companyCode=data.companyCode,
        )

        saved_item = await self.repository.add_reporting_item(new_item)
        return ReportingItemRead.model_validate(saved_item, from_attributes=True)
    
    async def update_reporting_item(
        self, reportingItemCode: str, reportingitem: ReportingItemUpdate
    ) -> Optional[ReportingItemRead]:
        updated = await self.repository.update_reporting_item(reportingItemCode, reportingitem)
        if updated:
            return ReportingItemRead.model_validate(updated, from_attributes=True)
        return None

    async def get_all_reporting_items(self, skip: int = 0, limit: int = 100) -> List[ReportingItemRead]:
        reportingitems = await self.repository.get_all_reporting_items(skip=skip, limit=limit)
        return [ReportingItemRead.model_validate(ci) for ci in reportingitems["data"]]
    
    async def get_control_items_by_account_type(self, account_type_id: int):
        return await self.repository.get_control_items_by_account_type(account_type_id)
    
    async def get_controlitem_dropdown(self) -> List[ControlItemDropdown]:
        return await self.repository.get_controlitem_dropdown()
    
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        return await self.repository.get_account_types()
    
    async def get_max_reporting_item_code(self, control_item_code: str) -> str:
        max_code = await self.repository.get_max_reporting_item_code(control_item_code)

        if max_code is None:
            return f"{control_item_code}01"   # first item

        last_two = max_code[2:]              # "05"
        next_two = str(int(last_two) + 1).zfill(2)

        return f"{control_item_code}{next_two}"  # "0106"
