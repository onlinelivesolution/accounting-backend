from datetime import date
from src.models.accountingperiod import AccountingPeriod
from src.services.interfaces.iperiod__service import IPeriodService
from src.repositories.interfaces.iperiod__repository import IPeriodRepository

class PeriodService(IPeriodService):

    def __init__(self, repository: IPeriodRepository):
        self.repository = repository

    async def create_period(self, start: date, end: date) -> AccountingPeriod:
        period = AccountingPeriod(
            periodStart=start,
            periodEnd=end,
            isClosed=False
        )
        return await self.repository.create_period(period)

    # async def close_period(self, end: date) -> AccountingPeriod:
    #     return await self.repository.close_period(end)
    
    async def close_period(self, period_end: date):
        return await self.repository.close_period(period_end)

    async def validate_open_period(self, journal_date: date):
        if await self.repository.is_period_closed(journal_date):
            raise ValueError("Accounting period is closed. Posting not allowed.")
