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
    
    @abstractmethod
    def load_sales_invoice_table(self) -> list[SalesInvoice]:
        pass
    
    @abstractmethod
    async def get_filter_sales_invoice(self, filter_type: str):
        pass
    
    @abstractmethod
    async def update_sales_invoice_status(self, entity: SalesInvoice) -> SalesInvoice:
        pass
    
    @abstractmethod
    async def get_sales_invoice_with_details(self, salesinvoice_id: int) -> SalesInvoice:
        pass
    
    @abstractmethod
    async def add_sales_invoice_detail(self, entity: SalesInvoiceDetail) -> SalesInvoiceDetail:
        pass
    
    @abstractmethod
    async def get_sales_order_dropdown(self):
        pass
    
    @abstractmethod
    async def get_sales_order_for_sales_invoice(self, salesOrderID: int):
        pass
    
    @abstractmethod
    async def update(self, invoice: SalesInvoice) -> SalesInvoice:
        pass
    
    @abstractmethod
    async def approve_sales_invoice(self, invoice: SalesInvoice) -> SalesInvoice:
        pass