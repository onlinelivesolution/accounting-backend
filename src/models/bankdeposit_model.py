from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from src.services.database import Base

class BankDeposit(Base):
    __tablename__ = "BankDeposit"

    bankDepositID       = Column(Integer, primary_key=True, index=True)
    bankAccountID       = Column(Integer, nullable=False)
    accountNumber       = Column(String(20), nullable=False)
    depositType         = Column(Integer, nullable=False)
    depositRefNo        = Column(String(25), nullable=False)
    depositDate         = Column(DateTime, nullable=False)
    depositedBy         = Column(String(50), nullable=False)
    amount              = Column(Numeric(18, 2), nullable=False)
    shortNote           = Column(String(50), nullable=False)
    status              = Column(Integer, nullable=False)
    isDeleted           = Column(Boolean, default=True)
    createdBy           = Column(String(50), nullable=False)
    createdDate         = Column(DateTime, nullable=False)
    updatedBy           = Column(String(50), nullable=False)
    updatedDate         = Column(DateTime, nullable=False)
    