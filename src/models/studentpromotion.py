from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class StudentPromotion(Base):
    __tablename__ = "StudentPromotion"

    promotionID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    fromEnrollmentID: Mapped[int] = mapped_column(
        ForeignKey("StudentEnrollment.enrollmentID"), nullable=False
    )

    toEnrollmentID: Mapped[int | None] = mapped_column(
        ForeignKey("StudentEnrollment.enrollmentID"), nullable=True
    )

    fromAcademicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"), nullable=False
    )

    toAcademicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"), nullable=False
    )

    fromClassID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"), nullable=False
    )

    toClassID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"), nullable=False
    )

    fromSectionID: Mapped[int | None] = mapped_column(
        ForeignKey("Section.sectionID"), nullable=True
    )

    toSectionID: Mapped[int | None] = mapped_column(
        ForeignKey("Section.sectionID"), nullable=True
    )

    resultStatus: Mapped[str] = mapped_column(String(30), nullable=False)

    promotionStatus: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Promoted"
    )

    promotionDate: Mapped[date] = mapped_column(Date, nullable=False)

    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    student = relationship("Student", back_populates="promotions")
