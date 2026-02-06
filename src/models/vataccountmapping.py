from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.services.database import Base

class VatAccountMapping(Base):
    __tablename__ = "VatAccountMapping"

    vatType            = Column(String(20), primary_key=True)
    detailItemCode     = Column(String(9), nullable=False)
    companyCode        = Column(String(2), nullable=False)
    isActive           = Column(Boolean, default=True)
