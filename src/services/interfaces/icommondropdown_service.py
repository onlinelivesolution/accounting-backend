from src.schemas.commondropdown_schema import DropdownItem
from src.schemas.commondropdown_schema import LineItemDropdown, CustomerDropdown
from abc import ABC, abstractmethod
from typing import List

class ICommonDropdownService(ABC):

    @abstractmethod
    async def get_vat_rate_dropdown(self, company_code: str) -> List[DropdownItem]:
        pass

    @abstractmethod
    async def get_lineitem_dropdown(self) -> List[LineItemDropdown]:
        pass

    @abstractmethod
    async def get_customer_dropdown(self) -> List[CustomerDropdown]:
        pass
