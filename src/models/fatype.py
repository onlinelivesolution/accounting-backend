from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, ConfigDict
from src.services.database import Base

class FAType(Base):
    __tablename__ = "FAType"

    fATypeID = Column(Integer, primary_key=True, index=True)
    fATypeName = Column(String)
    fAHeadID = Column(String)
    
    class Config:
        from_attributes = True