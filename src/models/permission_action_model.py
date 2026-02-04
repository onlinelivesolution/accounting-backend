from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.services.database import Base


class PermissionAction(Base):
    __tablename__ = "PermissionAction"

    permissionActionID = Column(Integer, primary_key=True, index=True)
    permissionID = Column(Integer, ForeignKey("Permission.permissionID"))
    actionName = Column(String(100), nullable=False)
    actionKey = Column(String(50), nullable=False)
    isActive = Column(Boolean, default=True)

    permission = relationship(
        "Permission",
        back_populates="actions"
    )
   
