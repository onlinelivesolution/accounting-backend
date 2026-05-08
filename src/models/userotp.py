from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.services.database import Base


class UserOTP(Base):

    __tablename__ = "UserOTP"

    otpID = Column(Integer, primary_key=True, index=True)

    userID = Column(Integer)

    otpCode = Column(String(10))

    expiryTime = Column(DateTime)

    isUsed = Column(Boolean, default=False)