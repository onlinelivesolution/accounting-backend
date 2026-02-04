from sqlalchemy import Column, Integer, String, DateTime, Numeric
from pydantic import BaseModel, ConfigDict
from src.services.database import Base

class EmployeePayment(Base):
    __tablename__ = "EmployeePayment"

    employeePaymentID = Column(Integer, primary_key=True, index=True)
    fiscalYear        = Column(String(4), nullable=False)
    month             = Column(Integer, nullable=False)
    companyCode       = Column(String(2), nullable=False)
    total             = Column(Numeric(18, 2), nullable=False)
    paymentMethodID   = Column(Integer, nullable=False)
    bankAccountNumber = Column(String(25), nullable=False)
    chequeNumber      = Column(String(30), nullable=False)
    paymentType       = Column(Integer, nullable=False)
    status            = Column(Integer, nullable=False)
    createdBy         = Column(String(50), nullable=False)
    createdDate       = Column(DateTime, nullable=False)
    
    class Config:
        from_attributes = True

    
