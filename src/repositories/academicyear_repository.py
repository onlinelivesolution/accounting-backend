from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from common.generic.generic_repository import GenericRepository
from src.models.academicyear import AcademicYear
from src.repositories.interfaces.iacademicyear_repository import (
    IAcademicYearRepository,
)

class AcademicYearRepository(GenericRepository[AcademicYear], IAcademicYearRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(AcademicYear, db)

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

    async def get_by_year(
        self,
        year: int,
    ) -> Optional[AcademicYear]:

        result = await self.db.execute(
            select(AcademicYear).where(
                AcademicYear.year == year
            )
        )

        return result.scalar_one_or_none()

    async def get_current(
        self,
    ) -> AcademicYear | None:

        result = await self.db.execute(
            select(AcademicYear).where(
                AcademicYear.isCurrent == True
            )
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

    # async def update(self, entity):
    #     merged_entity = await self.db.merge(entity)

    #     await self.db.commit()
    #     await self.db.refresh(merged_entity)

    #     return merged_entity
    
    async def get_dropdown_academic_years(
        self,
    ) -> list[AcademicYear]:

        result = await self.db.execute(
            select(AcademicYear)
            .where(
                AcademicYear.status == "Active"
            )
            .order_by(
                AcademicYear.year.desc()
            )
        )

        return list(result.scalars().all())