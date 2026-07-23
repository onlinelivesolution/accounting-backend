from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func


class SalaryPayment(Base):
    __tablename__ = "SalaryPayment"

    salaryPaymentID = Column(Integer, primary_key=True, index=True)
    paymentNo = Column(String(10), nullable=True)
    paymentDate = Column(DateTime, nullable=True)
    salaryMonth = Column(String(20), nullable=True)
    salaryYear = Column(String(4), nullable=True)
    bankAccountID = Column(Integer, nullable=True)
    totalAmount = Column(Numeric(18, 2), nullable=True)
    remarks = Column(String(255), nullable=True)
    status = Column(Integer, nullable=True)
    createdBy = Column(Integer, nullable=True)
    createdDate = Column(DateTime, nullable=True, server_default=func.now())
    companyCode = Column(String(2))
    bankAccountID = Column(Integer)
    bankAccountCode = Column(String(50))
    paymentAmount = Column(Numeric(18,2))


    salaryPaymentDetails = relationship(
        "SalaryPaymentDetail",
        back_populates="salaryPayment",
        cascade="all, delete-orphan",
    )
