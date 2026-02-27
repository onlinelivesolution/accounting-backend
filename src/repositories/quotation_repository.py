from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from sqlalchemy.orm import selectinload
from src.models.quotation import Quotation
from src.models.customers import Customer
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
    

    
    async def get_quotations(
        self,
        filter_type: str,
        quotation_no: Optional[str],
        page: int,
        page_size: int
    ):
        stmt = (
            select(Quotation)
            .options(selectinload(Quotation.customer))  # ✅ FIX
        )

        today = date.today()

        # ---------- FILTER ----------
        if filter_type == "TODAY":
            stmt = stmt.where(Quotation.quotationDate == today)

        elif filter_type == "THIS_MONTH":
            stmt = stmt.where(
                func.month(Quotation.quotationDate) == today.month,
                func.year(Quotation.quotationDate) == today.year
            )

        elif filter_type == "EXPIRING_TODAY":
            stmt = stmt.where(Quotation.expireDate == today)

        elif filter_type == "EXPIRED":
            stmt = stmt.where(Quotation.expireDate < today)

        elif filter_type == "PENDING":
            stmt = stmt.where(Quotation.status == "PENDING")

        elif filter_type == "INVOICED":
            stmt = stmt.where(Quotation.status == "INVOICED")

        # ---------- SEARCH ----------
        if quotation_no:
            stmt = stmt.where(
                Quotation.quotationNo.ilike(f"%{quotation_no}%")
            )

        # ---------- ORDER (MANDATORY FOR MSSQL) ----------
        stmt = stmt.order_by(Quotation.quotationID.desc())

        # ---------- COUNT ----------
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar()

        # ---------- PAGINATION ----------
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        quotations = result.scalars().all()

        return {
            "items": [
                {
                    "quotationID": q.quotationID,
                    "quotationNo": q.quotationNo,
                    "quotationDate": q.quotationDate,
                    "totalAmount": q.totalAmount,
                    "status": q.status,
                    "customerName": q.customer.customerName if q.customer else None
                }
                for q in quotations
            ],
            "total": total
        }
        
    async def get_quotation_dropdown(self):
        stmt = (
            select(
                Quotation.quotationID,
                Quotation.quotationNo
            )
            .where(Quotation.status == "Draft")   # important
            .order_by(Quotation.quotationNo)
        )

        result = await self.db.execute(stmt)
        return result.all()
    
    async def get_quotation_for_sales_order(self, quotationID: int):
        stmt = (
            select(Quotation)
            .options(selectinload(Quotation.items))  # ✅ eager load
            .where(
                Quotation.quotationID == quotationID,
                Quotation.status == "Draft"
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()