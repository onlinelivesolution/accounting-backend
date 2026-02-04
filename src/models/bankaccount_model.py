from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from src.services.database import Base

class BankAccount(Base):
    __tablename__ = "BankAccount"

    bankAccountID         = Column(Integer, primary_key=True, index=True)
    bankAccountName       = Column(String(150), nullable=False)
    category              = Column(String(50), nullable=False)
    defaultPaymentMethod  = Column(Integer, nullable=False)
    bankName              = Column(String(150), nullable=False)
    accountNumber         = Column(String(100), nullable=False)
    branchName            = Column(String(150), nullable=False)
    branchCode            = Column(String(50), nullable=False)
    description           = Column(String(255), nullable=False)
    isActive              = Column(Boolean, default=True)
    isDefault             = Column(Boolean, default=True)
    detailItemCode        = Column(String(9), ForeignKey("DetailItem.detailItemCode"), nullable=False)
    createdDate           = Column(DateTime, nullable=False)
    openingBalanceDate   = Column(Date, nullable=False)
    
    
