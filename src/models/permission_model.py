from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base


class Permission(Base):
    __tablename__ = "Permission"

    permissionID = Column(Integer, primary_key=True, index=True)
    permissionName = Column(String(100), nullable=False)
    isActive = Column(Boolean, default=True)

    actions = relationship(
        "PermissionAction",
        back_populates="permission",
        lazy="selectin"
    )
