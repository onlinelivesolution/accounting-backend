from sqlalchemy import Column, String
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship
from src.services.database import Base

class Company(Base):
    __tablename__ = "Company"

    companyCode = Column(String(2), primary_key=True, index=True)
    companyName = Column(String(200))
    
    class Config:
        from_attributes = True