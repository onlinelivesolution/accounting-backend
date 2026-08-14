from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class ClassSubject(Base):
    __tablename__ = "ClassSubject"

    classSubjectID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"), nullable=False
    )

    subjectID: Mapped[int] = mapped_column(
        ForeignKey("Subject.subjectID"), nullable=False
    )

    isCompulsory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    schoolClass = orm_relationship("SchoolClass", back_populates="classSubjects")

    subject = orm_relationship("Subject", back_populates="classSubjects")

    examSubjects = orm_relationship(
        "ExamSubject", back_populates="classSubject", lazy="selectin"
    )
