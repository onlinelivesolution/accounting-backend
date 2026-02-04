from sqlalchemy import Column, Integer, String, Numeric, BigInteger, DateTime
from src.services.database import Base

class ActivityCenter(Base):
    __tablename__ = "ActivityCenter"
    
    activityCenterCode = Column(String(4), primary_key=True, index=True)
    activityCenterName = Column(String(50), nullable=False)
    companyCode          = Column(String(2), nullable=False) 
