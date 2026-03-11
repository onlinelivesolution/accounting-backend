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
            expireDate=request.expireDate,
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
                    exclusiveAmount=item.exclusiveAmount,
                    discountAmount=item.discountAmount,
                    vatAmount=item.vatAmount,
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
    
    async def update_sales_order(self, salesorder_id: int, request):
        """
        Business logic:
        1. Check if sales order exists
        2. Update sales order header
        3. Remove old detail rows
        4. Insert new detail rows
        """

        # 🔹 1. Get existing order
        sales_order = await self.repository.get_by_id(salesorder_id)
        if not sales_order:
            return None

        # 🔹 2. Update header fields
        sales_order.salesOrderDate = request.salesOrderDate
        sales_order.expireDate = request.expireDate
        sales_order.customerID = request.customerID
        sales_order.exclusiveAmount = request.exclusiveAmount
        sales_order.discountAmount = request.discountAmount
        sales_order.vatAmount = request.vatAmount
        sales_order.totalAmount = request.totalAmount

        # 🔹 3. Delete existing details
        await self.repository.db.execute(
            SalesOrderDetail.__table__.delete().where(
                SalesOrderDetail.salesOrderID == salesorder_id
            )
        )

        # 🔹 4. Insert new details
        for item in request.items:
            detail = SalesOrderDetail(
                salesOrderID=salesorder_id,
                itemID=item.itemID,
                itemDescription=item.itemDescription,
                quantity=item.quantity,
                unitPrice=item.unitPrice,
                exclusiveAmount=item.exclusiveAmount,
                discountAmount=item.discountAmount,
                vatAmount=item.vatAmount,
                lineTotal=item.lineTotal,
            )
            self.repository.db.add(detail)

        # 🔹 5. Commit once
        await self.repository.db.commit()

        # 🔹 6. Refresh header
        await self.repository.db.refresh(sales_order)

        return sales_order
    
    async def update_sales_order_status(self, salesorder_id: int, status: str):

        sales_order = await self.repository.get_by_id(salesorder_id)

        if not sales_order:
            return None

        sales_order.status = status

        await self.repository.update_sales_order_status(sales_order)

        await self.repository.db.commit()

        return sales_order
    
    
    async def copy_sales_order(self, salesorder_id: int):

        # 1️⃣ Get existing order
        order = await self.repository.get_sales_order_with_details(salesorder_id)

        if not order:
            return None
        sales_order_no = await self.repository.get_next_salesorder_no()
        
        # 2️⃣ Create new order header
        new_order = SalesOrder(
            salesOrderNo=sales_order_no,
            salesOrderDate=datetime.utcnow(),
            customerID=order.customerID,
            exclusiveAmount=order.exclusiveAmount,
            discountAmount=order.discountAmount,
            vatAmount=order.vatAmount,
            totalAmount=order.totalAmount,
            status="Draft",
            expireDate=order.expireDate,            
            remarks=order.remarks, 
            createdBy="admin",
            createdDate=datetime.utcnow()
                       
        )

        await self.repository.add_sales_order(new_order)

        # 3️⃣ Copy details
        for item in order.items:

            new_detail = SalesOrderDetail(
                salesOrderID=new_order.salesOrderID,
                itemID=item.itemID,
                itemDescription=item.itemDescription,
                quantity=item.quantity,
                unitPrice=item.unitPrice,
                exclusiveAmount=item.exclusiveAmount,
                discountAmount=item.discountAmount,
                vatAmount=item.vatAmount,
                lineTotal=item.lineTotal
            )

            await self.repository.add_sales_order_detail(new_detail)

        # commit from service layer
        await self.repository.db.commit()

        return new_order