from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, BigInteger

from sqlalchemy.orm import relationship
from src.services.database import Base

class LeaveDetail(Base):
    __tablename__ = "LeaveDetail"
    
    leaveDetailID         = Column(Integer, primary_key=True, index=True) 
    leaveID               = Column(Integer, ForeignKey("Leave.leaveID"))
    employeeID            = Column(BigInteger, ForeignKey("Employee.employeeID"))
    startDate             = Column(DateTime, nullable=False)
    endDate               = Column(DateTime, nullable=False) 
    outOfStation          = Column(String(100), nullable=False) 
    totalDays             = Column(Numeric(18, 2), nullable=False)
    shortNote             = Column(String(200), nullable=False) 
    status                = Column(Integer, nullable=False)
    approvedBy            = Column(String(50), nullable=False)
    rejectedBy            = Column(String(50), nullable=False)
    appliedDate           = Column(DateTime, nullable=False) 
    leaveTypeID           = Column(Integer, nullable=False)
    createdBy             = Column(String(50), nullable=False)
    createdDate           = Column(DateTime, nullable=False) 
    updatedBy             = Column(String(50), nullable=False)
    updatedDate           = Column(DateTime, nullable=False)
    companyCode           = Column(String(2), nullable=False) 
    departmentCode        = Column(String(4), nullable=False) 
    sectionCode           = Column(String(6), nullable=False) 
    comments              = Column(String(200), nullable=False)
    isUnPaid              = Column(Boolean)
    fiscalYear            = Column(String(4), nullable=False)
    leavePurpose          = Column(String(200), nullable=False)
  
  
    leave = relationship("Leave", back_populates="details")
    employee = relationship("Employee", back_populates="leave_details")
