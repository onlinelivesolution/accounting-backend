from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from src.schemas.controlitem_schema import ControlItemCreate, ControlItemUpdate, ControlItemRead
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.fatype_schema import FATypeDropdown

class IControlItemService(ABC):
    
    @abstractmethod
    async def add_controlitem(self, data: ControlItemCreate) -> ControlItemRead:
        pass
    
    @abstractmethod
    async def update_control_item(self, ontrolItemCode: str, controlitem: ControlItemUpdate) -> Optional[ControlItemRead]:
        pass
    
    @abstractmethod
    async def get_all_controlitems(self, skip: int, limit: int):
        pass
    
    @abstractmethod
    async def get_next_control_item_code(self) -> str:
        pass
        
    @abstractmethod
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        pass
    
    @abstractmethod
    async def get_fa_types(self) -> List[FATypeDropdown]:
        pass
