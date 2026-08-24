from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile

from src.schemas.student_schema import (
    StudentCreateDTO,
    StudentDTO,
    StudentUpdateDTO,
    StudentDropdownDTO,
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
    
    @abstractmethod
    async def get_next_student_code(
        self,
    ) -> str:
        pass
    
    @abstractmethod
    async def get_dropdown_students(
        self,
    ) -> List[StudentDropdownDTO]:
        pass
    
    @abstractmethod
    async def upload_photo(
        self,
        studentID: int,
        file: UploadFile,
    ) -> dict:
        pass