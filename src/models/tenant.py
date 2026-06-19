from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from datetime import datetime

from src.services.database import Base


class Tenant(Base):

    __tablename__ = "Tenant"

    tenantID = Column(Integer, primary_key=True, index=True)

    companyName = Column(String(200))
    adminName = Column(String(100), nullable=False)
    databaseName = Column(String(200), unique=True)
    email = Column(String(200), unique=True)
    passwordHash = Column(String(255), nullable=False)  
    isActive = Column(Boolean, default=True)
    status = Column(String(20), default="Pending")
    createdDate = Column(DateTime, default=datetime.utcnow)
    updatedDate = Column(DateTime, nullable=True)    
    approvedBy = Column(String(100), nullable=True)
    approvedDate = Column(DateTime, nullable=True)
