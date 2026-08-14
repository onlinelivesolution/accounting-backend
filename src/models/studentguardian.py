from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship as orm_relationship

from src.services.database import Base


class StudentGuardian(Base):
    __tablename__ = "StudentGuardian"

    guardianID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    guardianName: Mapped[str] = mapped_column(String(150), nullable=False)

    relationship: Mapped[str] = mapped_column(String(50), nullable=False)

    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    alternatePhone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    email: Mapped[str | None] = mapped_column(String(150), nullable=True)

    occupation: Mapped[str | None] = mapped_column(String(100), nullable=True)

    address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    isPrimary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # SQLAlchemy relationship
    student = orm_relationship("Student", back_populates="guardians")
