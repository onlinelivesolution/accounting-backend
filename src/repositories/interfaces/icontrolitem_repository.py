from abc import ABC, abstractmethod
from typing import List, Dict, Any
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.controlitem import ControlItem
from src.schemas.controlitem_schema import ControlItemUpdate, ControlItemRead, ControlItemCreate
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.fatype_schema import FATypeDropdown

class IControlItemRepository(ABC):
    
    @abstractmethod
    async def add_controlitem(self, controlitem: ControlItem) -> ControlItem:
        pass 
    
    @abstractmethod
    async def update_control_item(self, controlItemCode: str, controlitem: ControlItemUpdate) -> Optional[ControlItem]:
        pass
    
    @abstractmethod
    async def get_all_controlitems(self, db: AsyncSession, skip: int, limit: int) -> List[ControlItem]:
        pass

    @abstractmethod
    async def get_next_control_item_code(self, db: AsyncSession) -> str:
        pass
    
    @abstractmethod
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        pass
    
    @abstractmethod
    async def get_fa_types(self) -> List[FATypeDropdown]:
        pass
