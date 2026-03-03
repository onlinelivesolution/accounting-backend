from abc import ABC, abstractmethod
from src.schemas.salesorder_schema import SalesOrderCreateRequest, SalesOrderUpdateRequest
from src.models.salesorder import SalesOrder
from typing import List, Optional
from common.enum.commenum import QuotationFilter


class ISalesOrderService(ABC):

    @abstractmethod
    async def create_sales_order(self, request: SalesOrderCreateRequest) -> SalesOrder:
        pass

    @abstractmethod
    async def get_sales_order(self, salesorder_id: int) -> SalesOrder | None:
        pass

    @abstractmethod
    async def list_sales_order(self) -> list[SalesOrder]:
        pass
    
    @abstractmethod
    async def get_next_salesorder_no(self) -> str:
        pass

    @abstractmethod
    async def load_sales_order_table(self) -> list[SalesOrder]:
        pass
    
    @abstractmethod
    async def get_filter_sales_order(self, filter_type: str):
        pass

    @abstractmethod
    async def update_sales_order(self, salesorder_id: int, request: SalesOrderUpdateRequest):
        pass