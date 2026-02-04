from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Optional
from sqlalchemy.orm import selectinload
from common.enum.commenum import DefaultItemStatus, MonthName
from src.models.salary import Salary
from src.models.salarydetail import SalaryDetail
from src.schemas.salaryschema import SalaryRead, SalaryDetailRead
from src.repositories.interfaces.isalarydetail_repository import ISalaryDetailRepository

from common.generic.generic_repository import GenericRepository

class SalaryDetailRepository(GenericRepository[Salary], ISalaryDetailRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Salary, db)

    async def get_salary_with_details(self, year: str, month: int, status: int) -> List[Salary]:
        stmt = (
            select(Salary)
            .options(joinedload(Salary.details).joinedload(SalaryDetail.employee))
            .where(Salary.year == year, Salary.month == month, Salary.status == status)
        )
        result = await self.db.execute(stmt)
        return result.scalars().unique().all()
    
    async def approve_salary_details(self, detail_ids: List[int]) -> None:
        if not detail_ids:
            return

        # ✅ Update SalaryDetail statuses
        await self.db.execute(
            update(SalaryDetail)
            .where(SalaryDetail.salaryDetailID.in_(detail_ids))
            .values(status=2)  # 2 = Approved
        )

        # ✅ Get affected SalaryIDs
        result = await self.db.execute(
            select(SalaryDetail.salaryID).where(SalaryDetail.salaryDetailID.in_(detail_ids))
        )
        salary_ids = set([row[0] for row in result.all()])

        # ✅ Update parent Salary if all details approved
        for sid in salary_ids:
            detail_statuses = await self.db.execute(
                select(SalaryDetail.status).where(SalaryDetail.salaryID == sid)
            )
            statuses = [row[0] for row in detail_statuses.all()]

            if statuses and all(s == 2 for s in statuses):
                await self.db.execute(
                    update(Salary).where(Salary.salaryID == sid).values(status=2)
                )

        await self.db.commit()
