from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class AccountingRuleDetail(Base):
    __tablename__ = "AccountingRuleDetail"

    ruleDetailID = Column(Integer, primary_key=True)

    ruleID = Column(Integer, ForeignKey("AccountingRule.ruleID"))

    accountCode = Column(String(20))
    entryType = Column(String(10))  # DEBIT / CREDIT
    amountSource = Column(String(50))

    rule = relationship("AccountingRule", back_populates="details")