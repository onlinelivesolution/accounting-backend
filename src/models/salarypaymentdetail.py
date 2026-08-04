from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func


class SalaryPaymentDetail(Base):
    __tablename__ = "SalaryPaymentDetail"

    salaryPaymentDetailID = Column(Integer, primary_key=True, index=True)
    salaryPaymentID = Column(
        Integer, ForeignKey("SalaryPayment.salaryPaymentID"), nullable=True
    )
    salaryID = Column(Integer, nullable=True)
    employeeID = Column(Integer, nullable=True)
    amount = Column(Numeric(18, 2), nullable=True)
    taxAmount = Column(Numeric(18, 2), nullable=True)
    pfAmount = Column(Numeric(18, 2), nullable=True)
    employerContribution = Column(Numeric(18, 2), nullable=True)
    loanAdjust = Column(Numeric(18, 2), nullable=True)
    adjustAdvanceSalary = Column(Numeric(18, 2), nullable=True)
    adjustUnpaidLeave = Column(Numeric(18, 2), nullable=True)
    paymentStatus = Column(Integer, nullable=True)


    salaryPayment = relationship(
        "SalaryPayment",
        back_populates="salaryPaymentDetails",
    )
