from abc import ABC, abstractmethod
from typing import List, Dict

class ITrialBalanceService(ABC):

    @abstractmethod
    async def get_trial_balance(self) -> List[Dict]:
        pass

