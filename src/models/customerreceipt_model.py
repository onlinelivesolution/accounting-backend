from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.services.database import Base


class CustomerReceipt(Base):
    __tablename__ = "CustomerReceipt"

    customerReceiptID = Column(Integer, primary_key=True, index=True)
    receiptNo = Column(String(50), nullable=False, unique=True)
    receiptDate = Column(Date, nullable=False)

    customerID = Column(Integer, nullable=False)
    totalAmount = Column(DECIMAL(18, 2), nullable=False)

    status = Column(String(20), default="DRAFT")  # DRAFT / APPROVED

    isDeleted = Column(Boolean, default=False)
    createdBy = Column(String(50), nullable=True)
    createdDate = Column(DateTime, default=datetime.utcnow)
    updatedBy = Column(String(50), nullable=True)
    updatedDate = Column(DateTime, nullable=True)

    # ✅ Relationship
    details = relationship(
        "CustomerReceiptDetail",
        back_populates="receipt",
        cascade="all, delete-orphan"
    )


class CustomerReceiptDetail(Base):
    __tablename__ = "CustomerReceiptDetail"

    customerReceiptDetailID = Column(Integer, primary_key=True, index=True)

    customerReceiptID = Column(
        Integer,
        ForeignKey("CustomerReceipt.customerReceiptID"),
        nullable=False
    )

    salesInvoiceID = Column(Integer, nullable=False)
    paidAmount = Column(DECIMAL(18, 2), nullable=False)

    # Optional fields
    narration = Column(String(255), nullable=True)

    # ✅ Relationship back
    receipt = relationship("CustomerReceipt", back_populates="details")