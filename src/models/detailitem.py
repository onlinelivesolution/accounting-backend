from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from src.services.database import Base

class DetailItem(Base):
    __tablename__ = "DetailItem"

    detailItemCode = Column(String(9), primary_key=True)
    detailItemName = Column(String(150), nullable=False)

    reportingItemCode = Column(
        String(20),
        ForeignKey("ReportingItem.reportingItemCode"),
        nullable=False
    )

    normalBalance = Column(String(6))  # DEBIT / CREDIT
    isActive = Column(Boolean, default=True)
    loadType = Column(String(20), nullable=True)

    
    class Config:
        from_attributes = True