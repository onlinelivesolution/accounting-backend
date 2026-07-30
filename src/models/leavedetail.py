from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, BigInteger

from sqlalchemy.orm import relationship
from src.services.database import Base

class LeaveDetail(Base):
    __tablename__ = "LeaveDetail"
    
    leaveDetailID         = Column(Integer, primary_key=True, index=True) 
    leaveID               = Column(Integer, ForeignKey("Leave.leaveID"))
    employeeID            = Column(BigInteger, ForeignKey("Employee.employeeID"))
    startDate             = Column(DateTime, nullable=True)
    endDate               = Column(DateTime, nullable=True) 
    outOfStation          = Column(String(100), nullable=True) 
    totalDays             = Column(Numeric(18, 2), nullable=True)
    shortNote             = Column(String(200), nullable=True) 
    status                = Column(Integer, nullable=True)
    approvedBy            = Column(String(50), nullable=True)
    rejectedBy            = Column(String(50), nullable=True)
    appliedDate           = Column(DateTime, nullable=True) 
    leaveTypeID           = Column(Integer, nullable=True)
    createdBy             = Column(String(50), nullable=True)
    createdDate           = Column(DateTime, nullable=True) 
    updatedBy             = Column(String(50), nullable=True)
    updatedDate           = Column(DateTime, nullable=True)
    companyCode           = Column(String(2), nullable=True) 
    departmentCode        = Column(String(4), nullable=True) 
    sectionCode           = Column(String(6), nullable=True) 
    comments              = Column(String(200), nullable=True)
    isUnPaid              = Column(Boolean)
    fiscalYear            = Column(String(4), nullable=True)
    leavePurpose          = Column(String(200), nullable=True)
  
  
    leave = relationship("Leave", back_populates="details")
    employee = relationship("Employee", back_populates="leave_details")
