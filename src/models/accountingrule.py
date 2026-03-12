from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class AccountingRule(Base):
    __tablename__ = "AccountingRule"

    ruleID = Column(Integer, primary_key=True, index=True)
    ruleCode = Column(String(50), unique=True)
    moduleName = Column(String(50))
    description = Column(String(255))
    isActive = Column(Boolean, default=True)

    details = relationship("AccountingRuleDetail", back_populates="rule")