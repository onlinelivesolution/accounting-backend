from datetime import date
from pydantic import BaseModel, ConfigDict


class AcademicYearBaseDTO(BaseModel):
    year: int
    name: str
    startDate: date
    endDate: date
    isCurrent: bool = False
    status: str = "Active"


class AcademicYearCreateDTO(AcademicYearBaseDTO):
    pass


class AcademicYearUpdateDTO(BaseModel):
    name: str | None = None
    startDate: date | None = None
    endDate: date | None = None
    isCurrent: bool | None = None
    status: str | None = None


class AcademicYearDTO(AcademicYearBaseDTO):
    academicYearID: int

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict


class AcademicYearDropdownDTO(BaseModel):
    academicYearID: int
    year: int
    name: str
    isCurrent: bool
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )