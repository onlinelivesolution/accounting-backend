from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class TaxDefinition(Base):
    __tablename__ = "TaxDefinition"
    
    taxDefinitionID        = Column(Integer, primary_key=True, index=True)    
    fiscalYear             = Column(String(4), nullable=False)
    taxFreeAmount          = Column(Numeric(18, 2), nullable=False)
    isAgeCreditApplicable  = Column(Boolean, nullable=False)
    age                    = Column(Numeric(18, 2), nullable=False)
    ageCredit              = Column(Numeric(18, 2), nullable=False)
    createdBy              = Column(String(50), nullable=False)    
    createdDate            = Column(DateTime, nullable=False)
    updatedBy              = Column(String(50), nullable=False)    
    updatedDate            = Column(DateTime, nullable=False)
    companyCode            = Column(String(2), nullable=False)    