from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class VATRates(Base):
    __tablename__ = "VATRates"

    vATRateID      = Column(Integer, primary_key=True, index=True)
    vATRateName    = Column(String(50), nullable=False)
    ratePercent    = Column(Numeric(5, 2), nullable=False)
    effectiveFrom  = Column(Date, nullable=False)
    effectiveTo    = Column(Date, nullable=False)
    companyCode    = Column(String(), nullable=False) 
    isActive       = Column(Boolean, default=True)
    createdBy      = Column(String(50), nullable=False)    
    createdDate    = Column(DateTime, nullable=False)
    updatedBy      = Column(String(50), nullable=False)    
    updatedDate    = Column(DateTime, nullable=False)

