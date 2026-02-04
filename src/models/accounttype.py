from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, ConfigDict
from src.services.database import Base

class AccountType(Base):
    __tablename__ = "AccountType"

    accountTypeID = Column(Integer, primary_key=True, index=True)
    accountTypeName = Column(String)
    isDeleted = Column(Boolean)
    
    class Config:
        from_attributes = True

    
