from src.services.interfaces.isalesinvoice_service import ISalesInvoiceService
from src.repositories.interfaces.isalesinvoice_repository import ISalesInvoiceRepository
from src.models.salesinvoice import SalesInvoice
from src.models.salesinvoicedetail import SalesInvoiceDetail
from src.schemas.salesinvoice_schema import SalesInvoiceCreateRequest
from datetime import datetime

class SalesInvoiceService(ISalesInvoiceService):

    def __init__(self, repository: ISalesInvoiceRepository):
        self.repository = repository
    
    async def create_sales_invoice(self, request: SalesInvoiceCreateRequest) -> SalesInvoice:
        salesinvoice = SalesInvoice(
            salesInvoiceNo=request.salesInvoiceNo,
            salesInvoiceDate=request.salesInvoiceDate,
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
            salesinvoice.items.append(
                SalesInvoiceDetail(
                    itemID=item.itemID,
                    itemDescription=item.itemDescription,
                    quantity=item.quantity,
                    unitPrice=item.unitPrice,
                    exclusiveAmount=item.exclusiveAmount,
                    discountAmount=item.discountAmount,
                    vatAmount=item.vatAmount,
                    totalAmount=item.totalAmount
                )
            )

        return await self.repository.create_sales_invoice(salesinvoice)

    async def get_sales_invoice_by_id(self, salesInvoiceID: int):
        return await self.repository.get_sales_invoice_by_id(salesInvoiceID)

    async def get_all_sales_invoice(self):
        return await self.repository.get_all_sales_invoice()
    
    async def get_next_salesinvoice_no(self) -> str:
        return await self.repository.get_next_salesinvoice_no()