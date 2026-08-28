from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship as orm_relationship,
)

from src.services.database import Base


class StudentMark(Base):
    __tablename__ = "StudentMark"

    studentMarkID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    examSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ExamSubject.examSubjectID"), nullable=False
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    enrollmentID: Mapped[int] = mapped_column(
        ForeignKey("StudentEnrollment.enrollmentID"), nullable=False
    )

    marks: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    grade: Mapped[str | None] = mapped_column(String(10), nullable=True)

    gradePoint: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)

    isAbsent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    
