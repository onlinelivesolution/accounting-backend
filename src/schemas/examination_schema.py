from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExaminationCreateDTO(BaseModel):
    academicYearID: int
    examName: str
    examTypeID: int
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    status: str = "Active"


class ExaminationUpdateDTO(BaseModel):
    academicYearID: Optional[int] = None
    examName: Optional[str] = None
    examTypeID: Optional[int] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    status: Optional[str] = None


class ExaminationDTO(BaseModel):
    examID: int
    academicYearID: int
    examName: str
    examTypeID: int
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    status: str
    createdDate: datetime
    updatedDate: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)