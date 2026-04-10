from abc import ABC, abstractmethod
from typing import List
from src.models.salesinvoice import SalesInvoice
from src.models.customerreceipt_model import CustomerReceipt


class ICustomerReceiptRepository(ABC):

    @abstractmethod
    async def get_customer_invoices(self, customer_id: int) -> List[SalesInvoice]:
        pass

    @abstractmethod
    async def get_total_paid_amount(self, invoice_id: int) -> float:
        pass

    @abstractmethod
    async def create_customer_receipt(self, receipt: CustomerReceipt) -> CustomerReceipt:
        pass

    @abstractmethod
    async def get_invoice_by_id(self, invoice_id: int) -> SalesInvoice:
        pass
    
