from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class Branch(Base):
    __tablename__ = "Branch"

    branchID        = Column(Integer, primary_key=True, index=True)
    branchCode      = Column(String(10), nullable=False)
    countryID       = Column(Integer, nullable=False)
    bankID          = Column(Integer, nullable=False)
    branchName      = Column(String(50), nullable=False)
    address         = Column(String(200), nullable=False)
    isDeleted       = Column(Boolean, default=True)
    createdBy       = Column(String(50), nullable=False)
    createdDate     = Column(DateTime, nullable=False)
    updatedBy       = Column(String(50), nullable=False)
    updatedDate     = Column(DateTime, nullable=False)
