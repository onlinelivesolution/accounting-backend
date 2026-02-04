from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from src.services.database import Base

class Journal(Base):
    __tablename__ = "Journal"

    journalID          = Column(Integer, primary_key=True, index=True)
    journalDate        = Column(DateTime, nullable=False)
    companyCode        = Column(String(2), nullable=False)
    activityCenterCode = Column(String(4), nullable=False)
    respCenterCode     = Column(String(6), nullable=False)
    aBType             = Column(Integer, nullable=False)
    fAType             = Column(Integer, nullable=False)
    controlItemCode    = Column(String(2), nullable=False)
    reportingItemCode  = Column(String(4), nullable=False)
    detailItemCode     = Column(String(6), nullable=False)
    debitAmount        = Column(Numeric(18, 2), nullable=False)
    creditAmount       = Column(Numeric(18, 2), nullable=False)
    referenceNo        = Column(Integer, nullable=False)
    fiscalYear         = Column(String(4), nullable=False)
    accountNumber      = Column(String(12), nullable=False)
    referenceID        = Column(String(30), nullable=False)
    period             = Column(Integer, nullable=False)
    createdBy          = Column(String(50), nullable=False)
    projectCode        = Column(String(50), nullable=False)