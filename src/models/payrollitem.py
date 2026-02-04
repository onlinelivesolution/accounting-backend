from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.services.database import Base

class PayrollItem(Base):
    __tablename__ = "PayrollItem"

    payrollItemID        = Column(Integer, primary_key=True, index=True)   
    payrollItemName      = Column(String(50), nullable=False)
    companyCode          = Column(String(2), nullable=False)
    createdBy            = Column(String(50), nullable=False)
    createdDate          = Column(DateTime, nullable=False)
    updatedBy            = Column(String(50), nullable=False)
    updatedDate          = Column(DateTime, nullable=False)
    status               = Column(Integer, nullable=False)
    
    payscale_mappings = relationship("PayScaleMapping", back_populates="payroll_item")

