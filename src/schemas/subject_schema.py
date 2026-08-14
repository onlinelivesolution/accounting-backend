from datetime import date
from pydantic import BaseModel, ConfigDict

class SubjectBaseDTO(BaseModel):
    subjectCode: str
    subjectName: str
    description: str | None = None
    status: str = "Active"


class SubjectCreateDTO(SubjectBaseDTO):
    pass


class SubjectUpdateDTO(BaseModel):
    subjectCode: str | None = None
    subjectName: str | None = None
    description: str | None = None
    status: str | None = None


class SubjectDTO(SubjectBaseDTO):
    subjectID: int

    model_config = ConfigDict(from_attributes=True)