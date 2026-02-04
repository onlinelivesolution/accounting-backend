from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from src.services.database import Base

class ContactPerson(Base):
    __tablename__ = "ContactPerson"

    contactPersonID     = Column(Integer, primary_key=True, index=True)
    name                = Column(String(20), nullable=False)
    designation         = Column(String(25), nullable=False)
    phone               = Column(String(20), nullable=False)
    email               = Column(String(25), nullable=False)
    status              = Column(Integer, nullable=False)
    isDeleted           = Column(Boolean, default=True)
    createdBy           = Column(String(50), nullable=False)
    createdDate         = Column(DateTime, nullable=False)
    updatedBy           = Column(String(50), nullable=False)
    updatedDate         = Column(DateTime, nullable=False)