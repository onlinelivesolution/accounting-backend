from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.services.database import Base

class PayrollItem(Base):
    __tablename__ = "PayrollItem"

    payrollItemID        = Column(Integer, primary_key=True, index=True)   
    payrollItemName      = Column(String(50), nullable=True)
    createdBy            = Column(String(50), nullable=True)
    createdDate          = Column(DateTime, nullable=True)
    updatedBy            = Column(String(50), nullable=True)
    updatedDate          = Column(DateTime, nullable=True)
    companyCode          = Column(String(2), nullable=True)
    status               = Column(Integer, nullable=True)
    
    payscale_mappings = relationship("PayScaleMapping", back_populates="payroll_item")

