from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.studentenrollment import StudentEnrollment
from src.repositories.interfaces.istudentenrollment_repository import (
    IStudentEnrollmentRepository,
)


class StudentEnrollmentRepository(IStudentEnrollmentRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        enrollment: StudentEnrollment,
    ) -> StudentEnrollment:

        self.db.add(enrollment)

        await self.db.commit()

        await self.db.refresh(enrollment)

        return enrollment

    async def get_by_id(
        self,
        enrollment_id: int,
    ) -> Optional[StudentEnrollment]:

        result = await self.db.execute(
            select(StudentEnrollment).where(
                StudentEnrollment.enrollmentID == enrollment_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_student_and_year(
        self,
        student_id: int,
        academic_year_id: int,
    ) -> Optional[StudentEnrollment]:

        result = await self.db.execute(
            select(StudentEnrollment).where(
                StudentEnrollment.studentID == student_id,
                StudentEnrollment.academicYearID == academic_year_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> List[StudentEnrollment]:

        result = await self.db.execute(
            select(StudentEnrollment).order_by(StudentEnrollment.enrollmentID.desc())
        )

        return list(result.scalars().all())

    async def get_by_student(
        self,
        student_id: int,
    ) -> List[StudentEnrollment]:

        result = await self.db.execute(
            select(StudentEnrollment)
            .where(StudentEnrollment.studentID == student_id)
            .order_by(StudentEnrollment.academicYearID.desc())
        )

        return list(result.scalars().all())

    async def update(
        self,
        enrollment: StudentEnrollment,
    ) -> StudentEnrollment:

        await self.db.commit()

        await self.db.refresh(enrollment)

        return enrollment

    async def deactivate(
        self,
        enrollment: StudentEnrollment,
    ) -> StudentEnrollment:

        enrollment.status = "Inactive"

        await self.db.commit()

        await self.db.refresh(enrollment)

        return enrollment
