from abc import ABC, abstractmethod
from typing import List

from src.schemas.student_schema import (
    StudentCreateDTO,
    StudentDTO,
    StudentUpdateDTO,
)


class IStudentService(ABC):

    @abstractmethod
    async def get_all(self) -> List[StudentDTO]:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        student_id: int,
    ) -> StudentDTO:
        pass

    @abstractmethod
    async def create(
        self,
        data: StudentCreateDTO,
    ) -> StudentDTO:
        pass

    @abstractmethod
    async def update(
        self,
        student_id: int,
        data: StudentUpdateDTO,
    ) -> StudentDTO:
        pass

    @abstractmethod
    async def deactivate(
        self,
        student_id: int,
    ) -> StudentDTO:
        pass