from datetime import datetime
from decimal import Decimal
# from src.models.examination import Examination
# from src.models.student import Student
# from src.models.examsubject import ExamSubject
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class StudentExamMark(Base):
    __tablename__ = "StudentExamMark"

    markID: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    examID: Mapped[int] = mapped_column(
        ForeignKey("Examination.examID"),
        nullable=False
    )

    examSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ExamSubject.examSubjectID"),
        nullable=False
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"),
        nullable=False
    )

    writtenMarks: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0
    )

    mcqMarks: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0
    )

    practicalMarks: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0
    )

    vivaMarks: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0
    )

    totalMarks: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0
    )

    isPassed: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    isLocked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
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


    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"),
        nullable=False,
    )

    examSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ExamSubject.examSubjectID"),
        nullable=False,
    )
    
    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"),
        nullable=False,
    )

    examSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ExamSubject.examSubjectID"),
        nullable=False,
    )

