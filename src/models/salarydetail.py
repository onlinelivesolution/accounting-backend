from sqlalchemy import Column, Integer, String, Numeric, DateTime, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class SalaryDetail(Base):
    __tablename__ = "SalaryDetail"
    
    salaryDetailID         = Column(BigInteger, primary_key=True, index=True)
    salaryID               = Column(Integer, ForeignKey("Salary.salaryID")) 
    employeeID             = Column(BigInteger, ForeignKey("Employee.employeeID"))
    payscaleID             = Column(Integer, nullable=False)
    absenceDay             = Column(Numeric(18, 2), nullable=False)
    basicSalary            = Column(Numeric(18, 2), nullable=False)
    houseRentAllowance     = Column(Numeric(18, 2), nullable=False)
    medicalAllowance       = Column(Numeric(18, 2), nullable=False)
    travelAllowance        = Column(Numeric(18, 2), nullable=False)
    conveyance             = Column(Numeric(18, 2), nullable=False)
    overtime               = Column(Numeric(18, 2), nullable=False)
    otherAllowance         = Column(Numeric(18, 2), nullable=False)
    grossEarnings          = Column(Numeric(18, 2), nullable=False)
    adjustUnPaidLeave      = Column(Numeric(18, 2), nullable=False)
    taxAmount              = Column(Numeric(18, 2), nullable=False)
    pFAmount               = Column(Numeric(18, 2), nullable=False)
    employerContribution   = Column(Numeric(18, 2), nullable=False)
    supplementaryPF        = Column(Numeric(18, 2), nullable=False)
    loanAdjust             = Column(Numeric(18, 2), nullable=False)
    houseRentDeduction     = Column(Numeric(18, 2), nullable=False)
    excessMobileBill       = Column(Numeric(18, 2), nullable=False)
    adjustAdvanceSalary    = Column(Numeric(18, 2), nullable=False)
    gradedTax              = Column(Numeric(18, 2), nullable=False)
    otherDeduction         = Column(Numeric(18, 2), nullable=False)
    netEarnings            = Column(Numeric(18, 2), nullable=False)
    companyCode            = Column(String(2), nullable=False)
    departmentCode         = Column(String(4), nullable=False)
    sectionCode            = Column(String(6), nullable=False) 
    status                 = Column(Integer, nullable=False) 
    isUnPaid               = Column(Boolean, nullable=False)
    createdBy              = Column(String(50), nullable=False)    
    createdDate            = Column(DateTime, nullable=False)
    settingTaxAmount       = Column(Numeric(18, 2), nullable=False)
    approvedDate           = Column(DateTime, nullable=False)
    
    @property
    def employeeName(self) -> str:
        return self.employee.employeeName if self.employee else None
    
    salary = relationship("Salary", back_populates="details")
    employee = relationship("Employee", back_populates="salary_details")
