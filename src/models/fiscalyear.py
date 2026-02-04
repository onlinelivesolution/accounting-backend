from sqlalchemy import Column, String, Integer, Boolean
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship
from src.services.database import Base

class FiscalYear(Base):
    __tablename__ = "FiscalYear"

    finYearID = Column(Integer, primary_key=True, index=True)
    finYear = Column(String, nullable=False)
    isCurrentFinYear = Column(Boolean, default=True)
    companyCode = Column(String, nullable=False)
    
    class Config:
        from_attributes = True