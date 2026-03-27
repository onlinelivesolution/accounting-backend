from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date
from src.models.salesinvoice import SalesInvoice
from src.models.salesorder import SalesOrder
from src.models.salesinvoicedetail import SalesInvoiceDetail
from src.repositories.interfaces.isalesinvoice_repository import ISalesInvoiceRepository
from common.generic.generic_repository import GenericRepository

class SalesInvoiceRepository(GenericRepository[SalesInvoice], ISalesInvoiceRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(SalesInvoice, db)
        self.db = db
    
    async def create_sales_invoice(self, salesinvoice: SalesInvoice) -> SalesInvoice:

        self.db.add(salesinvoice)

        await self.db.commit()
        await self.db.refresh(salesinvoice)

        return salesinvoice
    
    async def update_sales_invoice(self, entity: SalesInvoice) -> SalesInvoice:
        """
        Updates only the SalesInvoice header.
        Commit should be controlled by the service layer.
        """

        self.db.add(entity)      # attach entity to session
        await self.db.flush()    # push changes (no commit)

        return entity
    
    async def get_sales_invoice_by_id(self, salesInvoiceID: int) -> SalesInvoice | None:
        stmt = (
            select(SalesInvoice)
            .options(selectinload(SalesInvoice.items))
            .where(SalesInvoice.salesInvoiceID == salesInvoiceID)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_sales_invoice(self) -> list[SalesInvoice]:
        result = await self.db.execute(select(SalesInvoice))
        return result.scalars().all()
    
    async def get_all(self) -> list[SalesInvoice]:
        result = await self.db.execute(select(SalesInvoice))
        return result.scalars().all()
    
    async def get_next_salesinvoice_no(self) -> str:
        result = await self.db.execute(
            select(func.max(SalesInvoice.salesInvoiceNo))
        )
        last_no = result.scalar()

        if not last_no:
            return "SIN0000001"

        number = int(last_no.replace("SIN", "")) + 1
        return f"SIN{number:07d}"
    
    async def load_sales_invoice_table(self):
        stmt = (
            select(SalesInvoice)
            .options(selectinload(SalesInvoice.customer))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()  
    
    async def get_filter_sales_invoice(
        self,
        filter_type: str,
        salesinvoice_no: Optional[str],
        page: int,
        page_size: int
    ):
        stmt = (
            select(SalesInvoice)
            .options(selectinload(SalesInvoice.customer))  # ✅ FIX
        )

        today = date.today()

        # ---------- FILTER ----------
        if filter_type == "TODAY":
            stmt = stmt.where(SalesInvoice.salesInvoiceDate == today)

        elif filter_type == "THIS_MONTH":
            stmt = stmt.where(
                func.month(SalesInvoice.salesInvoiceDate) == today.month,
                func.year(SalesInvoice.salesInvoiceDate) == today.year
            )

        elif filter_type == "EXPIRING_TODAY":
            stmt = stmt.where(SalesInvoice.expireDate == today)

        elif filter_type == "EXPIRED":
            stmt = stmt.where(SalesInvoice.expireDate < today)

        elif filter_type == "PENDING":
            stmt = stmt.where(SalesInvoice.status == "PENDING")

        elif filter_type == "INVOICED":
            stmt = stmt.where(SalesInvoice.status == "INVOICED")

        # ---------- SEARCH ----------
        if salesinvoice_no:
            stmt = stmt.where(
                SalesInvoice.salesInvoiceNo.ilike(f"%{salesinvoice_no}%")
            )

        # ---------- ORDER (MANDATORY FOR MSSQL) ----------
        stmt = stmt.order_by(SalesInvoice.salesInvoiceID.desc())

        # ---------- COUNT ----------
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar()

        # ---------- PAGINATION ----------
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        salesorders = result.scalars().all()

        return {
            "items": [
                {
                    "salesInvoiceID": so.salesInvoiceID,
                    "salesInvoiceNo": so.salesInvoiceNo,
                    "salesInvoiceDate": so.salesInvoiceDate,
                    "totalAmount": so.totalAmount,
                    "status": so.status,
                    "customerName": so.customer.customerName if so.customer else None
                }
                for so in salesorders
            ],
            "total": total
        }
    
    async def update_sales_invoice_status(self, entity: SalesInvoice) -> SalesInvoice:
        """
        Updates only the SalesInvoice status.
        Commit should be controlled by the service layer.
        """

        self.db.add(entity)      # attach entity to session
        await self.db.flush()    # push changes (no commit)

        return entity
    
    async def get_sales_invoice_with_details(self, salesinvoice_id: int):

        query = (
            select(SalesInvoice)
            .options(selectinload(SalesInvoice.items))
            .where(SalesInvoice.salesInvoiceID == salesinvoice_id)
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()


    async def add_sales_invoice(self, entity: SalesInvoice) -> SalesInvoice:

        self.db.add(entity)
        await self.db.flush()

        return entity


    async def add_sales_invoice_detail(self, entity: SalesInvoiceDetail):

        self.db.add(entity)
        await self.db.flush()

        return entity
    
    async def get_sales_order_dropdown(self):
        stmt = (
            select(
                SalesOrder.salesOrderID,
                SalesOrder.salesOrderNo
            )
            .where(SalesOrder.status == "Draft")   # important
            .order_by(SalesOrder.salesOrderNo)
        )

        result = await self.db.execute(stmt)
        return result.all()
    
    async def get_sales_order_for_sales_invoice(self, salesOrderID: int):
        stmt = (
            select(SalesOrder)
            .options(selectinload(SalesOrder.items))  # ✅ eager load
            .where(
                SalesOrder.salesOrderID == salesOrderID,
                SalesOrder.status == "Draft"
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()