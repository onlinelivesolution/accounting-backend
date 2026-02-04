from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.reportingitem import ReportingItem
from src.schemas.reportingitem_schema import ReportingItemUpdate
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.controlitem_schema import ControlItemDropdown

class IReportingItemRepository(ABC):
    
    @abstractmethod
    async def add_reporting_item(self, reportingitem: ReportingItem) -> ReportingItem:
        pass 
    
    @abstractmethod
    async def update_reporting_item(self, reportingItemCode: str, reportingitem: ReportingItemUpdate) -> Optional[ReportingItem]:
        pass
    
    @abstractmethod
    async def get_all_reporting_items(self, db: AsyncSession, skip: int, limit: int) -> List[ReportingItem]:
        pass
    
    @abstractmethod
    async def get_control_items_by_account_type(self, account_type_id: int):
        pass
    
    @abstractmethod
    async def get_controlitem_dropdown(self) -> List[ControlItemDropdown]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        pass
    
    @abstractmethod
    async def get_max_reporting_item_code(self, control_item_code: str) -> Optional[str]:
        pass

