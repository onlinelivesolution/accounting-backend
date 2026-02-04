from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class Leave(Base):
    __tablename__ = "Leave"
    
    leaveID               = Column(Integer, primary_key=True, index=True) 
    companyCode           = Column(String(2), nullable=False)
    fiscalYear            = Column(String(4), nullable=False)
    status                = Column(Integer, nullable=False)    
    createdBy             = Column(String(50), nullable=False)
    createdDate           = Column(DateTime, nullable=False) 
    updatedBy             = Column(String(50), nullable=False)
    updatedDate           = Column(DateTime, nullable=False)

    
    details = relationship("LeaveDetail", back_populates="leave", cascade="all, delete-orphan")
