from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.istudent_repository import (
    IStudentRepository,
)


class StudentRepository(GenericRepository[Student], IStudentRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Student, db)

    async def get_all(self) -> List[Student]:

        result = await self.db.execute(
            select(Student)
            .order_by(Student.studentID.desc())
        )

        return list(result.scalars().all())

    async def get_by_id(
        self,
        student_id: int,
    ) -> Student | None:

        result = await self.db.execute(
            select(Student).where(
                Student.studentID == student_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_student_code(
        self,
        student_code: str,
    ) -> Student | None:

        result = await self.db.execute(
            select(Student).where(
                Student.studentCode == student_code
            )
        )

        return result.scalar_one_or_none()

    async def get_by_admission_no(
        self,
        admission_no: str,
    ) -> Student | None:

        result = await self.db.execute(
            select(Student).where(
                Student.admissionNo == admission_no
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        student: Student,
    ) -> Student:

        self.db.add(student)

        await self.db.commit()

        await self.db.refresh(student)

        return student

    async def update(
        self,
        student: Student,
    ) -> Student:

        await self.db.commit()

        await self.db.refresh(student)

        return student