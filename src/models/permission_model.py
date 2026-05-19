from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base


class Permission(Base):
    __tablename__ = "Permission"

    permissionID = Column(Integer, primary_key=True, index=True)
    permissionName = Column(String(100), nullable=False)
    moduleName = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    createdBy = Column(String(50), nullable=False)
    createdDate = Column(DateTime, server_default=func.now(), nullable=False)
    updatedBy = Column(String(50), nullable=True)
    updatedDate = Column(DateTime, nullable=True)
    companyCode = Column(String(2), nullable=True)
    permissionKey = Column(String(50), nullable=True)
    isActive = Column(Boolean, default=True)

    actions = relationship(
        "PermissionAction",
        back_populates="permission",
        lazy="selectin"
    )
