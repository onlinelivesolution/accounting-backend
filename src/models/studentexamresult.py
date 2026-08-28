from datetime import datetime
from decimal import Decimal
# from src.models.examination import Examination
# from src.models.student import Student
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class StudentExamResult(Base):
    __tablename__ = "StudentExamResult"

    resultID: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    examID: Mapped[int] = mapped_column(
        ForeignKey("Examination.examID"),
        nullable=False
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"),
        nullable=False
    )

    totalMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    fullMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    percentage: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        nullable=False,
        default=0
    )

    gpa: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 2),
        nullable=True
    )

    grade: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    position: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    totalSubjects: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    passedSubjects: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    failedSubjects: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    isPassed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    isPublished: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


    
  