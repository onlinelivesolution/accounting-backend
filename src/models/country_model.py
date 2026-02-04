from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class Country(Base):
    __tablename__ = "Country"

    countryID          = Column(Integer, primary_key=True, index=True)
    countryName        = Column(String(50), nullable=False)
