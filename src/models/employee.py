from sqlalchemy import Column, Integer, String, DateTime, BigInteger, LargeBinary
from sqlalchemy.orm import relationship
from src.services.database import Base

class Employee(Base):
    __tablename__ = "Employee"

    employeeID          = Column(BigInteger, primary_key=True, index=True)
    employeeCode        = Column(String, nullable=False)
    applicantID         = Column(Integer, nullable=False)
    firstName           = Column(String(30), nullable=False)
    middleName          = Column(String(30), nullable=False)
    lastName            = Column(String(30), nullable=False)
    employeeName        = Column(String(90), nullable=False)
    fatherName          = Column(String(50), nullable=False)
    motherName          = Column(String(50), nullable=False)
    gender              = Column(Integer, nullable=False)
    dateOfBirth         = Column(DateTime, nullable=False)    
    nationalID          = Column(String(20), nullable=False)
    address             = Column(String(500), nullable=False)
    postalAddress       = Column(String(500), nullable=False)
    accountHolder       = Column(String(100), nullable=False)
    bankID              = Column(Integer, nullable=False)
    bankBranchID        = Column(Integer, nullable=False)    
    accountNumber       = Column(String(25), nullable=False)
    designation         = Column(String(50), nullable=False)
    joinDate            = Column(DateTime, nullable=False)
    email               = Column(String(50), nullable=False)
    phone               = Column(String(31), nullable=False)    
    companyCode         = Column(String(2), nullable=False)
    activityCenterCode  = Column(String(4), nullable=False)
    respCenterCode      = Column(String(6), nullable=False)    
    emergencyContact    = Column(String(30), nullable=False)
    employeeImage       = Column(LargeBinary, nullable=True)
    status              = Column(Integer, nullable=False)
    deviceID            = Column(Integer, nullable=False)    
    gradedTaxNo         = Column(String(25), nullable=False)
    terminitionDate     = Column(DateTime, nullable=False)
    employeeSetID       = Column(Integer, nullable=False)
    createdBy           = Column(String(50), nullable=False)
    createdDate         = Column(DateTime, nullable=False)
    updatedBy           = Column(String(50), nullable=False)
    updatedDate         = Column(DateTime, nullable=False)
    
    payscales = relationship("PayScale", back_populates="employee")
    overtime_details = relationship("OvertimeDetail", back_populates="employee")
    loans = relationship("EmployeeLoan", back_populates="employee")
    advance_salary = relationship("AdvanceSalary", back_populates="employee")
    leave_details = relationship("LeaveDetail", back_populates="employee")
    salary_details = relationship("SalaryDetail", back_populates="employee")
    

    
