from sqlalchemy import Column, Integer, String, Numeric, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class EmployeeLoan(Base):
    __tablename__ = "EmployeeLoan"
    
    employeeLoanID         = Column(Integer, primary_key=True, index=True)    
    employeeID             = Column(BigInteger, ForeignKey("Employee.employeeID"))
    loanAmount             = Column(Numeric(18, 2), nullable=False)
    interest               = Column(Numeric(18, 2), nullable=False)
    loanPurpose            = Column(String(200), nullable=False)    
    createdDate            = Column(DateTime, nullable=False)
    numberOfInstallment    = Column(Integer, nullable=False)
    installmentAmount      = Column(Numeric(18, 2), nullable=False)
    requiredDate           = Column(DateTime, nullable=False)
    hRComments             = Column(String(200), nullable=False) 
    companyCode            = Column(String(2), nullable=False)
    departmentCode         = Column(String(4), nullable=False)
    sectionCode            = Column(String(6), nullable=False) 
    status                 = Column(Integer, nullable=False) 
    fiscalYear             = Column(String(4), nullable=False) 
    approvedBy             = Column(String(50), nullable=False)
    paidBy                 = Column(String(50), nullable=False)
    loanActivatedDate      = Column(DateTime, nullable=False)
    paymentMethodID        = Column(Integer, nullable=False)    
    bankAccountNumber      = Column(String(25), nullable=False)
    chequeNumber           = Column(String(30), nullable=False)
    createdBy              = Column(String(50), nullable=False)
    createdDate            = Column(DateTime, nullable=False)    
    updatedBy              = Column(String(50), nullable=False) 
    updatedDate            = Column(DateTime, nullable=False) 
           
    employee = relationship("Employee", back_populates="loans")
  