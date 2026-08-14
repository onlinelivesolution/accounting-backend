from datetime import date
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class StudentMarkCreateDTO(BaseModel):
    examSubjectID: int
    studentID: int
    enrollmentID: int

    marks: Decimal

    isAbsent: bool = False
    remarks: str | None = None
    
class StudentMarkDTO(StudentMarkCreateDTO):
    studentMarkID: int
    grade: str | None = None
    gradePoint: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)