from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Computed
from src.services.database import Base


class StudentPayment(Base):
    __tablename__ = "StudentPayment"

    paymentID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("Student.studentID"), nullable=False
    )

    paymentDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    receiptNo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    totalAmount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    paymentMethod: Mapped[str] = mapped_column(String(30), nullable=False)

    referenceNo: Mapped[str | None] = mapped_column(String(100), nullable=True)

    bankAccountID: Mapped[int | None] = mapped_column(Integer, nullable=True)

    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)

    journalHeaderID: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Completed")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    student = relationship("Student")

    paymentDetails = relationship(
        "StudentPaymentDetail",
        back_populates="payment",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
