from abc import ABC, abstractmethod
from typing import Optional
from src.models.accountingrule import AccountingRule


class IAccountingRuleRepository(ABC):

    @abstractmethod
    async def get_rule(self, ruleCode: str) -> Optional[AccountingRule]:
        pass

    @abstractmethod
    async def create_accounting_rule(self, rule: AccountingRule) -> AccountingRule:
        pass

    @abstractmethod
    async def update_rule(self, rule: AccountingRule) -> AccountingRule:
        pass