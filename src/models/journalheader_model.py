from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.services.database import Base


class JournalHeader(Base):
    __tablename__ = "JournalHeader"

    journalHeaderID = Column(Integer, primary_key=True, index=True)
    journalDate = Column(Date, nullable=False)    
    referenceNo = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    createdDate = Column(DateTime, server_default=func.now())
    journalType = Column(String(50), nullable=False)  # OPENING, GENERAL, ADJUSTMENT
    periodID = Column(
        Integer,
        ForeignKey("AccountingPeriod.periodID"),
        nullable=False
    )

    period = relationship("AccountingPeriod")
