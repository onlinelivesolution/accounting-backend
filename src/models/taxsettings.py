from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class TaxSettings(Base):
    __tablename__ = "TaxSettings"
    
    taxSettingID          = Column(Integer, primary_key=True, index=True)    
    employeeID            = Column(Integer, nullable=True)
    employeeCode          = Column(String(10), nullable=True) 
    taxAmount             = Column(Numeric(18, 2), nullable=True)
    status                = Column(Integer, nullable=True)
   
   
   