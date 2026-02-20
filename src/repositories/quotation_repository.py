from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from sqlalchemy.orm import selectinload
from src.models.quotation import Quotation
from common.enum.commenum import QuotationFilter
from sqlalchemy import select, extract
from datetime import date
from src.repositories.interfaces.iquotation_repository import IQuotationRepository


class QuotationRepository(IQuotationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, quotation: Quotation) -> Quotation:
        self.db.add(quotation)
        await self.db.commit()

        # 🔥 IMPORTANT: reload with relationships
        stmt = (
            select(Quotation)
            .options(selectinload(Quotation.items))
            .where(Quotation.quotationID == quotation.quotationID)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_by_id(self, quotationID: int) -> Quotation | None:
        stmt = (
            select(Quotation)
            .options(selectinload(Quotation.items))
            .where(Quotation.quotationID == quotationID)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Quotation]:
        result = await self.db.execute(select(Quotation))
        return result.scalars().all()
    
   
    async def get_next_quotation_no(self) -> str:
        result = await self.db.execute(
            select(func.max(Quotation.quotationNo))
        )
        last_no = result.scalar()

        if not last_no:
            return "QTO0000001"

        number = int(last_no.replace("QTO", "")) + 1
        return f"QTO{number:07d}"
    
    async def get_quotation_table(self):
        stmt = (
            select(Quotation)
            .options(selectinload(Quotation.customer))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_quotations(self, filter: QuotationFilter, search: Optional[str]
    ):
        today = date.today()
        stmt = select(Quotation)

        # 🔎 SEARCH BY QUOTATION NO
        if search:
            stmt = stmt.where(
                Quotation.quotationNo.ilike(f"%{search}%")
            )

        # 📌 FILTERS
        if filter == QuotationFilter.TODAY:
            stmt = stmt.where(Quotation.quotationDate == today)

        elif filter == QuotationFilter.THIS_MONTH:
            stmt = stmt.where(
                extract("month", Quotation.quotationDate) == today.month,
                extract("year", Quotation.quotationDate) == today.year
            )

        elif filter == QuotationFilter.EXPIRING_TODAY:
            stmt = stmt.where(Quotation.expireDate == today)

        elif filter == QuotationFilter.EXPIRED:
            stmt = stmt.where(Quotation.expireDate < today)

        elif filter == QuotationFilter.PENDING:
            stmt = stmt.where(Quotation.status == "Pending")

        elif filter == QuotationFilter.INVOICED:
            stmt = stmt.where(Quotation.status == "Invoiced")

        result = await self.db.execute(stmt)
        return result.scalars().all()

