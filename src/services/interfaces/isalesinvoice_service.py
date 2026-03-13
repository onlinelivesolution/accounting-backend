from abc import ABC, abstractmethod
from src.schemas.salesinvoice_schema import SalesInvoiceCreateRequest, SalesInvoiceUpdateRequest
from src.models.salesinvoice import SalesInvoice

class ISalesInvoiceService(ABC):
    
    @abstractmethod
    async def create_sales_invoice(self, request: SalesInvoiceCreateRequest) -> SalesInvoice:
        pass

    @abstractmethod
    async def get_sales_invoice_by_id(self, salesinvoice_id: int) -> SalesInvoice | None:
        pass

    @abstractmethod
    async def get_all_sales_invoice(self) -> list[SalesInvoice]:
        pass
    
    @abstractmethod
    async def get_next_salesinvoice_no(self) -> str:
        pass