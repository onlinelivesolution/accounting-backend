from abc import ABC, abstractmethod
from typing import List

from src.models.student import Student


class IStudentRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[Student]:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        student_id: int,
    ) -> Student | None:
        pass

    @abstractmethod
    async def get_by_student_code(
        self,
        student_code: str,
    ) -> Student | None:
        pass

    @abstractmethod
    async def get_by_admission_no(
        self,
        admission_no: str,
    ) -> Student | None:
        pass

    @abstractmethod
    async def create(
        self,
        student: Student,
    ) -> Student:
        pass

    @abstractmethod
    async def update(
        self,
        student: Student,
    ) -> Student:
        pass
    
    @abstractmethod
    async def get_next_student_id(
        self,
    ) -> int:
        pass
    
    @abstractmethod
    async def get_dropdown_students(
        self,
    ) -> List[Student]:
        pass
