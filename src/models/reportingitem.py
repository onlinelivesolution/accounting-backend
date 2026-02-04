from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from pydantic import BaseModel, ConfigDict
from src.services.database import Base

class ReportingItem(Base):
    __tablename__ = "ReportingItem"

    reportingItemCode = Column(String(20), primary_key=True)
    reportingItemName = Column(String(100), nullable=False)

    controlItemCode = Column(
        String(10),
        ForeignKey("ControlItem.controlItemCode"),
        nullable=False
    )
    
    class Config:
        from_attributes = True