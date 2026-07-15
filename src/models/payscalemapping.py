from sqlalchemy import Column, Integer, String, DateTime,Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from src.models.payrollitem import PayrollItem


class PayScaleMapping(Base):
    __tablename__ = "PayScaleMapping"

    payscaleMappingID   = Column(Integer, primary_key=True, index=True)    
    payrollItemID       = Column(Integer, ForeignKey("PayrollItem.payrollItemID"))
    payscaleID          = Column(Integer, ForeignKey('PayScale.payscaleID'))
    amount              = Column(Numeric(18, 2), nullable=True)
    createdBy           = Column(String(50), nullable=True)    
    createdDate         = Column(DateTime, nullable=True)
    updatedBy           = Column(String(50), nullable=True)
    updatedDate         = Column(DateTime, nullable=True)   
    companyCode         = Column(String(2), nullable=True)
    isBasic             = Column(Boolean, nullable=True)
    isPF                = Column(Boolean, nullable=True)
    status              = Column(Integer, nullable=True)

    
    payscale = relationship("PayScale", back_populates="mappings")
    payroll_item = relationship("PayrollItem", back_populates="payscale_mappings")
