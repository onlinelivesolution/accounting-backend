from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.schemas.student_schema import StudentDTO
from src.schemas.studentguardian_schema import StudentGuardianDTO
from src.schemas.studentenrollment_schema import StudentEnrollmentDTO
from src.schemas.studentpromotion_schema import StudentPromotionDTO

class StudentProfileDTO(BaseModel):
    student: StudentDTO

    guardians: list[StudentGuardianDTO] = []

    currentEnrollment: StudentEnrollmentDTO | None = None

    enrollments: list[StudentEnrollmentDTO] = []

    promotions: list[StudentPromotionDTO] = []

    model_config = ConfigDict(from_attributes=True)