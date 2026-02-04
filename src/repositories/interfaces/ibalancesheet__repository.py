from abc import ABC, abstractmethod
from typing import Dict

class IBalanceSheetRepository(ABC):

    @abstractmethod
    async def get_balance_sheet_raw(self) -> Dict:
        pass
