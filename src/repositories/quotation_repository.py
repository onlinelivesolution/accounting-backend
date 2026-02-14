from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from src.models.quotation import Quotation
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

