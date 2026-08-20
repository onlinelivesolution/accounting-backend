from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.studentenrollment import StudentEnrollment


class IStudentEnrollmentRepository(ABC):

    @abstractmethod
    async def create(
        self,
        enrollment: StudentEnrollment,
    ) -> StudentEnrollment:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        enrollment_id: int,
    ) -> Optional[StudentEnrollment]:
        pass

    @abstractmethod
    async def get_by_student_and_year(
        self,
        student_id: int,
        academic_year_id: int,
    ) -> Optional[StudentEnrollment]:
        pass

    @abstractmethod
    async def get_all(
        self,
    ) -> List[StudentEnrollment]:
        pass

    @abstractmethod
    async def get_by_student(
        self,
        student_id: int,
    ) -> List[StudentEnrollment]:
        pass

    @abstractmethod
    async def update(
        self,
        enrollment: StudentEnrollment,
    ) -> StudentEnrollment:
        pass

    @abstractmethod
    async def deactivate(
        self,
        enrollment: StudentEnrollment,
    ) -> StudentEnrollment:
        pass
