from datetime import date
from pydantic import BaseModel, ConfigDict

class SchoolClassBaseDTO(BaseModel):
    className: str
    classCode: str
    classOrder: int
    status: str = "Active"


class SchoolClassCreateDTO(SchoolClassBaseDTO):
    pass


class SchoolClassUpdateDTO(BaseModel):
    className: str | None = None
    classCode: str | None = None
    classOrder: int | None = None
    status: str | None = None


class SchoolClassDTO(SchoolClassBaseDTO):
    classID: int

    model_config = ConfigDict(from_attributes=True)