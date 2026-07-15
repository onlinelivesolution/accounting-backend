from sqlalchemy import Column, String, Integer, Boolean, DateTime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship
from src.services.database import Base

class FiscalYear(Base):
    __tablename__ = "FiscalYear"

    finYearID = Column("FinYearID", Integer, primary_key=True, autoincrement=True)
    finYear = Column("FinYear", String(4), nullable=False)
    openClose = Column("OpenClose", Boolean, default=True)
    status = Column("Status", String(1), default="O")
    comments = Column("Comments", String(50), nullable=True)
    dateOpen = Column("DateOpen", DateTime, nullable=False)
    dateClose = Column("DateClose", DateTime, nullable=True)
    isCeilingLoced = Column("IsCeilingLoced", Boolean, default=False)
    isUpDateClosed = Column("IsUpDateClosed", Boolean, default=False)
    isCurrentFinYear = Column("IsCurrentFinYear", Boolean, default=True)
    companyCode = Column("CompanyCode", String(2), nullable=False)
    
    class Config:
        from_attributes = True