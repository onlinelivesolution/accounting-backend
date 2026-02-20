from abc import ABC, abstractmethod
from typing import List, Optional
from src.schemas.accountreport_schema import AccountReportRead
from datetime import date

class IAccountReportRepository(ABC):

    @abstractmethod
    async def get_balance_sheet(self, as_of_date: date):
        pass
    
    @abstractmethod
    async def get_trial_balance(self, as_of_date: date):
        pass
    
    @abstractmethod
    async def get_profit_loss(self, as_of_date: date):
        pass
    
    @abstractmethod
    async def get_ledger_entries(
        self,
        detailItemCode: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[AccountReportRead]:
        ...
