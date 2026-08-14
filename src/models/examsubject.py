from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class ExamSubject(Base):
    __tablename__ = "ExamSubject"

    examSubjectID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    examID: Mapped[int] = mapped_column(ForeignKey("Exam.examID"), nullable=False)

    classSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ClassSubject.classSubjectID"), nullable=False
    )

    fullMarks: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, default=100
    )

    passMarks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=33)

    isOptional: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    exam = orm_relationship("Exam", back_populates="examSubjects")

    classSubject = orm_relationship("ClassSubject", back_populates="examSubjects")

    marks = orm_relationship(
        "StudentMark",
        back_populates="examSubject",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
