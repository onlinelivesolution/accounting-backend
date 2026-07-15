from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class TaxDefinition(Base):
    __tablename__ = "TaxDefinition"
    
    taxDefinitionID        = Column(Integer, primary_key=True, index=True)    
    fiscalYear             = Column(String(4), nullable=True)
    taxFreeAmount          = Column(Numeric(18, 2), nullable=True)
    isAgeCreditApplicable  = Column(Boolean, nullable=True)
    age                    = Column(Numeric(18, 2), nullable=True)
    ageCredit              = Column(Numeric(18, 2), nullable=True)
    createdBy              = Column(String(50), nullable=True)    
    createdDate            = Column(DateTime, nullable=True)
    updatedBy              = Column(String(50), nullable=True)    
    updatedDate            = Column(DateTime, nullable=True)
    companyCode            = Column(String(2), nullable=True)    