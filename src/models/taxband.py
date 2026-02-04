from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class TaxBand(Base):
    __tablename__ = "TaxBand"
    
    taxBandID               = Column(Integer, primary_key=True, index=True)    
    taxDefinitionID         = Column(Integer, nullable=False)
    bandName                = Column(String(50), nullable=False)
    startRange              = Column(Numeric(18, 2), nullable=False)
    endRange                = Column(Numeric(18, 2), nullable=False)
    percentage              = Column(Numeric(18, 2), nullable=False)
 
           
    