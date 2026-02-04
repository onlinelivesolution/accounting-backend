from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from src.services.database import Base

class ControlItem(Base):
    __tablename__ = "ControlItem"

    controlItemCode = Column(String(10), primary_key=True)
    controlItemName = Column(String(100), nullable=False)
    accountCategory = Column(String(50))  # Asset, Liability, Income, Expense
    financialStatementType = Column(String(5))  # BS / PL
    isActive = Column(Boolean, default=True)

    
    class Config:
        from_attributes = True

