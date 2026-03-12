from abc import ABC, abstractmethod
from typing import Optional
from src.models.accountingrule import AccountingRule


class IAccountingRuleService(ABC):

    @abstractmethod
    async def get_rule(self, ruleCode: str) -> Optional[AccountingRule]:
        pass

    @abstractmethod
    async def create_rule(self, request):
        pass