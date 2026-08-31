from datetime import datetime
from decimal import Decimal

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
        autoincrement=True,
    )

    examID: Mapped[int] = mapped_column(
        ForeignKey("Examination.examID"),
        nullable=False,
    )

    classSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ClassSubject.classSubjectID"),
        nullable=False,
    )

    fullMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    passMarks: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    isOptional: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    createdDate: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # =========================================================
    # Relationships
    # =========================================================


    examination: Mapped["Examination"] = relationship(
        "Examination",
        back_populates="examSubjects",
        lazy="selectin",
    )

    classSubject: Mapped["ClassSubject"] = relationship(
        "ClassSubject",
        back_populates="examSubjects",
        lazy="selectin",
    )

    examSchedules: Mapped[list["ExamSchedule"]] = relationship(
        "ExamSchedule",
        back_populates="examSubject",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    studentMarks: Mapped[list["StudentExamMark"]] = relationship(
        "StudentExamMark",
        back_populates="examSubject",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
