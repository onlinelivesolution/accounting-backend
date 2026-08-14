from datetime import date
from pydantic import BaseModel, ConfigDict

class StudentGuardianBaseDTO(BaseModel):
    guardianName: str
    relationship: str
    phone: str | None = None
    alternatePhone: str | None = None
    email: str | None = None
    occupation: str | None = None
    address: str | None = None
    isPrimary: bool = False


class StudentGuardianCreateDTO(StudentGuardianBaseDTO):
    pass


class StudentGuardianDTO(StudentGuardianBaseDTO):
    guardianID: int
    studentID: int

    model_config = ConfigDict(from_attributes=True)