from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date
from src.models.salesinvoice import SalesInvoice
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

        stmt = (
            select(salesinvoice)
            .options(selectinload(salesinvoice.items))
            .where(salesinvoice.salesInvoiceID == salesinvoice.salesInvoiceID)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
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
    
    async def get_next_salesinvoice_no(self) -> str:
        result = await self.db.execute(
            select(func.max(SalesInvoice.salesInvoiceNo))
        )
        last_no = result.scalar()

        if not last_no:
            return "SIN0000001"

        number = int(last_no.replace("SIN", "")) + 1
        return f"SOR{number:07d}"