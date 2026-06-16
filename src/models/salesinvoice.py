from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class SalesInvoice(Base):
    __tablename__ = "SalesInvoice"
    
    salesInvoiceID     = Column(Integer, primary_key=True, index=True) 
    salesOrderID       = Column(Integer, nullable=True)
    salesInvoiceNo     = Column(String(30), nullable=False)
    customerID         = Column(Integer, ForeignKey("Customer.customerID"), nullable=False) 
    salesInvoiceDate   = Column(Date, nullable=False)  
    exclusiveAmount    = Column(Numeric(18, 2))
    discountAmount     = Column(Numeric(18, 2))
    vatAmount          = Column(Numeric(18, 2))
    totalAmount        = Column(Numeric(18, 2))
    status             = Column(String(20))
    paymentStatus      = Column(String(20))
    remarks            = Column(String(255), nullable=True)
    createdBy          = Column(String(50), nullable=False)    
    createdDate        = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy          = Column(String(50), nullable=True)
    updatedDate        = Column(DateTime, nullable=True) 
    approvedBy         = Column(String(50), nullable=True)
    approvedDate       = Column(DateTime, nullable=True) 
    companyCode        = Column(String(2), nullable=True)

    items = relationship("SalesInvoiceDetail", back_populates="sales_invoice", lazy="selectin")
    customer = relationship("Customer", back_populates="salesinvoices")