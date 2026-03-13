from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.repositories.interfaces.iaccountingrule_repository import IAccountingRuleRepository
from src.models.accountingrule import AccountingRule


class AccountingRuleRepository(IAccountingRuleRepository):

    def __init__(self, db):
        self.db = db

    async def get_rule(self, ruleCode: str):

        query = (
            select(AccountingRule)
            .options(selectinload(AccountingRule.details))
            .where(AccountingRule.ruleCode == ruleCode)
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()


    async def create_accounting_rule(self, rule: AccountingRule):

        self.db.add(rule)

        await self.db.commit()
        await self.db.refresh(rule)

        return rule


    async def update_rule(self, rule: AccountingRule):

        await self.db.commit()
        await self.db.refresh(rule)

        return rule