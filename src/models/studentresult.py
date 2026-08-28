from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class StudentResult(Base):
    __tablename__ = "StudentResult"

    resultID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    examID: Mapped[int] = mapped_column(ForeignKey("Exam.examID"), nullable=False)

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    enrollmentID: Mapped[int] = mapped_column(
        ForeignKey("StudentEnrollment.enrollmentID"), nullable=False
    )

    totalMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )

    obtainedMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )

    percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=0
    )

    grade: Mapped[str | None] = mapped_column(String(10), nullable=True)

    gradePoint: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)

    position: Mapped[int | None] = mapped_column(Integer, nullable=True)

    passFail: Mapped[str] = mapped_column(String(20), nullable=False)

    resultStatus: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Draft"
    )

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    examID: Mapped[int] = mapped_column(ForeignKey("Exam.examID"), nullable=False)


  
