from datetime import date, datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship as orm_relationship,
)

from src.services.database import Base


class Student(Base):
    __tablename__ = "Student"

    studentID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentCode: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    admissionNo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    firstName: Mapped[str] = mapped_column(String(100), nullable=False)

    middleName: Mapped[str | None] = mapped_column(String(100), nullable=True)

    lastName: Mapped[str | None] = mapped_column(String(100), nullable=True)

    dateOfBirth: Mapped[date | None] = mapped_column(Date, nullable=True)

    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)

    bloodGroup: Mapped[str | None] = mapped_column(String(10), nullable=True)

    photoPath: Mapped[str | None] = mapped_column(String(500), nullable=True)

    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    email: Mapped[str | None] = mapped_column(String(150), nullable=True)

    address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    postalCode: Mapped[str | None] = mapped_column(String(20), nullable=True)

    admissionDate: Mapped[date | None] = mapped_column(Date, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    guardians = orm_relationship(
        "StudentGuardian",
        back_populates="student",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    documents = orm_relationship(
        "StudentDocument",
        back_populates="student",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    enrollments = relationship(
        "StudentEnrollment",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    promotions = orm_relationship(
        "StudentPromotion",
        back_populates="student",
        lazy="selectin",
    )
