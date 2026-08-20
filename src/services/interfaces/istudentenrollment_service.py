from abc import ABC, abstractmethod
from typing import List

from src.schemas.studentenrollment_schema import (
    StudentEnrollmentCreateDTO,
    StudentEnrollmentDTO,
    StudentEnrollmentUpdateDTO,
)


class IStudentEnrollmentService(ABC):

    @abstractmethod
    async def create(
        self,
        data: StudentEnrollmentCreateDTO,
    ) -> StudentEnrollmentDTO:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        enrollment_id: int,
    ) -> StudentEnrollmentDTO:
        pass

    @abstractmethod
    async def get_all(
        self,
    ) -> List[StudentEnrollmentDTO]:
        pass

    @abstractmethod
    async def get_by_student(
        self,
        student_id: int,
    ) -> List[StudentEnrollmentDTO]:
        pass

    @abstractmethod
    async def update(
        self,
        enrollment_id: int,
        data: StudentEnrollmentUpdateDTO,
    ) -> StudentEnrollmentDTO:
        pass

    @abstractmethod
    async def deactivate(
        self,
        enrollment_id: int,
    ) -> StudentEnrollmentDTO:
        pass
