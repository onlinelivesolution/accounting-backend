from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.services.database import Base 
from sqlalchemy.sql import func

class SystemUser(Base):
    __tablename__ = "SystemUser"

    systemUserID = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    passwordHash = Column(String(255))
    email = Column(String(100))
    role = Column(String(50), default="SystemAdmin")

    otp = Column(String(10), nullable=True)
    otpExpiry = Column(DateTime, nullable=True)

    isActive = Column(Boolean, default=True) 
    
    createdBy          = Column(Integer,  nullable=False)   
    createdDate        = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy          = Column(Integer,  nullable=False) 
    updatedDate        = Column(DateTime, nullable=True) 
