from datetime import datetime
# from src.models.examination import Examination
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class ExamType(Base):
    __tablename__ = "ExamType"

    examTypeID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    examTypeName: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    isActive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    examinations: Mapped[list["Examination"]] = relationship(
        "Examination",
        back_populates="examType"
    )