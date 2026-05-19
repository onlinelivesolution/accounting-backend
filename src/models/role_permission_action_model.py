from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from src.services.database import Base


class RolePermissionAction(Base):
    __tablename__ = "RolePermissionAction"

    rolePermissionActionID = Column(Integer, primary_key=True, index=True)
    roleID = Column(Integer, ForeignKey("Role.roleID"))
    permissionID = Column(Integer, ForeignKey("Permission.permissionID"))
    permissionActionID = Column(Integer, ForeignKey("PermissionAction.permissionActionID"))
    isAllowed = Column(Boolean, default=False)
    createdBy = Column(String(50), nullable=True)
    updatedBy = Column(String(50), nullable=True)
    updatedDate = Column(DateTime, nullable=True)
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())

    role = relationship("Role", back_populates="role_permission_actions")
    permission = relationship("Permission")
    permission_action = relationship("PermissionAction")

