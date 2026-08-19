from abc import ABC, abstractmethod
from src.schemas.academicyear_schema import AcademicYearDTO
from src.models.academicyear import AcademicYear
from src.schemas.academicyear_schema import (
    AcademicYearCreateDTO,
    AcademicYearUpdateDTO,
)


class IAcademicYearService(ABC):

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(
        self,
        academic_year_id: int,
    ):
        pass

    @abstractmethod
    async def get_by_year(
        self,
        year: int,
    ) -> AcademicYear | None:
        pass

    @abstractmethod
    async def get_current(self):
        pass

    @abstractmethod
    async def create(
        self, request: AcademicYearCreateDTO
    ) -> AcademicYear:
        pass

    @abstractmethod
    async def update(
        self,
        academic_year_id: int,
        data: AcademicYearUpdateDTO,
    ):
        pass

    @abstractmethod
    async def set_current(
        self,
        academic_year_id: int,
    ):
        pass

    # @abstractmethod
    # async def deactivate(
    #     self,
    #     academic_year_id: int,
    # ) -> AcademicYearDTO:
    #     pass