from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class Role(Base):
    __tablename__ = "Role"

    roleID = Column(Integer, primary_key=True, index=True)
    roleName = Column(String(100), nullable=False)
    isActive = Column(Boolean, default=True)
    description = Column(String(50), nullable=True)
    companyCode = Column(String(2), nullable=True)
    createdBy          = Column(String(50), nullable=False)
    createdDate        = Column(DateTime,server_default=func.now(), nullable=False)
    updatedBy          = Column(String(50), nullable=True)
    updatedDate        = Column(DateTime, nullable=True) 
    users = relationship("UserInfo", back_populates="role")
    role_permission_actions = relationship("RolePermissionAction", back_populates="role")
