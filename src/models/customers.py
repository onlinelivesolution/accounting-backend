from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class Customer(Base):
    __tablename__ = "Customer"
    
    customerID           = Column(Integer, primary_key=True, index=True) 
    customerName         = Column(String(50), nullable=False) 
    creditLimit          = Column(Numeric(18, 2))
    vatReference         = Column(String(50), nullable=False) 
    isActive             = Column(Boolean, default=True)

    quotations = relationship("Quotation", back_populates="customer")