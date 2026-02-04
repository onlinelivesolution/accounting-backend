from sqlalchemy import Column, Integer, String, DateTime, BigInteger, LargeBinary, Boolean, Numeric
from src.services.database import Base

class EmployeeHistory(Base):
    __tablename__ = "EmployeeHistory"

    employeeHistoryID   = Column(BigInteger, primary_key=True, index=True)
    employeeID          = Column(Integer, nullable=False)
    payscaleID           = Column(Integer, nullable=False)
    companyCode         = Column(String(2), nullable=False)
    departmentCode      = Column(String(4), nullable=False)
    sectionCode         = Column(String(6), nullable=False)
    transferID          = Column(Integer, nullable=False)
    promotionID         = Column(Integer, nullable=False)
    designationID       = Column(Integer, nullable=False)
    payrollScheduleID   = Column(Integer, nullable=False)
    status              = Column(Integer, nullable=False)
    isCurrentEmployee   = Column(Boolean, nullable=False)
    isRejoin            = Column(Boolean, nullable=False)
    rejoinDate          = Column(DateTime, nullable=False)
    joiningDate         = Column(DateTime, nullable=False)    
    evaluationID        = Column(Integer, nullable=False)
    isOvertimeAllowed   = Column(Boolean, nullable=False)
    leavePolicyID       = Column(Integer, nullable=False)
    employeeTypeID      = Column(Integer, nullable=False)
    yearOfExperience    = Column(Numeric(18, 2), nullable=False)
    maritalStatus       = Column(Integer, nullable=False)    
    passportNumber      = Column(String(20), nullable=False)    
    createdBy           = Column(String(30), nullable=False)
    createdDate         = Column(DateTime, nullable=False) 
    updatedBy           = Column(String(30), nullable=False)
    updatedDate         = Column(DateTime, nullable=False) 
    supplementaryPF     = Column(Numeric(18, 2), nullable=False)
    isPFApplicable      = Column(Boolean, nullable=False)
    employeeSetID       = Column(Integer, nullable=False)

    

    
