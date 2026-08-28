from datetime import date, datetime
from src.models.academicyear import AcademicYear
from src.models.examschedule import ExamSchedule
from src.models.examsubject import ExamSubject
from src.models.studentexamresult import StudentExamResult
from src.models.studentexammark import StudentExamMark
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class Examination(Base):
    __tablename__ = "Exam"

    examID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    academicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"),
        nullable=False
    )

    examName: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    examType: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    startDate: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    endDate: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    createdDate: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    updatedDate: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # -----------------------------------------
    # Relationships
    # -----------------------------------------

    academicYear: Mapped["AcademicYear"] = relationship(
        "AcademicYear"
    )

    examSubjects: Mapped[list["ExamSubject"]] = relationship(
        "ExamSubject",
        back_populates="examination"
    )

    examSchedules: Mapped[list["ExamSchedule"]] = relationship(
        "ExamSchedule",
        back_populates="examination"
    )

    studentMarks: Mapped[list["StudentExamMark"]] = relationship(
        "StudentExamMark",
        back_populates="examination"
    )

    studentResults: Mapped[list["StudentExamResult"]] = relationship(
        "StudentExamResult",
        back_populates="examination"
    )