from abc import ABC, abstractmethod
from typing import Dict

class IBalanceSheetService(ABC):

    @abstractmethod
    async def get_balance_sheet(self) -> Dict:
        pass
