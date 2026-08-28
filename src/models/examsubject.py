from datetime import datetime
from decimal import Decimal
# from src.models.examschedule import ExamSchedule
# from src.models.classsubject import ClassSubject
# from src.models.examination import Examination
# from src.models.studentexammark import StudentExamMark
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base

class ExamSubject(Base):
    __tablename__ = "ExamSubject"

    examSubjectID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    examID: Mapped[int] = mapped_column(
        ForeignKey("Exam.examID"),
        nullable=False
    )

    classSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ClassSubject.classSubjectID"),
        nullable=False
    )

    fullMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    passMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    isOptional: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    createdDate: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    # -----------------------------------------
    # Relationships
    # -----------------------------------------

    examination: Mapped["Examination"] = relationship(
        "Examination",
        back_populates="examSubjects"
    )

    classSubject: Mapped["ClassSubject"] = relationship(
        "ClassSubject"
    )

    examSchedules: Mapped[list["ExamSchedule"]] = relationship(
        "ExamSchedule",
        back_populates="examSubject"
    )

    studentMarks: Mapped[list["StudentExamMark"]] = relationship(
        "StudentExamMark",
        back_populates="examSubject"
    )