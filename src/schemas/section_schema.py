from datetime import date
from pydantic import BaseModel, ConfigDict

class SectionBaseDTO(BaseModel):
    classID: int
    sectionName: str
    sectionCode: str
    capacity: int | None = None
    status: str = "Active"


class SectionCreateDTO(SectionBaseDTO):
    pass


class SectionUpdateDTO(BaseModel):
    sectionName: str | None = None
    sectionCode: str | None = None
    capacity: int | None = None
    status: str | None = None


class SectionDTO(SectionBaseDTO):
    sectionID: int

    model_config = ConfigDict(from_attributes=True)