from sqlalchemy import Column, Integer, String, DateTime, BigInteger, LargeBinary
from sqlalchemy.orm import relationship
from src.services.database import Base

class Employee(Base):
    __tablename__ = "Employee"

    employeeID          = Column(BigInteger, primary_key=True, index=True)
    employeeCode        = Column(String, nullable=True)
    applicantID         = Column(Integer, nullable=True)
    firstName           = Column(String(30), nullable=True)
    middleName          = Column(String(30), nullable=True)
    lastName            = Column(String(30), nullable=True)
    employeeName        = Column(String(90), nullable=True)
    fatherName          = Column(String(50), nullable=True)
    motherName          = Column(String(50), nullable=True)
    gender              = Column(Integer, nullable=True)
    dateOfBirth         = Column(DateTime, nullable=True)    
    nationalID          = Column(String(20), nullable=True)
    address             = Column(String(500), nullable=True)
    postalAddress       = Column(String(500), nullable=True)
    accountHolder       = Column(String(100), nullable=True)
    bankID              = Column(Integer, nullable=True)
    bankBranchID        = Column(Integer, nullable=True)    
    accountNumber       = Column(String(25), nullable=True)
    designation         = Column(String(50), nullable=True)
    joinDate            = Column(DateTime, nullable=True)
    email               = Column(String(50), nullable=True)
    phone               = Column(String(31), nullable=True)    
    companyCode         = Column(String(2), nullable=True)
    activityCenterCode  = Column(String(4), nullable=True)
    respCenterCode      = Column(String(6), nullable=True)    
    emergencyContact    = Column(String(30), nullable=True)
    employeeImage       = Column(LargeBinary, nullable=True)
    status              = Column(Integer, nullable=True)
    deviceID            = Column(Integer, nullable=True)    
    gradedTaxNo         = Column(String(25), nullable=True)
    terminitionDate     = Column(DateTime, nullable=True)
    employeeSetID       = Column(Integer, nullable=True)
    createdBy           = Column(String(50), nullable=True)
    createdDate         = Column(DateTime, nullable=True)
    updatedBy           = Column(String(50), nullable=True)
    updatedDate         = Column(DateTime, nullable=True)
    
    payscales = relationship("PayScale", back_populates="employee")
    overtime_details = relationship("OvertimeDetail", back_populates="employee")
    loans = relationship("EmployeeLoan", back_populates="employee")
    advance_salary = relationship("AdvanceSalary", back_populates="employee")
    leave_details = relationship("LeaveDetail", back_populates="employee")
    salary_details = relationship("SalaryDetail", back_populates="employee")
    

    
