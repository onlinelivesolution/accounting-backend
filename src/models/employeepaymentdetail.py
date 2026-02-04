from sqlalchemy import Column, Integer, String, DateTime, Numeric
from pydantic import BaseModel, ConfigDict
from src.services.database import Base

class EmployeePaymentDetail(Base):
    __tablename__ = "EmployeePaymentDetail"

    employeePaymentDetailID = Column(Integer, primary_key=True, index=True)
    employeePaymentID       = Column(Integer, nullable=False)
    employeeID              = Column(Integer, nullable=False)
    sectionCode             = Column(String(6), nullable=False)
    amount                  = Column(Numeric(18, 2), nullable=False)
    referenceID             = Column(Integer, nullable=False)
    note                    = Column(String(200), nullable=False)
    providentFund           = Column(Numeric(18, 2), nullable=False)
    supplementaryPF         = Column(Numeric(18, 2), nullable=False)
    employerContribution    = Column(Numeric(18, 2), nullable=False)
    
    class Config:
        from_attributes = True