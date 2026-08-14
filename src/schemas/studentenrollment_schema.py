from datetime import date
from pydantic import BaseModel, ConfigDict

class StudentEnrollmentCreateDTO(BaseModel):
    studentID: int
    academicYearID: int
    classID: int
    sectionID: int | None = None
    rollNo: int | None = None
    enrollmentDate: date
    status: str = "Active"
    remarks: str | None = None


class StudentEnrollmentDTO(StudentEnrollmentCreateDTO):
    enrollmentID: int

    model_config = ConfigDict(from_attributes=True)