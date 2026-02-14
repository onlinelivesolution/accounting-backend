from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class LineItem(Base):
    __tablename__ = "LineItem"
    
    itemID           = Column(Integer, primary_key=True, index=True) 
    itemCode         = Column(String(30), nullable=False)
    itemName         = Column(String(50), nullable=False)
    categoryID       = Column(Integer, nullable=False)    
    unitPrice        = Column(Numeric(18, 2))
    isActive         = Column(Boolean, default=True)