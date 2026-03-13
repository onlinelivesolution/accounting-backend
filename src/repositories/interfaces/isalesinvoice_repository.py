from abc import ABC, abstractmethod
from src.models.salesinvoice import SalesInvoice
from src.models.salesinvoicedetail import SalesInvoiceDetail

class ISalesInvoiceRepository(ABC):
    
    @abstractmethod
    async def create_sales_invoice(self, salesinvoice: SalesInvoice) -> SalesInvoice:
        pass
    
    @abstractmethod
    async def get_sales_invoice_by_id(self, salesInvoiceID: int) -> SalesInvoice | None:
        pass
    
    @abstractmethod
    async def get_all_sales_invoice(self) -> list[SalesInvoice]:
        pass
    
    @abstractmethod
    async def get_next_salesinvoice_no(self) -> list:
        pass