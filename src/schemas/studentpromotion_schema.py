from datetime import date
from pydantic import BaseModel, ConfigDict

class StudentPromotionRequestDTO(BaseModel):
    studentID: int

    fromEnrollmentID: int

    toAcademicYearID: int
    toClassID: int
    toSectionID: int | None = None

    resultStatus: str
    promotionStatus: str = "Promoted"

    promotionDate: date

    remarks: str | None = None

class StudentPromotionDTO(BaseModel):
    promotionID: int
    studentID: int

    fromEnrollmentID: int
    toEnrollmentID: int | None = None

    fromAcademicYearID: int
    toAcademicYearID: int

    fromClassID: int
    toClassID: int

    fromSectionID: int | None = None
    toSectionID: int | None = None

    resultStatus: str
    promotionStatus: str
    promotionDate: date
    remarks: str | None = None

    model_config = ConfigDict(from_attributes=True)