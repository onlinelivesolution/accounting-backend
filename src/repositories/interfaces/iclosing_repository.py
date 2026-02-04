from abc import ABC, abstractmethod
from typing import List, Dict

class IClosingRepository(ABC):

    @abstractmethod
    async def get_income_expense_balances(self) -> List[Dict]:
        pass
