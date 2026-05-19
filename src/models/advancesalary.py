from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from src.services.database import Base

class AdvanceSalary(Base):
    __tablename__ = "AdvanceSalary"
    
    advanceSalaryID        = Column(Integer, primary_key=True, index=True)    
    employeeID             = Column(BigInteger, ForeignKey("Employee.employeeID"))
    amount                 = Column(Numeric(18, 2), nullable=False)
    purpose                = Column(String(200), nullable=False)
    fiscalYear             = Column(String(4), nullable=False)    
    month                  = Column(Integer, nullable=False)
    requiredDate           = Column(DateTime, nullable=False)
    hRComments             = Column(String(200), nullable=False)
    companyCode            = Column(String(2), nullable=False)
    departmentCode         = Column(String(4), nullable=False)
    sectionCode            = Column(String(6), nullable=False)
    status                 = Column(Integer, nullable=False)
    approvedBy             = Column(String(30), nullable=False)
    paidBy                 = Column(String(30), nullable=False)
    paymentMethodID        = Column(Integer, nullable=False)
    bankAccountNumber      = Column(String(25), nullable=False)
    chequeNumber           = Column(String(30), nullable=False)
    createdBy              = Column(String(50), nullable=False)
    createdDate            = Column(DateTime, nullable=False)
    updatedBy              = Column(String(50), nullable=False)
    updatedDate            = Column(DateTime, nullable=False)
    salaryID               = Column(Integer, nullable=False)
    
    employee = relationship("Employee", back_populates="advance_salary")

 
           
    