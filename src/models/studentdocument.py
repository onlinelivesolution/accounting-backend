from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class StudentDocument(Base):
    __tablename__ = "StudentDocument"

    documentID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    documentType: Mapped[str] = mapped_column(String(50), nullable=False)

    documentName: Mapped[str] = mapped_column(String(200), nullable=False)

    fileName: Mapped[str | None] = mapped_column(String(255), nullable=True)

    filePath: Mapped[str | None] = mapped_column(String(500), nullable=True)

    fileExtension: Mapped[str | None] = mapped_column(String(20), nullable=True)

    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    uploadedDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    # Relationship
    student = orm_relationship("Student", back_populates="documents")
