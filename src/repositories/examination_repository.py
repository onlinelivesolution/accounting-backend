from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.examination import Examination
from src.repositories.interfaces.iexamination_repository import (
    IExaminationRepository,
)


class ExaminationRepository(IExaminationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    async def create(
        self,
        examination: Examination
    ) -> Examination:

        self.db.add(examination)

        await self.db.flush()

        await self.db.refresh(examination)

        return examination

    # ---------------------------------------------------------
    # Get By ID
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        examID: int
    ) -> Optional[Examination]:

        result = await self.db.execute(
            select(Examination)
            .where(
                Examination.examID == examID
            )
        )

        return result.scalar_one_or_none()

    # ---------------------------------------------------------
    # Get All
    # ---------------------------------------------------------

    async def get_all(
        self
    ) -> List[Examination]:

        result = await self.db.execute(
            select(Examination)
            .order_by(
                Examination.examID.desc()
            )
        )

        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Get By Academic Year
    # ---------------------------------------------------------

    async def get_by_academic_year(
        self,
        academicYearID: int
    ) -> List[Examination]:

        result = await self.db.execute(
            select(Examination)
            .where(
                Examination.academicYearID == academicYearID
            )
            .order_by(
                Examination.startDate.desc(),
                Examination.examID.desc()
            )
        )

        return list(result.scalars().all())


    async def exists_by_name_and_year(
        self,
        academicYearID: int,
        examName: str,
        exclude_examID: Optional[int] = None
    ) -> bool:

        query = select(Examination.examID).where(
            Examination.academicYearID == academicYearID,
            Examination.examName == examName
        )

        if exclude_examID is not None:
            query = query.where(
                Examination.examID != exclude_examID
            )

        result = await self.db.execute(query)

        return result.scalar_one_or_none() is not None

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    async def update(
        self,
        examination: Examination
    ) -> Examination:

        await self.db.flush()

        await self.db.refresh(examination)

        return examination

    # ---------------------------------------------------------
    # Deactivate
    # ---------------------------------------------------------

    async def deactivate(
        self,
        examID: int
    ) -> bool:

        examination = await self.get_by_id(examID)

        if not examination:
            return False

        examination.status = "Inactive"

        await self.db.flush()

        return True