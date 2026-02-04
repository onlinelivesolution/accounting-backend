from sqlalchemy import Column, Integer, String, DateTime,Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from src.models.payrollitem import PayrollItem


class PayScaleMapping(Base):
    __tablename__ = "PayScaleMapping"

    payscaleMappingID   = Column(Integer, primary_key=True, index=True)    
    payrollItemID       = Column(Integer, ForeignKey("PayrollItem.payrollItemID"))
    payscaleID          = Column(Integer, ForeignKey('PayScale.payscaleID'))
    amount              = Column(Numeric(18, 2), nullable=False)
    createdBy           = Column(String(50), nullable=False)    
    createdDate         = Column(DateTime, nullable=False)
    updatedBy           = Column(String(50), nullable=False)
    updatedDate         = Column(DateTime, nullable=False)   
    companyCode         = Column(String(2), nullable=False)
    isBasic             = Column(Boolean, nullable=False)
    isPF                = Column(Boolean, nullable=False)
    status              = Column(Integer, nullable=False)

    
    payscale = relationship("PayScale", back_populates="mappings")
    payroll_item = relationship("PayrollItem", back_populates="payscale_mappings")
