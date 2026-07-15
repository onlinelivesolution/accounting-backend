from sqlalchemy import Column, Integer, String, DateTime, BigInteger, LargeBinary, Boolean, Numeric
from src.services.database import Base

class EmployeeHistory(Base):
    __tablename__ = "EmployeeHistory"

    employeeHistoryID   = Column(BigInteger, primary_key=True, index=True)
    employeeID          = Column(Integer, nullable=True)
    payscaleID           = Column(Integer, nullable=True)
    companyCode         = Column(String(2), nullable=True)
    departmentCode      = Column(String(4), nullable=True)
    sectionCode         = Column(String(6), nullable=True)
    transferID          = Column(Integer, nullable=True)
    promotionID         = Column(Integer, nullable=True)
    designationID       = Column(Integer, nullable=True)
    payrollScheduleID   = Column(Integer, nullable=True)
    status              = Column(Integer, nullable=True)
    isCurrentEmployee   = Column(Boolean, nullable=True)
    isRejoin            = Column(Boolean, nullable=True)
    rejoinDate          = Column(DateTime, nullable=True)
    joiningDate         = Column(DateTime, nullable=True)    
    evaluationID        = Column(Integer, nullable=True)
    isOvertimeAllowed   = Column(Boolean, nullable=True)
    leavePolicyID       = Column(Integer, nullable=True)
    employeeTypeID      = Column(Integer, nullable=True)
    yearOfExperience    = Column(Numeric(18, 2), nullable=True)
    maritalStatus       = Column(Integer, nullable=True)    
    passportNumber      = Column(String(20), nullable=True)    
    createdBy           = Column(String(30), nullable=True)
    createdDate         = Column(DateTime, nullable=True) 
    updatedBy           = Column(String(30), nullable=True)
    updatedDate         = Column(DateTime, nullable=True) 
    supplementaryPF     = Column(Numeric(18, 2), nullable=True)
    isPFApplicable      = Column(Boolean, nullable=True)
    employeeSetID       = Column(Integer, nullable=True)

    

    
