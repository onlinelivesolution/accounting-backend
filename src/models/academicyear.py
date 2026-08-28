from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class AcademicYear(Base):
    __tablename__ = "AcademicYear"

    academicYearID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    year: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    startDate: Mapped[date] = mapped_column(Date, nullable=False)

    endDate: Mapped[date] = mapped_column(Date, nullable=False)

    isCurrent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    examinations = orm_relationship(
        "Examination",
        back_populates="academicYear",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    
    enrollments = relationship(
        "StudentEnrollment",
        back_populates="academicYear",
    )
