from abc import ABC, abstractmethod
from typing import List, Optional
from src.schemas.accountreport_schema import AccountReportRead
from datetime import date

class IAccountReportService(ABC):

    @abstractmethod
    async def get_ledger(
        self,
        detailItemCode: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[AccountReportRead]:
        ...
