from abc import ABC, abstractmethod
from typing import List

from src.schemas.academicyear_schema import (
    AcademicYearCreateDTO,
    AcademicYearDTO,
    AcademicYearUpdateDTO,
)


class IAcademicYearService(ABC):

    @abstractmethod
    async def get_all(self) -> List[AcademicYearDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, academic_year_id: int) -> AcademicYearDTO:
        pass

    @abstractmethod
    async def get_current(self) -> AcademicYearDTO:
        pass

    @abstractmethod
    async def create(self, data: AcademicYearCreateDTO) -> AcademicYearDTO:
        pass

    @abstractmethod
    async def update(
        self, academic_year_id: int, data: AcademicYearUpdateDTO
    ) -> AcademicYearDTO:
        pass

    @abstractmethod
    async def delete(self, academic_year_id: int) -> bool:
        pass

    @abstractmethod
    async def set_current(self, academic_year_id: int) -> AcademicYearDTO:
        pass
