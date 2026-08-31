from datetime import date, datetime, time

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class ExamSchedule(Base):
    __tablename__ = "ExamSchedule"

    examScheduleID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    examID: Mapped[int] = mapped_column(
        ForeignKey("Examination.examID"),
        nullable=False,
    )

    examSubjectID: Mapped[int] = mapped_column(
        ForeignKey("ExamSubject.examSubjectID"),
        nullable=False,
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"),
        nullable=False,
    )

    sectionID: Mapped[int | None] = mapped_column(
        ForeignKey("Section.sectionID"),
        nullable=True,
    )

    examDate: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    startTime: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    endTime: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    roomNo: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    instructions: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    isActive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # =========================================================
    # Relationships
    # =========================================================



    examination: Mapped["Examination"] = relationship(
        "Examination",
        back_populates="examSchedules",
        lazy="selectin",
    )

    examSubject: Mapped["ExamSubject"] = relationship(
        "ExamSubject",
        back_populates="examSchedules",
        lazy="selectin",
    )

    schoolClass: Mapped["SchoolClass"] = relationship(
        "SchoolClass",
        back_populates="examSchedules",
        lazy="selectin",
    )

    section: Mapped["Section | None"] = relationship(
        "Section",
        back_populates="examSchedules",
        lazy="selectin",
    )
