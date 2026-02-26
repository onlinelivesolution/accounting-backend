from src.services.interfaces.isalesorder_service import ISalesOrderService
from src.repositories.interfaces.isalesorder_repository import ISalesOrderRepository
from src.models.salesorder import SalesOrder
from src.models.salesorderdetail import SalesOrderDetail
from src.schemas.salesorder_schema import SalesOrderCreateRequest
from datetime import datetime


class SalesOrderService(ISalesOrderService):

    def __init__(self, repository: ISalesOrderRepository):
        self.repository = repository

    async def create_sales_order(self, request: SalesOrderCreateRequest) -> SalesOrder:
        salesorder = SalesOrder(
            salesOrderNo=request.salesOrderNo,
            salesOrderDate=request.salesOrderDate,
            customerID=request.customerID,
            exclusiveAmount=request.exclusiveAmount,
            discountAmount=request.discountAmount,
            vatAmount=request.vatAmount,
            totalAmount=request.totalAmount,
            createdBy=request.createdBy,
            createdDate=datetime.utcnow(),
            status="Draft",
            remarks=request.remarks,
            items=[]
        )

        for item in request.items:
            salesorder.items.append(
                SalesOrderDetail(
                    itemID=item.itemID,
                    itemDescription=item.itemDescription,
                    quantity=item.quantity,
                    unitPrice=item.unitPrice,
                    discountAmount=item.discountAmount,
                    lineTotal=item.lineTotal
                )
            )

        return await self.repository.create(salesorder)

    async def get_sales_order(self, salesOrderID: int):
        return await self.repository.get_by_id(salesOrderID)

    async def list_sales_order(self):
        return await self.repository.get_all()
    
    async def get_next_salesorder_no(self) -> str:
        return await self.repository.get_next_salesorder_no()
    
    async def load_sales_order_table(self):
        quotations = await self.repository.load_sales_order_table()

        return [
            {
                "salesOrderID": so.salesOrderID,
                "salesOrderNo": so.salesOrderNo,
                "salesOrderDate": so.salesOrderDate,
                "totalAmount": so.totalAmount,
                "customerID": so.customerID,
                "status": so.status,
                "customerName": so.customer.customerName if so.customer else None
            }
            for so in quotations
        ]
    
    
    async def get_filter_sales_order(
        self,
        filter_type: str,
        salesorder_no: str | None,
        page: int,
        page_size: int
    ):
        return await self.repository.get_filter_sales_order(
            filter_type,
            salesorder_no,
            page,
            page_size
        )