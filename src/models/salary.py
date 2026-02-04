from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.services.database import Base

class Salary(Base):
    __tablename__ = "Salary"
    
    salaryID            = Column(Integer, primary_key=True, index=True) 
    fiscalYear          = Column(String(4), nullable=False)   
    month               = Column(Integer, nullable=False)
    workingDay          = Column(Numeric(18, 2), nullable=False)
    companyCode         = Column(String(2), nullable=False)
    departmentCode      = Column(String(4), nullable=False)
    sectionCode         = Column(String(6), nullable=False)   
    createdBy           = Column(String(50), nullable=False)    
    createdDate         = Column(DateTime, nullable=False)
    approvedBy          = Column(String(50), nullable=False)
    approvedDate        = Column(DateTime, nullable=False)
    hRComments          = Column(String(200), nullable=False) 
    status              = Column(Integer, nullable=False) 
    year                = Column(String(4), nullable=False)  
    
    details = relationship("SalaryDetail", back_populates="salary", cascade="all, delete-orphan")

    