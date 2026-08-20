from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class StudentEnrollment(Base):
    __tablename__ = "StudentEnrollment"

    __table_args__ = (
        UniqueConstraint(
            "studentID",
            "academicYearID",
            name="uq_student_academic_year",
        ),
    )

    enrollmentID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    studentID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Student.studentID"),
        nullable=False,
    )

    academicYearID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("AcademicYear.academicYearID"),
        nullable=False,
    )

    classID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("SchoolClass.classID"),
        nullable=False,
    )

    sectionID: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("Section.sectionID"),
        nullable=True,
    )

    rollNo: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    enrollmentDate: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Active",
    )

    remarks: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    createdDate: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )

    updatedDate: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Relationships

    student = relationship(
        "Student",
        back_populates="enrollments",
    )

    academicYear = relationship(
        "AcademicYear",
        back_populates="enrollments",
    )

    schoolClass = relationship(
        "SchoolClass",
        back_populates="enrollments",
    )

    section = relationship(
        "Section",
        back_populates="enrollments",
    )
