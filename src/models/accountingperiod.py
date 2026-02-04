from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from src.services.database import Base

class AccountingPeriod(Base):
    __tablename__ = "AccountingPeriod"

    periodID = Column(Integer, primary_key=True)
    periodStart = Column(Date, nullable=False)
    periodEnd = Column(Date, nullable=False)
    isClosed = Column(Boolean, default=False)
    closedAt = Column(DateTime)
