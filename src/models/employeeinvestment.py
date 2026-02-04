from sqlalchemy import Column, Integer, String, Numeric, BigInteger, DateTime
from src.services.database import Base

class EmployeeInvestment(Base):
    __tablename__ = "EmployeeInvestment"
    
    employeeInvestmentID   = Column(Integer, primary_key=True, index=True) 
    investmentNumber       = Column(String(10), nullable=False)
    employeeID             = Column(BigInteger, nullable=False)
    fiscalYear             = Column(String(4), nullable=False) 
    investAmount           = Column(Numeric(18, 2), nullable=False)
    status                 = Column(Integer, nullable=False)
    createdBy              = Column(String(50), nullable=False)    
    createdDate            = Column(DateTime, nullable=False)
    updatedBy              = Column(String(50), nullable=False)    
    updatedDate            = Column(DateTime, nullable=False)

   
   
   