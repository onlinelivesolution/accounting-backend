from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class ExamType(Base):
    __tablename__ = "ExamType"

    examTypeID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    examTypeName: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)
