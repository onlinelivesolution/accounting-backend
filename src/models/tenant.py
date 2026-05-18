from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

from src.services.database import Base


class Tenant(Base):

    __tablename__ = "Tenant"

    tenantID = Column(Integer, primary_key=True, index=True)

    companyName = Column(String(200))

    email = Column(String(200), unique=True)

    databaseName = Column(String(200), unique=True)

    createdDate = Column(DateTime, default=datetime.utcnow)
