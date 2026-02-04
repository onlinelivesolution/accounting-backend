from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class Role(Base):
    __tablename__ = "Role"

    roleID = Column(Integer, primary_key=True, index=True)
    roleName = Column(String(100), nullable=False)
    isActive = Column(Boolean, default=True)

    users = relationship("UserInfo", back_populates="role")
    role_permission_actions = relationship("RolePermissionAction", back_populates="role")
