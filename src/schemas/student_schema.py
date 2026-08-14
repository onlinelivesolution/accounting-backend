from datetime import date
from pydantic import BaseModel, ConfigDict


class StudentBaseDTO(BaseModel):
    studentCode: str
    admissionNo: str

    firstName: str
    middleName: str | None = None
    lastName: str | None = None

    dateOfBirth: date | None = None
    gender: str | None = None
    bloodGroup: str | None = None

    photoPath: str | None = None

    phone: str | None = None
    email: str | None = None

    address: str | None = None
    city: str | None = None
    postalCode: str | None = None

    admissionDate: date | None = None

    status: str = "Active"


class StudentCreateDTO(StudentBaseDTO):
    pass


class StudentUpdateDTO(BaseModel):
    firstName: str | None = None
    middleName: str | None = None
    lastName: str | None = None

    dateOfBirth: date | None = None
    gender: str | None = None
    bloodGroup: str | None = None

    photoPath: str | None = None

    phone: str | None = None
    email: str | None = None

    address: str | None = None
    city: str | None = None
    postalCode: str | None = None

    status: str | None = None


class StudentDTO(StudentBaseDTO):
    studentID: int

    model_config = ConfigDict(from_attributes=True)