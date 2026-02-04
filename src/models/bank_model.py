from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class Bank(Base):
    __tablename__ = "Bank"

    bankID          = Column(Integer, primary_key=True, index=True)
    bankCode        = Column(String(10), nullable=False)
    bankName        = Column(String(50), nullable=False)
    address         = Column(String(200), nullable=False)
    isDeleted       = Column(Boolean, default=True)
    createdBy       = Column(String(50), nullable=False)
    createdDate     = Column(DateTime, nullable=False)
    updatedBy       = Column(String(50), nullable=False)
    updatedDate     = Column(DateTime, nullable=False)
    companyCode     = Column(String(2), nullable=False)
