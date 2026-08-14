from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Computed
from src.services.database import Base

class StudentPaymentDetail(Base):
    __tablename__ = "StudentPaymentDetail"

    paymentDetailID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    paymentID: Mapped[int] = mapped_column(
        ForeignKey("StudentPayment.paymentID"), nullable=False
    )

    studentFeeID: Mapped[int] = mapped_column(
        ForeignKey("StudentFee.studentFeeID"), nullable=False
    )

    paidAmount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    payment = relationship("StudentPayment", back_populates="paymentDetails")

    studentFee = relationship("StudentFee")
