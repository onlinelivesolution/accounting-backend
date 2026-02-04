from sqlalchemy import Column, Integer, String, DateTime, Text, func
from src.services.database import Base
from datetime import datetime

class FailedEmployeeUpload(Base):
    __tablename__ = "FailedEmployeeUpload"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employeeCode = Column(String(10), nullable=True)
    reason = Column(Text, nullable=True)
    rawData = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now())