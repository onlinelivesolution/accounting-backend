from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.services.interfaces.icustomerreceipt_service import ICustomerReceiptService
from src.repositories.interfaces.icustomerreceipt_repository import ICustomerReceiptRepository
from src.models.customerreceipt_model import CustomerReceipt, CustomerReceiptDetail


class CustomerReceiptService(ICustomerReceiptService):

    def __init__(self, repository: ICustomerReceiptRepository, db: AsyncSession):
        self.repository = repository
        self.db = db

    # ✅ Load invoices (with due calculation)
    async def get_customer_invoices(self, customer_id: int):
        invoices = await self.repository.get_customer_invoices(customer_id)

        response = []
        for inv in invoices:
            paid = await self.repository.get_total_paid_amount(inv.salesInvoiceID)
            due = float(inv.totalAmount) - paid

            response.append({
                "salesInvoiceID": inv.salesInvoiceID,
                "salesInvoiceNo": inv.salesInvoiceNo,
                "SalesInvoiceDate": inv.salesInvoiceDate,
                "totalAmount": float(inv.totalAmount),
                "dueAmount": due,
                "receiveAmount": 0,
                "discountAmount": 0
            })

        return response
    
    

    async def create_customer_receipt(self, request):

        async with self.db.begin():

            # ✅ Calculate allocated from request
            allocated_amount = sum(d.paidAmount for d in request.details) if request.details else 0

            # ✅ Calculate unallocated
            unallocated_amount = request.totalAmount - allocated_amount

            # 🔴 Validation
            if allocated_amount > request.totalAmount:
                raise HTTPException(
                    status_code=400,
                    detail="Allocated amount cannot exceed total amount"
                )

            # ✅ Create master
            receipt = CustomerReceipt(
                receiptNo=request.receiptNo,
                receiptDate=request.receiptDate,
                customerID=request.customerID,
                totalAmount=request.totalAmount,
                allocatedAmount=allocated_amount,
                unallocatedAmount=unallocated_amount,
                status=request.status
            )

            await self.repository.create_customer_receipt(receipt)

            # ✅ If no details → fully unallocated (Flow A)
            if not request.details:
                return receipt

            # ✅ If details exist → allocate (Flow B)
            for d in request.details:

                paid_so_far = await self.repository.get_total_paid_amount(d.salesInvoiceID)
                invoice = await self.repository.get_invoice_by_id(d.salesInvoiceID)

                due = float(invoice.totalAmount) - paid_so_far

                if d.paidAmount > due:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Receive amount exceeds due for invoice {invoice.salesInvoiceNo}"
                    )

                detail = CustomerReceiptDetail(
                    customerReceiptID=receipt.customerReceiptID,
                    salesInvoiceID=d.salesInvoiceID,
                    paidAmount=d.paidAmount,
                    narration=d.narration
                )

                self.db.add(detail)

                # ✅ Update payment status
                total_paid = paid_so_far + d.paidAmount

                if total_paid >= float(invoice.totalAmount):
                    invoice.paymentStatus = "PAID"
                elif total_paid > 0:
                    invoice.paymentStatus = "PARTIAL"

            return receipt

    # ✅ Create receipt + business rules
    # async def create_customer_receipt(self, request):
    #     async with self.db.begin():

    #         receipt = CustomerReceipt(
    #             receiptNo=request.receiptNo,
    #             receiptDate=request.receiptDate,
    #             customerID=request.customerID,
    #             totalAmount=request.totalAmount,
    #             status=request.status
    #         )

    #         await self.repository.create_customer_receipt(receipt)

    #         for d in request.details:

    #             # 🔴 Business validation
    #             paid_so_far = await self.repository.get_total_paid_amount(d.salesInvoiceID)
    #             invoice = await self.repository.get_invoice_by_id(d.salesInvoiceID)

    #             due = float(invoice.totalAmount) - paid_so_far

    #             if d.paidAmount > due:
    #                 raise Exception(f"Receive amount exceeds due for invoice {invoice.salesInvoiceNo}")

    #             detail = CustomerReceiptDetail(
    #                 customerReceiptID=receipt.customerReceiptID,
    #                 salesInvoiceID=d.salesInvoiceID,
    #                 paidAmount=d.paidAmount,
    #                 narration=d.narration
    #             )

    #             self.db.add(detail)

    #             # ✅ Update payment status
    #             total_paid = paid_so_far + d.paidAmount

    #             if total_paid >= float(invoice.totalAmount):
    #                 invoice.paymentStatus = "PAID"
    #             elif total_paid > 0:
    #                 invoice.paymentStatus = "PARTIAL"

    #         return receipt
        
    async def get_customer_balance(self, customer_id: int):

        invoices = await self.repository.get_customer_invoices(customer_id)

        total_due = 0

        for inv in invoices:
            paid = await self.repository.get_total_paid_amount(inv.salesInvoiceID)
            due = float(inv.totalAmount) - paid
            total_due += due

        return {
            "customerID": customer_id,
            "totalDue": total_due
        }