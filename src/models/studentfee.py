from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship as orm_relationship
from sqlalchemy import Computed
from src.services.database import Base


class StudentFee(Base):
    __tablename__ = "StudentFee"

    studentFeeID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    enrollmentID: Mapped[int] = mapped_column(
        ForeignKey("StudentEnrollment.enrollmentID"), nullable=False
    )

    academicYearID: Mapped[int] = mapped_column(
        ForeignKey("AcademicYear.academicYearID"), nullable=False
    )

    feeHeadID: Mapped[int] = mapped_column(
        ForeignKey("FeeHead.feeHeadID"), nullable=False
    )

    feeMonth: Mapped[date | None] = mapped_column(Date, nullable=True)

    dueDate: Mapped[date | None] = mapped_column(Date, nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    discountAmount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=0
    )

    paidAmount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=0
    )

    dueAmount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), Computed("amount - discountAmount - paidAmount", persisted=True)
    )

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Unpaid")

    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    feeHead = orm_relationship("FeeHead", back_populates="studentFees")
