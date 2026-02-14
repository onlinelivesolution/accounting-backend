from abc import ABC, abstractmethod
from src.schemas.quotation_schema import QuotationCreateRequest
from src.models.quotation import Quotation


class IQuotationService(ABC):

    @abstractmethod
    async def create_quotation(self, request: QuotationCreateRequest) -> Quotation:
        pass

    @abstractmethod
    async def get_quotation(self, quotation_id: int) -> Quotation | None:
        pass

    @abstractmethod
    async def list_quotations(self) -> list[Quotation]:
        pass

    @abstractmethod
    async def get_next_quotation_no(self) -> str:
        pass
