from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.database import Base


class FeeStructure(Base):
    __tablename__ = "FeeStructure"

    feeStructureID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    academicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"), nullable=False
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("SchoolClass.classID"), nullable=False
    )

    feeHeadID: Mapped[int] = mapped_column(
        ForeignKey("FeeHead.feeHeadID"), nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    frequency: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Monthly"
    )

    effectiveFrom: Mapped[date | None] = mapped_column(Date, nullable=True)

    effectiveTo: Mapped[date | None] = mapped_column(Date, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)
