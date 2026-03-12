from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class SalesInvoiceDetail(Base):
    __tablename__ = "SalesInvoiceDetail"
    
    salesInvoiceDetailID  = Column(Integer, primary_key=True, index=True) 
    salesInvoiceID        = Column(Integer, ForeignKey("SalesInvoice.salesInvoiceID"), nullable=False)
    itemID              = Column(Integer, nullable=False)
    itemDescription     = Column(String(255), nullable=False)    
    quantity            = Column(Numeric(18, 2), nullable=False)
    unitPrice           = Column(Numeric(18, 2), nullable=True)
    exclusiveAmount     = Column(Numeric(18, 2), nullable=True)
    discountAmount      = Column(Numeric(18, 2), nullable=True)
    vatAmount           = Column(Numeric(18, 2), nullable=True)
    totalAmount           = Column(Numeric(18, 2), nullable=False)
    

    # sales_invoice = relationship("SalesInvoice", back_populates="items")