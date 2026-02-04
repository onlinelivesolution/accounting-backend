from datetime import date, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.accountingperiod import AccountingPeriod
from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.iperiod__repository import IPeriodRepository

class PeriodRepository(GenericRepository[AccountingPeriod], IPeriodRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(AccountingPeriod, db)
        self.db = db

    async def is_period_closed(self, journal_date: date) -> bool:
        q = select(AccountingPeriod).where(
            AccountingPeriod.periodStart <= journal_date,
            AccountingPeriod.periodEnd >= journal_date,
            AccountingPeriod.isClosed == True
        )
        result = await self.db.execute(q)
        return result.scalar_one_or_none() is not None

    async def close_period(self, period_end: date) -> AccountingPeriod:
        q = select(AccountingPeriod).where(
            AccountingPeriod.periodEnd == period_end
        )
        result = await self.db.execute(q)
        period = result.scalar_one_or_none()

        if not period:
            raise ValueError("Accounting period not found")

        period.isClosed = True
        period.closedAt = datetime.utcnow()
        return period

    async def create_period(self, period: AccountingPeriod) -> AccountingPeriod:
        return await self.create(period)
    
    async def get_open_period(self) -> AccountingPeriod | None:
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
            .order_by(AccountingPeriod.periodStart.desc())
        )
        return result.scalars().first()
