from sqlalchemy import Column, Integer, String

from src.services.database import Base


class AccountMapping(Base):
    __tablename__ = "AccountMapping"

    accountMappingID = Column(Integer, primary_key=True, index=True)
    accountMappingType = Column(String(25), nullable=True)
    controlItem = Column(String(20), nullable=True)
    financialStatement = Column(String(5), nullable=True)
    normalBalance = Column(String(6), nullable=True)