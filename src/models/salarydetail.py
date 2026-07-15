from sqlalchemy import Column, Integer, String, Numeric, DateTime, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class SalaryDetail(Base):
    __tablename__ = "SalaryDetail"
    
    salaryDetailID         = Column(BigInteger, primary_key=True, index=True)
    salaryID               = Column(Integer, ForeignKey("Salary.salaryID")) 
    employeeID             = Column(BigInteger, ForeignKey("Employee.employeeID"))
    payscaleID             = Column(Integer, nullable=True)
    absenceDay             = Column(Numeric(18, 2), nullable=True)
    basicSalary            = Column(Numeric(18, 2), nullable=True)
    houseRentAllowance     = Column(Numeric(18, 2), nullable=True)
    medicalAllowance       = Column(Numeric(18, 2), nullable=True)
    travelAllowance        = Column(Numeric(18, 2), nullable=True)
    conveyance             = Column(Numeric(18, 2), nullable=True)
    overtime               = Column(Numeric(18, 2), nullable=True)
    otherAllowance         = Column(Numeric(18, 2), nullable=True)
    grossEarnings          = Column(Numeric(18, 2), nullable=True)
    adjustUnPaidLeave      = Column(Numeric(18, 2), nullable=True)
    taxAmount              = Column(Numeric(18, 2), nullable=True)
    pFAmount               = Column(Numeric(18, 2), nullable=True)
    employerContribution   = Column(Numeric(18, 2), nullable=True)
    supplementaryPF        = Column(Numeric(18, 2), nullable=True)
    loanAdjust             = Column(Numeric(18, 2), nullable=True)
    houseRentDeduction     = Column(Numeric(18, 2), nullable=True)
    excessMobileBill       = Column(Numeric(18, 2), nullable=True)
    adjustAdvanceSalary    = Column(Numeric(18, 2), nullable=True)
    gradedTax              = Column(Numeric(18, 2), nullable=True)
    otherDeduction         = Column(Numeric(18, 2), nullable=True)
    netEarnings            = Column(Numeric(18, 2), nullable=True)
    companyCode            = Column(String(2), nullable=True)
    departmentCode         = Column(String(4), nullable=True)
    sectionCode            = Column(String(6), nullable=True) 
    status                 = Column(Integer, nullable=True) 
    isUnPaid               = Column(Boolean, nullable=True)
    createdBy              = Column(String(50), nullable=True)    
    createdDate            = Column(DateTime, nullable=True)
    settingTaxAmount       = Column(Numeric(18, 2), nullable=True)
    approvedDate           = Column(DateTime, nullable=True)
    
    @property
    def employeeName(self) -> str:
        return self.employee.employeeName if self.employee else None
    
    salary = relationship("Salary", back_populates="details")
    employee = relationship("Employee", back_populates="salary_details")
