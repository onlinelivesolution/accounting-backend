from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class Customer(Base):
    __tablename__ = "Customer"
    
    customerID           = Column(Integer, primary_key=True, index=True) 
    customerName         = Column(String(50), nullable=False) 
    creditLimit          = Column(Numeric(18, 2))
    vatReference         = Column(String(50), nullable=True) 
    address              = Column(String(200), nullable=True) 
    phone                = Column(String(50), nullable=True) 
    email                = Column(String(50), nullable=True) 
    postBox              = Column(String(50), nullable=True) 
    faxNumber            = Column(String(50), nullable=True) 
    city                 = Column(String(50), nullable=True) 
    country              = Column(String(50), nullable=True) 
    createdBy            = Column(String(50), nullable=False)    
    createdDate          = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy            = Column(String(50), nullable=True)
    updatedDate          = Column(DateTime, nullable=True) 
    accountNumber        = Column(String(20), nullable=True)
    companyCode          = Column(String(2), nullable=True)
    shippingAddress      = Column(String(200), nullable=True)
    billingAddress       = Column(String(200), nullable=True)
    contactPerson        = Column(String(50), nullable=True)
    isActive             = Column(Boolean, default=True)

    quotations = relationship("Quotation", back_populates="customer")
    salesorders = relationship("SalesOrder", back_populates="customer")
    salesinvoices = relationship("SalesInvoice", back_populates="customer")