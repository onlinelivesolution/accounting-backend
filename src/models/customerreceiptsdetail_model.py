# models/customer_receipt.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.services.database import Base

class CustomerReceiptDetail(Base):
    __tablename__ = "CustomerReceiptDetail"

    customerReceiptDetailID = Column(Integer, primary_key=True, index=True)

    customerReceiptID = Column(
        Integer,
        ForeignKey("CustomerReceipt.customerReceiptID"),
        nullable=False
    )

    invoiceID = Column(Integer, nullable=False)
    paidAmount = Column(DECIMAL(18, 2), nullable=False)
    discountAmount = Column(DECIMAL(18, 2), nullable=True)

    # Optional fields
    narration = Column(String(255), nullable=True)

    # ✅ Relationship back
    receipt = relationship("CustomerReceipt", back_populates="details")