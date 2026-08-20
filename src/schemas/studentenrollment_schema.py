from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentEnrollmentCreateDTO(BaseModel):

    studentID: int
    academicYearID: int
    classID: int

    sectionID: Optional[int] = None
    rollNo: Optional[int] = None

    enrollmentDate: date

    status: str = "Active"

    remarks: Optional[str] = None


class StudentEnrollmentUpdateDTO(BaseModel):

    academicYearID: Optional[int] = None
    classID: Optional[int] = None
    sectionID: Optional[int] = None
    rollNo: Optional[int] = None
    enrollmentDate: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class StudentEnrollmentDTO(BaseModel):

    enrollmentID: int

    studentID: int
    academicYearID: int
    classID: int

    sectionID: Optional[int] = None
    rollNo: Optional[int] = None

    enrollmentDate: date

    status: str

    remarks: Optional[str] = None

    createdDate: datetime
    updatedDate: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
