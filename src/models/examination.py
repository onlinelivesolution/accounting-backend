from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class Examination(Base):
    __tablename__ = "Examination"

    examinationID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    academicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"), nullable=False
    )

    examinationName: Mapped[str] = mapped_column(String(100), nullable=False)

    examinationType: Mapped[str] = mapped_column(String(50), nullable=False)

    startDate: Mapped[date | None] = mapped_column(Date, nullable=True)

    endDate: Mapped[date | None] = mapped_column(Date, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    academicYear = orm_relationship("AcademicYear", back_populates="examinations")

    examSubjects = orm_relationship(
        "ExamSubject",
        back_populates="examination",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
