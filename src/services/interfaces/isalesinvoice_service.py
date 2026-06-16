from abc import ABC, abstractmethod
from src.schemas.salesinvoice_schema import (
    SalesInvoiceCreateRequest,
    SalesInvoiceUpdateRequest,
)
from src.models.salesinvoice import SalesInvoice
from sqlalchemy.ext.asyncio import AsyncSession


class ISalesInvoiceService(ABC):

    @abstractmethod
    async def create_sales_invoice(
        self, request: SalesInvoiceCreateRequest
    ) -> SalesInvoice:
        pass

    @abstractmethod
    async def get_sales_invoice_by_id(self, salesInvoiceID: int) -> SalesInvoice | None:
        pass

    @abstractmethod
    async def get_all_sales_invoice(self) -> list[SalesInvoice]:
        pass

    @abstractmethod
    async def get_next_salesinvoice_no(self) -> str:
        pass

    @abstractmethod
    async def get_filter_sales_invoice(self, filter_type: str):
        pass

    @abstractmethod
    async def list_sales_invoice(self) -> list[SalesInvoice]:
        pass

    @abstractmethod
    async def load_sales_invoice_table(self) -> list[SalesInvoice]:
        pass

    @abstractmethod
    async def update_sales_invoice(
        self, salesinvoice_id: int, request: SalesInvoiceUpdateRequest
    ):
        pass

    @abstractmethod
    async def update_sales_invoice_status(self, salesinvoice_id: int, status: str):
        pass

    @abstractmethod
    async def copy_sales_invoice(self, salesinvoice_id: int):
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
    async def approve_sales_invoice(self, salesInvoiceID: int):
        pass
