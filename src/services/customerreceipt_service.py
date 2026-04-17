from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.services.interfaces.icustomerreceipt_service import ICustomerReceiptService
from src.repositories.interfaces.icustomerreceipt_repository import ICustomerReceiptRepository
from src.models.customerreceipt_model import CustomerReceipt, CustomerReceiptDetail
from src.services.interfaces.icommonjournal_service import ICommonJournalService


class CustomerReceiptService(ICustomerReceiptService):
    
    def __init__(
        self,
        repository: ICustomerReceiptRepository,
        common_journal_service: ICommonJournalService   # ✅ ADD
    ):
        self.repository = repository
        self.common_journal_service = common_journal_service

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

        async with self.repository.begin():   # ✅ FIX

            allocated_amount = sum(
                (d.paidAmount + d.discountAmount) for d in request.details
            ) if request.details else 0

            unallocated_amount = request.totalAmount - allocated_amount

            if allocated_amount > request.totalAmount:
                raise HTTPException(
                    status_code=400,
                    detail="Allocated amount cannot exceed total amount"
                )

            receipt = CustomerReceipt(
                receiptNo=request.receiptNo,
                receiptDate=request.receiptDate,
                customerID=request.customerID,
                totalAmount=request.totalAmount,
                allocatedAmount=allocated_amount,
                unallocatedAmount=unallocated_amount,
                status=request.status,
                companyCode=request.companyCode
            )

            await self.repository.create_customer_receipt(receipt)

            # ✅ FIX
            await self.repository.flush()

            # =====================================================
            # ✅ CASE 1: NO DETAILS
            # =====================================================
            if not request.details:
                await self.common_journal_service.post_customer_receipt_journal(receipt, request)
                return receipt

            # =====================================================
            # ✅ CASE 2: WITH DETAILS
            # =====================================================
            for d in request.details:

                applied_so_far = await self.repository.get_total_applied_amount(d.salesInvoiceID)
                invoice = await self.repository.get_invoice_by_id(d.salesInvoiceID)

                due = float(invoice.totalAmount) - applied_so_far

                if (d.paidAmount + d.discountAmount) > due:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Receive + Discount exceeds due for invoice {invoice.salesInvoiceNo}"
                    )

                detail = CustomerReceiptDetail(
                    customerReceiptID=receipt.customerReceiptID,
                    salesInvoiceID=d.salesInvoiceID,
                    paidAmount=d.paidAmount,
                    discountAmount=d.discountAmount,
                    narration=d.narration
                )

                # ✅ FIX
                await self.repository.add_detail(detail)

                total_applied = applied_so_far + d.paidAmount + d.discountAmount

                if total_applied >= float(invoice.totalAmount):
                    invoice.paymentStatus = "PAID"
                elif total_applied > 0:
                    invoice.paymentStatus = "PARTIAL"

            # =====================================================
            # 🔥 POST JOURNAL
            # =====================================================
            await self.common_journal_service.post_customer_receipt_journal(receipt, request)

            return receipt

        
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