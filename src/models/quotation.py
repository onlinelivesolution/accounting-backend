from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class Quotation(Base):
    __tablename__ = "Quotation"
    
    quotationID            = Column(Integer, primary_key=True, index=True) 
    quotationNo         = Column(String(30), nullable=False)
    quotationDate         = Column(Date, nullable=False)
    customerID = Column(Integer, ForeignKey("Customer.customerID"))   
    subtotalAmount          = Column(Numeric(18, 2))
    discountAmount          = Column(Numeric(18, 2))
    vATAmount          = Column(Numeric(18, 2))
    totalAmount          = Column(Numeric(18, 2))
    status              = Column(String(20))
    expireDate      = Column(Date, nullable=False)
    remarks          = Column(String(255), nullable=False)
    createdBy           = Column(String(50), nullable=False)    
    createdDate        = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy          = Column(String(50), nullable=True)
    updatedDate        = Column(DateTime, nullable=True) 
    approvedBy          = Column(String(50), nullable=True)
    approvedDate        = Column(DateTime, nullable=True) 

    items = relationship("QuotationDetail", back_populates="quotation", cascade="all, delete-orphan")
    customer = relationship("Customer", back_populates="quotations")