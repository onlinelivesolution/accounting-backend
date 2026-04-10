from abc import ABC, abstractmethod
from src.schemas.customerreceipt_schema import CustomerReceiptCreate


class ICustomerReceiptService(ABC):

    @abstractmethod
    async def get_customer_invoices(self, customer_id: int):
        pass

    @abstractmethod
    async def create_customer_receipt(self, request: CustomerReceiptCreate):
        pass
    
    @abstractmethod
    async def get_customer_balance(self, customer_id: int):
        pass