from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.academicyear import AcademicYear
from src.repositories.interfaces.iacademicyear_repository import (
    IAcademicYearRepository,
)


class AcademicYearRepository(IAcademicYearRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[AcademicYear]:

        result = await self.db.execute(
            select(AcademicYear).order_by(AcademicYear.year.desc())
        )

        return list(result.scalars().all())

    async def get_by_id(self, academic_year_id: int) -> Optional[AcademicYear]:

        result = await self.db.execute(
            select(AcademicYear).where(AcademicYear.academicYearID == academic_year_id)
        )

        return result.scalar_one_or_none()

    async def get_by_year(self, year: int) -> Optional[AcademicYear]:

        result = await self.db.execute(
            select(AcademicYear).where(AcademicYear.year == year)
        )

        return result.scalar_one_or_none()

    async def get_current(self) -> Optional[AcademicYear]:

        result = await self.db.execute(
            select(AcademicYear).where(AcademicYear.isCurrent == True)
        )

        return result.scalar_one_or_none()

    async def create(self, academic_year: AcademicYear) -> AcademicYear:

        self.db.add(academic_year)

        await self.db.commit()

        await self.db.refresh(academic_year)

        return academic_year

    async def update(self, academic_year: AcademicYear) -> AcademicYear:

        await self.db.commit()

        await self.db.refresh(academic_year)

        return academic_year

    async def delete(self, academic_year_id: int) -> bool:

        academic_year = await self.get_by_id(academic_year_id)

        if academic_year is None:
            return False

        await self.db.delete(academic_year)

        await self.db.commit()

        return True
