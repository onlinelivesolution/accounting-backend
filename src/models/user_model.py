from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from src.models.role_model import Role
from sqlalchemy.sql import func


class UserInfo(Base):
    __tablename__ = "UserInfo"

    userID = Column(Integer, primary_key=True, index=True)
    userName = Column(String(50), unique=True, index=True, nullable=False)
    roleID = Column(Integer, ForeignKey("Role.roleID"))
    email = Column(String(100))
    fullName = Column(String(150))
    passwordHash = Column(String(255), nullable=False)
    isActive = Column(Boolean, default=True)
    isSuperAdmin = Column(Boolean, default=False)
    companyCode = Column(String(2))
    createdBy = Column(String(50))
    createdDate = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy = Column(String(50))
    updatedDate = Column(DateTime)
    failedLoginAttempts = Column(Integer, default=0)
    lockedUntil = Column(DateTime, nullable=True)

    # Relationship to Role
    role = relationship("Role", back_populates="users")
