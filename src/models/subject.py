from datetime import datetime

from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class Subject(Base):
    __tablename__ = "Subject"

    subjectID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    subjectCode: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    subjectName: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    classSubjects = orm_relationship(
        "ClassSubject",
        back_populates="subject",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
