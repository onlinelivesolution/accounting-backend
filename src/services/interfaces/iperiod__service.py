from abc import ABC, abstractmethod
from datetime import date
from src.models.accountingperiod import AccountingPeriod

class IPeriodService(ABC):

    @abstractmethod
    async def create_period(self, start: date, end: date) -> AccountingPeriod: ...

    @abstractmethod
    async def close_period(self, end: date) -> AccountingPeriod: ...

    @abstractmethod
    async def validate_open_period(self, journal_date: date): ...
