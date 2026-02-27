from abc import ABC, abstractmethod
from src.models.quotation import Quotation


class IQuotationRepository(ABC):

    @abstractmethod
    async def create(self, quotation: Quotation) -> Quotation:
        pass

    @abstractmethod
    async def get_by_id(self, quotationID: int) -> Quotation | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Quotation]:
        pass

    @abstractmethod
    async def get_next_quotation_no(self) -> str:
        pass

    @abstractmethod
    def get_quotation_table(self) -> list[Quotation]:
        pass
    
    @abstractmethod
    async def get_quotations(self, filter_type: str):
        pass
    
    @abstractmethod
    async def get_quotation_dropdown(self):
        pass
    
    @abstractmethod
    async def get_quotation_for_sales_order(self, quotationID: int):
        pass
