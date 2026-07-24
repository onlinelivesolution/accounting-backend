from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy import select, func, desc
from sqlalchemy.orm import joinedload
from typing import Optional
from sqlalchemy.orm import selectinload
from common.enum.commenum import DefaultItemStatus, MonthName
from src.models.salarypayment import SalaryPayment
from src.models.salary import Salary
from src.models.salarydetail import SalaryDetail
from src.schemas.salaryschema import SalaryRead, SalaryDetailRead
from src.repositories.interfaces.isalarypayment_repository import (
    ISalaryPaymentRepository,
)

from common.generic.generic_repository import GenericRepository


class SalaryPaymentRepository(GenericRepository[Salary], ISalaryPaymentRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Salary, db)

    async def get_approve_salary(
        self, year: str, month: int, status: int
    ) -> List[Salary]:
        stmt = (
            select(Salary)
            .options(joinedload(Salary.details).joinedload(SalaryDetail.employee))
            .where(Salary.year == year, Salary.month == month, Salary.status == status)
        )
        result = await self.db.execute(stmt)
        return result.scalars().unique().all()
    

    # create salary payment and salary payment detail
    async def create_salary_payment(
        self, salary_payment: SalaryPayment
    ) -> SalaryPayment:

        self.db.add(salary_payment)

        await self.db.commit()
        await self.db.refresh(salary_payment)

        return salary_payment
    
    async def get_next_salary_payment_no(self) -> str:
        result = await self.db.execute(select(func.max(SalaryPayment.paymentNo)))
        last_no = result.scalar()

        if not last_no:
            return "SPT0000001"

        number = int(last_no.replace("SPT", "")) + 1
        return f"SPT{number:07d}"
