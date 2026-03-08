from abc import ABC, abstractmethod
from src.models.salesorder import SalesOrder

class ISalesOrderRepository(ABC):

    @abstractmethod
    async def create(self, salesorder: SalesOrder) -> SalesOrder:
        pass

    @abstractmethod
    async def get_by_id(self, salesOrderID: int) -> SalesOrder | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[SalesOrder]:
        pass

    @abstractmethod
    async def get_next_salesorder_no(self) -> list:
        pass

    @abstractmethod
    def load_sales_order_table(self) -> list[SalesOrder]:
        pass

    @abstractmethod
    async def get_filter_sales_order(self, filter_type: str):
        pass

    @abstractmethod
    async def update_sales_order(self, entity: SalesOrder) -> SalesOrder:
        pass

    @abstractmethod
    async def update_sales_order_status(self, entity: SalesOrder) -> SalesOrder:
        pass