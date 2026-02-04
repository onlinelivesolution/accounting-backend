from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class EmployeeLoanAdjust(Base):
    __tablename__ = "EmployeeLoanAdjust"
    
    employeeLoanAdjustID       = Column(Integer, primary_key=True, index=True)    
    employeeLoanID             = Column(Integer, nullable=False)
    salaryID                   = Column(Integer, nullable=False)
    adjustAmount               = Column(Numeric(18, 2), nullable=False)
    adjustDate                 = Column(DateTime, nullable=False)
    note                       = Column(String(200), nullable=False) 
    isPosted                   = Column(Boolean, nullable=False)
 
           
    
  