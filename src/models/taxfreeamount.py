from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from src.services.database import Base

class TaxFreeAmount(Base):
    __tablename__ = "TaxFreeAmount"
    
    freeAmountID        = Column(Integer, primary_key=True, index=True)    
    gender              = Column(Integer, nullable=True)
    freeAmount          = Column(Numeric(18, 2), nullable=True)
    createdDate         = Column(DateTime, nullable=True)
    userID              = Column(String(50), nullable=True)    
   
   