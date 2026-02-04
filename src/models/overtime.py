from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class Overtime(Base):
    __tablename__ = "Overtime"
    
    overtimeID            = Column(Integer, primary_key=True, index=True) 
    overtimeDate          = Column(DateTime, nullable=False) 
    companyCode           = Column(String(2), nullable=False) 
    shortNote             = Column(String(200), nullable=False)  
    status                = Column(Integer, nullable=False)
    createdBy             = Column(String(50), nullable=False)
    createdDate           = Column(DateTime, nullable=False) 
    approvedBy            = Column(String(50), nullable=False)
    updatedBy             = Column(String(50), nullable=False)
    updatedDate           = Column(DateTime, nullable=False)
    year                  = Column(String(4), nullable=False)
    month                 = Column(Integer, nullable=False)
    
    details = relationship("OvertimeDetail", back_populates="overtime", cascade="all, delete-orphan")
