from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class TaxBand(Base):
    __tablename__ = "TaxBand"
    
    taxBandID               = Column(Integer, primary_key=True, index=True)    
    taxDefinitionID         = Column(Integer, nullable=True)
    bandName                = Column(String(50), nullable=True)
    startRange              = Column(Numeric(18, 2), nullable=True)
    endRange                = Column(Numeric(18, 2), nullable=True)
    percentage              = Column(Numeric(18, 2), nullable=True)
 
           
    