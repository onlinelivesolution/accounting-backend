from datetime import date
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class StudentResultDTO(BaseModel):
    resultID: int

    examID: int
    studentID: int
    enrollmentID: int

    totalMarks: Decimal
    obtainedMarks: Decimal

    percentage: Decimal

    grade: str | None = None
    gradePoint: Decimal | None = None

    position: int | None = None

    passFail: str
    resultStatus: str

    model_config = ConfigDict(from_attributes=True)