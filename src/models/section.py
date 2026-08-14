from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class Section(Base):
    __tablename__ = "Section"

    sectionID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"), nullable=False
    )

    sectionName: Mapped[str] = mapped_column(String(50), nullable=False)

    sectionCode: Mapped[str] = mapped_column(String(20), nullable=False)

    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    schoolClass = relationship("SchoolClass", back_populates="sections")

    enrollments = relationship(
        "StudentEnrollment", back_populates="section", lazy="selectin"
    )
