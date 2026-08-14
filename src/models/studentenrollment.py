from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class StudentEnrollment(Base):
    __tablename__ = "StudentEnrollment"

    enrollmentID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    academicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"), nullable=False
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"), nullable=False
    )

    sectionID: Mapped[int | None] = mapped_column(
        ForeignKey("Section.sectionID"), nullable=True
    )

    rollNo: Mapped[int | None] = mapped_column(Integer, nullable=True)

    enrollmentDate: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    student = relationship("Student", back_populates="enrollments")

    academicYear = relationship("AcademicYear")

    schoolClass = relationship("SchoolClass")

    section = relationship("Section", back_populates="enrollments")
