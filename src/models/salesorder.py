from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class SalesOrder(Base):
    __tablename__ = "SalesOrder"
    
    salesOrderID       = Column(Integer, primary_key=True, index=True) 
    quotationID        = Column(Integer, nullable=False)
    salesOrderNo       = Column(String(30), nullable=False)
    salesOrderDate     = Column(Date, nullable=False)
    customerID         = Column(Integer, ForeignKey("Customer.customerID"))   
    exclusiveAmount    = Column(Numeric(18, 2))
    discountAmount     = Column(Numeric(18, 2))
    vatAmount          = Column(Numeric(18, 2))
    totalAmount        = Column(Numeric(18, 2))
    status             = Column(String(20))
    expireDate         = Column(Date, nullable=False)
    remarks            = Column(String(255), nullable=False)
    createdBy          = Column(String(50), nullable=False)    
    createdDate        = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy          = Column(String(50), nullable=True)
    updatedDate        = Column(DateTime, nullable=True) 
    approvedBy         = Column(String(50), nullable=True)
    approvedDate       = Column(DateTime, nullable=True) 

    items = relationship("SalesOrderDetail", back_populates="sales_order", lazy="selectin")
    customer = relationship("Customer", back_populates="salesorders")