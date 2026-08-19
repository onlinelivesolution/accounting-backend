from abc import ABC, abstractmethod
from typing import List, Optional
from src.schemas.academicyear_schema import AcademicYearDTO
from src.models.academicyear import AcademicYear


class IAcademicYearRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[AcademicYear]:
        pass

    @abstractmethod
    async def get_by_id(self, academic_year_id: int) -> Optional[AcademicYear]:
        pass

    @abstractmethod
    async def get_by_year(self, year: int) -> AcademicYear | None:
        pass

    @abstractmethod
    async def get_current(self) -> Optional[AcademicYear]:
        pass

    @abstractmethod
    async def create(self, academic_year: AcademicYear) -> AcademicYear:
        pass

    @abstractmethod
    async def update(self, academic_year: AcademicYear) -> AcademicYear:
        pass

    # @abstractmethod
    # async def deactivate(
    #     self,
    #     academic_year_id: int,
    # ) -> AcademicYearDTO:
    #     pass