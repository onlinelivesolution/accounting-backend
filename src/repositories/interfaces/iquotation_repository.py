from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.models.quotation import Quotation
from common.enum.commenum import QuotationFilter


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
    async def get_quotation_filters(self, filter_type: str):
        pass
