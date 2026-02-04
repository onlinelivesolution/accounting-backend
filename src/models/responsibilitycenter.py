from sqlalchemy import Column, Integer, String, Numeric, BigInteger, DateTime
from src.services.database import Base

class ResponsibilityCenter(Base):
    __tablename__ = "ResponsibilityCenter"
    
    respCenterCode = Column(String(6), primary_key=True, index=True)
    respCenterName = Column(String(50), nullable=False)
    activityCenterCode          = Column(String(4), nullable=False) 
