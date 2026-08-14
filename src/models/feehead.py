from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from src.services.database import Base


class FeeHead(Base):
    __tablename__ = "FeeHead"

    feeHeadID: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    feeHeadCode: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    feeHeadName: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    defaultAmount: Mapped[float] = mapped_column(
        Numeric(18, 2), nullable=False, default=0
    )

    frequency: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Monthly"
    )

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")

    createdDate: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    updatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    studentFees = orm_relationship(
        "StudentFee", back_populates="feeHead", lazy="selectin"
    )
