from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.examination import Examination


class IExaminationRepository(ABC):

    @abstractmethod
    async def create(
        self,
        examination: Examination
    ) -> Examination:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        examID: int
    ) -> Optional[Examination]:
        pass

    @abstractmethod
    async def get_all(
        self
    ) -> List[Examination]:
        pass

    @abstractmethod
    async def get_by_academic_year(
        self,
        academicYearID: int
    ) -> List[Examination]:
        pass

    @abstractmethod
    async def exists_by_name_and_year(
        self,
        academicYearID: int,
        examName: str,
        exclude_examID: Optional[int] = None
    ) -> bool:
        pass

    @abstractmethod
    async def update(
        self,
        examination: Examination
    ) -> Examination:
        pass

    @abstractmethod
    async def deactivate(
        self,
        examID: int
    ) -> bool:
        pass