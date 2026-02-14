from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base

class QuotationDetail(Base):
    __tablename__ = "QuotationDetail"
    
    quotationDetailID            = Column(Integer, primary_key=True, index=True) 
    quotationID = Column(Integer, ForeignKey("Quotation.quotationID"), nullable=False)
    itemID               = Column(Integer, nullable=False)
    itemDescription          = Column(String(255), nullable=False)    
    quantity          = Column(Numeric(18, 2), nullable=False)
    unitPrice          = Column(Numeric(18, 2), nullable=True)
    discountAmount          = Column(Numeric(18, 2), nullable=True)
    lineTotal          = Column(Numeric(18, 2), nullable=False)


    quotation = relationship("Quotation", back_populates="items")