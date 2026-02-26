from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from src.services.database import Base


class JournalDetail(Base):
    __tablename__ = "JournalDetail"
    __table_args__ = {
        "implicit_returning": False
    }


    journalDetailID = Column(Integer, primary_key=True, index=True)
    journalType = Column(String(50), nullable=False)  # OPENING, GENERAL, ADJUSTMENT
    journalHeaderID = Column(
        Integer,
        ForeignKey("JournalHeader.journalHeaderID"),
        nullable=False
    )

    detailItemCode = Column(
        String(50),
        ForeignKey("DetailItem.detailItemCode"),
        nullable=False
    )

    debitAmount = Column(Numeric(18, 2), default=0)
    creditAmount = Column(Numeric(18, 2), default=0)
    vatPercent = Column(Numeric(5, 2), default=0)
    narration = Column(String(255), nullable=True)
    fiscalYear = Column(String(20), nullable=True)
