from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.customerreceipt_model import CustomerReceipt, CustomerReceiptDetail
from src.models.salesinvoice import SalesInvoice
from src.repositories.interfaces.icustomerreceipt_repository import ICustomerReceiptRepository


class CustomerReceiptRepository(ICustomerReceiptRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # ✅ TRANSACTION CONTROL
    # =====================================================
    def begin(self):
        return self.db.begin()

    async def flush(self):
        await self.db.flush()

    # =====================================================
    # ✅ GET INVOICES
    # =====================================================
    async def get_customer_invoices(self, customer_id: int):
        query = select(SalesInvoice).where(
            SalesInvoice.customerID == customer_id,
            SalesInvoice.status == "APPROVED",
            SalesInvoice.paymentStatus.in_(["UNPAID", "PARTIAL"])
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    # =====================================================
    # ✅ PAID ONLY
    # =====================================================
    async def get_total_paid_amount(self, salesInvoice_id: int):
        query = select(
            func.coalesce(func.sum(CustomerReceiptDetail.paidAmount), 0)
        ).where(CustomerReceiptDetail.salesInvoiceID == salesInvoice_id)

        result = await self.db.execute(query)
        return float(result.scalar())

    # =====================================================
    # ✅ PAID + DISCOUNT (IMPORTANT)
    # =====================================================
    async def get_total_applied_amount(self, invoice_id: int):
        result = await self.db.execute(
            select(
                func.coalesce(
                    func.sum(
                        CustomerReceiptDetail.paidAmount +
                        CustomerReceiptDetail.discountAmount
                    ),
                    0
                )
            ).where(CustomerReceiptDetail.salesInvoiceID == invoice_id)
        )
        return float(result.scalar())

    # =====================================================
    # ✅ GET SINGLE INVOICE
    # =====================================================
    async def get_invoice_by_id(self, invoice_id: int):
        result = await self.db.execute(
            select(SalesInvoice).where(SalesInvoice.salesInvoiceID == invoice_id)
        )
        return result.scalar_one()

    # =====================================================
    # ✅ MASTER INSERT
    # =====================================================
    async def create_customer_receipt(self, receipt: CustomerReceipt):
        self.db.add(receipt)
        await self.db.flush()  # ✅ ensures receiptID is available
        return receipt

    # =====================================================
    # ✅ DETAIL INSERT
    # =====================================================
    async def add_detail(self, detail: CustomerReceiptDetail):
        self.db.add(detail)

    # =====================================================
    # ✅ OPTIONAL (BULK INSERT - FUTURE OPTIMIZATION)
    # =====================================================
    async def add_details(self, details: list[CustomerReceiptDetail]):
        self.db.add_all(details)