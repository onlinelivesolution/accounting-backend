from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class StudentCreateDTO(BaseModel):

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


class StudentUpdateDTO(BaseModel):

    studentCode: str | None = None
    admissionNo: str | None = None

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

    admissionDate: date | None = None

    status: str | None = None


class StudentDTO(BaseModel):

    studentID: int

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

    status: str

    createdDate: datetime
    updatedDate: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class StudentDropdownDTO(BaseModel):
    studentID: int
    studentCode: str
    studentName: str
    admissionNo: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )