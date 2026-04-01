from src.services.interfaces.isalesinvoice_service import ISalesInvoiceService
from src.repositories.interfaces.isalesinvoice_repository import ISalesInvoiceRepository
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.models.salesinvoice import SalesInvoice
from src.models.salesinvoicedetail import SalesInvoiceDetail
from src.schemas.salesinvoice_schema import SalesInvoiceCreateRequest
from fastapi import HTTPException
from datetime import datetime

class SalesInvoiceService(ISalesInvoiceService):

    # def __init__(self, repository: ISalesInvoiceRepository):
    #     self.repository = repository
    
    def __init__(
        self,
        repository: ISalesInvoiceRepository,
        journal_service: ICommonJournalService   # ✅ ADD THIS
    ):
        self.repository = repository
        self.journal_service = journal_service
    
    async def create_sales_invoice(self, request: SalesInvoiceCreateRequest) -> SalesInvoice:
        salesinvoice = SalesInvoice(
            salesOrderID=request.salesOrderID,
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
    
    async def update_sales_invoice(self, salesinvoice_id: int, request):
        """
        Business logic:
        1. Check if sales invoice exists
        2. Update sales invoice header
        3. Remove old detail rows
        4. Insert new detail rows
        """

        # 🔹 1. Get existing order
        sales_invoice = await self.repository.get_sales_invoice_by_id(salesinvoice_id)
        if not sales_invoice:
            return None

        # 🔹 2. Update header fields
        sales_invoice.salesInvoiceDate = request.salesOrderDate
        sales_invoice.customerID = request.customerID
        sales_invoice.exclusiveAmount = request.exclusiveAmount
        sales_invoice.discountAmount = request.discountAmount
        sales_invoice.vatAmount = request.vatAmount
        sales_invoice.totalAmount = request.totalAmount

        # 🔹 3. Delete existing details
        await self.repository.db.execute(
            SalesInvoiceDetail.__table__.delete().where(
                SalesInvoiceDetail.salesInvoiceID == salesinvoice_id
            )
        )

        # 🔹 4. Insert new details
        for item in request.items:
            detail = SalesInvoiceDetail(
                salesInvoiceID=salesinvoice_id,
                itemID=item.itemID,
                itemDescription=item.itemDescription,
                quantity=item.quantity,
                unitPrice=item.unitPrice,
                exclusiveAmount=item.exclusiveAmount,
                discountAmount=item.discountAmount,
                vatAmount=item.vatAmount,
                totalAmount=item.totalAmount,
            )
            self.repository.db.add(detail)

        # 🔹 5. Commit once
        await self.repository.db.commit()

        # 🔹 6. Refresh header
        await self.repository.db.refresh(sales_invoice)

        return sales_invoice

    async def get_sales_invoice_by_id(self, salesInvoiceID: int):
        return await self.repository.get_sales_invoice_by_id(salesInvoiceID)
    
    async def list_sales_invoice(self):
        return await self.repository.get_all_sales_invoice()
    
    async def get_all_sales_invoice(self):
        return await self.repository.get_all_sales_invoice()
    
    async def get_next_salesinvoice_no(self) -> str:
        return await self.repository.get_next_salesinvoice_no()
    
    async def load_sales_invoice_table(self):
        salesinvoice = await self.repository.load_sales_invoice_table()

        return [
            {
                "salesInvoiceID": si.salesInvoiceID,
                "salesInvoiceNo": si.salesInvoiceNo,
                "salesInvoiceDate": si.salesInvoiceDate,
                "totalAmount": si.totalAmount,
                "customerID": si.customerID,
                "status": si.status,
                "customerName": si.customer.customerName if si.customer else None
            }
            for si in salesinvoice
        ]
    
    
    async def get_filter_sales_invoice(
        self,
        filter_type: str,
        salesinvoice_no: str | None,
        page: int,
        page_size: int
    ):
        return await self.repository.get_filter_sales_invoice(
            filter_type,
            salesinvoice_no,
            page,
            page_size
        )
    
    async def update_sales_invoice_status(self, salesinvoice_id: int, status: str):

        sales_invoice = await self.repository.get_sales_invoice_by_id(salesinvoice_id)

        if not sales_invoice:
            return None

        sales_invoice.status = status

        await self.repository.update_sales_invoice_status(sales_invoice)

        await self.repository.db.commit()

        return sales_invoice
    
    async def copy_sales_invoice(self, salesinvoice_id: int):

        # 1️⃣ Get existing invoice
        invoice = await self.repository.get_sales_invoice_with_details(salesinvoice_id)

        if not invoice:
            return None
        sales_invoice_no = await self.repository.get_next_salesinvoice_no()
        
        # 2️⃣ Create new invoice header
        new_invoice = SalesInvoice(
            salesInvoiceNo=sales_invoice_no,
            salesInvoiceDate=datetime.utcnow(),
            customerID=invoice.customerID,
            exclusiveAmount=invoice.exclusiveAmount,
            discountAmount=invoice.discountAmount,
            vatAmount=invoice.vatAmount,
            totalAmount=invoice.totalAmount,
            status="Draft",           
            remarks=invoice.remarks, 
            createdBy="admin",
            createdDate=datetime.utcnow()
                       
        )

        await self.repository.create_sales_invoice(new_invoice)

        # 3️⃣ Copy details
        for item in invoice.items:

            new_detail = SalesInvoiceDetail(
                salesInvoiceID=new_invoice.salesInvoiceID,
                itemID=item.itemID,
                itemDescription=item.itemDescription,
                quantity=item.quantity,
                unitPrice=item.unitPrice,
                exclusiveAmount=item.exclusiveAmount,
                discountAmount=item.discountAmount,
                vatAmount=item.vatAmount,
                totalAmount=item.totalAmount
            )

            await self.repository.add_sales_invoice_detail(new_detail)

        # commit from service layer
        await self.repository.db.commit()

        return new_invoice
    
    async def get_sales_order_dropdown(self):
        return await self.repository.get_sales_order_dropdown()
    
    async def get_sales_order_for_sales_invoice(self, salesOrderID: int):
        salesorder = await self.repository.get_sales_order_for_sales_invoice(salesOrderID)

        if not salesorder:
            raise HTTPException(status_code=404, detail="Sales Order not found")

        # 🔹 Map quotation → sales order format
        return {
            "salesOrderID": salesorder.salesOrderID,
            "customerID": salesorder.customerID,
            "exclusiveAmount": float(salesorder.exclusiveAmount),
            "discountAmount": float(salesorder.discountAmount),
            "vatAmount": float(salesorder.vatAmount),
            "totalAmount": float(salesorder.totalAmount),
            "items": [
                {
                    "itemID": d.itemID,
                    "itemDescription": d.itemDescription,
                    "quantity": float(d.quantity),
                    "unitPrice": float(d.unitPrice),
                    "discountAmount": float(d.discountAmount),
                    "lineTotal": float(d.lineTotal)
                }
                for d in salesorder.items
            ]
        }
    
    async def approve_sales_invoice(self, salesInvoiceID: int):

        invoice = await self.repository.get_sales_invoice_by_id(salesInvoiceID)

        if not invoice:
            raise Exception("Invoice not found")

        if invoice.status == "APPROVED":
            raise Exception("Already approved")

        # ✅ Journal Posting
        await self.journal_service.post_sales_invoice_journal(invoice)

        # ✅ Update status
        invoice.status = "APPROVED"

        await self.repository.update(invoice)

        return {"message": "Approved successfully"}
    
    async def update(self, invoice: SalesInvoice) -> SalesInvoice:
        return await self.repository.update(invoice)