from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from src.models.accountingperiod import AccountingPeriod

class IPeriodRepository(ABC):

    @abstractmethod
    async def is_period_closed(self, journal_date: date) -> bool: ...

    @abstractmethod
    async def close_period(self, period_end: date) -> AccountingPeriod: ...

    @abstractmethod
    async def create_period(self, period: AccountingPeriod) -> AccountingPeriod: ...
    
    @abstractmethod
    async def get_open_period(self) -> Optional[AccountingPeriod]:
        ...
