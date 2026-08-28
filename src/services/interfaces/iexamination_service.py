from abc import ABC, abstractmethod
from typing import List, Optional

from src.schemas.examination_schema import (
    ExaminationCreateDTO,
    ExaminationDTO,
    ExaminationUpdateDTO,
)


class IExaminationService(ABC):

    @abstractmethod
    async def create(
        self,
        data: ExaminationCreateDTO
    ) -> ExaminationDTO:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        examID: int
    ) -> Optional[ExaminationDTO]:
        pass

    @abstractmethod
    async def get_all(
        self
    ) -> List[ExaminationDTO]:
        pass

    @abstractmethod
    async def get_by_academic_year(
        self,
        academicYearID: int
    ) -> List[ExaminationDTO]:
        pass

    @abstractmethod
    async def update(
        self,
        examID: int,
        data: ExaminationUpdateDTO
    ) -> ExaminationDTO:
        pass

    @abstractmethod
    async def deactivate(
        self,
        examID: int
    ) -> bool:
        pass