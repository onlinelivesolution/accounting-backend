from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentExamResultDTO(BaseModel):
    resultID: int

    examID: int
    studentID: int

    totalMarks: Decimal
    fullMarks: Decimal
    percentage: Decimal

    gpa: Optional[Decimal] = None
    grade: Optional[str] = None

    position: Optional[int] = None

    totalSubjects: int
    passedSubjects: int
    failedSubjects: int

    isPassed: bool
    isPublished: bool

    remarks: Optional[str] = None

    status: str

    createdDate: datetime
    updatedDate: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)