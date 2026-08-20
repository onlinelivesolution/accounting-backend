from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class SchoolClass(Base):
    __tablename__ = "SchoolClass"

    classID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    className: Mapped[str] = mapped_column(String(50), nullable=False)

    classCode: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    classOrder: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    sections = relationship("Section", back_populates="schoolClass", lazy="selectin")

    classSubjects = orm_relationship(
        "ClassSubject",
        back_populates="schoolClass",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    
    enrollments = relationship(
        "StudentEnrollment",
        back_populates="schoolClass",
    )
