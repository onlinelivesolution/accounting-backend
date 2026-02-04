from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from src.services.database import Base

class BankAccAndAccType(Base):
    __tablename__ = "BankAccAndAccType"

    bankAccAndAccTypeID = Column(Integer, primary_key=True, index=True)
    bankAccountID       = Column(Integer, nullable=False)
    bankAccountTypeID   = Column(Integer, nullable=False)
    contactPersonID     = Column(Integer, nullable=False)
    responsiblePersonID = Column(Integer, nullable=False)
    status              = Column(Integer, nullable=False)
    isDeleted           = Column(Boolean, default=True)
    createdBy           = Column(String(50), nullable=False)
    createdDate         = Column(DateTime, nullable=False)
    updatedBy           = Column(String(50), nullable=False)
    updatedDate         = Column(DateTime, nullable=False)
    