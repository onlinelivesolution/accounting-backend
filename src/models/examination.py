from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class Examination(Base):
    __tablename__ = "Examination"

    examID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    academicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"),
        nullable=False,
    )

    examName: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    examTypeID: Mapped[int] = mapped_column(
        ForeignKey("ExamType.examTypeID"),
        nullable=False,
    )

    startDate: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    endDate: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    createdDate: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    updatedDate: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # =========================================================
    # Relationships
    # =========================================================

    academicYear: Mapped["AcademicYear"] = relationship(
        "AcademicYear",
        back_populates="examinations",
        lazy="selectin",
    )
    
    examType: Mapped["ExamType"] = relationship(
        "ExamType",
        back_populates="examinations",
        lazy="selectin",
    )
    
    examSubjects: Mapped[list["ExamSubject"]] = relationship(
        "ExamSubject",
        back_populates="examination",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    examSchedules: Mapped[list["ExamSchedule"]] = relationship(
        "ExamSchedule",
        back_populates="examination",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
