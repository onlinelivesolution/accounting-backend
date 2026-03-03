from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class SalesOrderDetail(Base):
    __tablename__ = "SalesOrderDetail"
    
    salesOrderDetailID  = Column(Integer, primary_key=True, index=True) 
    salesOrderID        = Column(Integer, ForeignKey("SalesOrder.salesOrderID"), nullable=False)
    itemID              = Column(Integer, nullable=False)
    itemDescription     = Column(String(255), nullable=False)    
    quantity            = Column(Numeric(18, 2), nullable=False)
    unitPrice           = Column(Numeric(18, 2), nullable=True)
    exclusiveAmount     = Column(Numeric(18, 2), nullable=True)
    discountAmount      = Column(Numeric(18, 2), nullable=True)
    vatAmount           = Column(Numeric(18, 2), nullable=True)
    lineTotal           = Column(Numeric(18, 2), nullable=False)
    

    sales_order = relationship("SalesOrder", back_populates="items")