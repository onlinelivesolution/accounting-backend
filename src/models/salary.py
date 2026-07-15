from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.services.database import Base

class Salary(Base):
    __tablename__ = "Salary"
    
    salaryID            = Column(Integer, primary_key=True, index=True) 
    fiscalYear          = Column(String(4), nullable=True)   
    month               = Column(Integer, nullable=True)
    workingDay          = Column(Numeric(18, 2), nullable=True)
    companyCode         = Column(String(2), nullable=True)
    departmentCode      = Column(String(4), nullable=True)
    sectionCode         = Column(String(6), nullable=True)   
    createdBy           = Column(String(50), nullable=True)    
    createdDate         = Column(DateTime, nullable=True)
    approvedBy          = Column(String(50), nullable=True)
    approvedDate        = Column(DateTime, nullable=True)
    hRComments          = Column(String(200), nullable=True) 
    status              = Column(Integer, nullable=True) 
    year                = Column(String(4), nullable=True)  
    
    details = relationship("SalaryDetail", back_populates="salary", cascade="all, delete-orphan")

    