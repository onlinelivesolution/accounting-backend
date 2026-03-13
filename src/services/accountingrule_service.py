from src.services.interfaces.iaccountingrule_service import IAccountingRuleService
from src.repositories.interfaces.iaccountingrule_repository import IAccountingRuleRepository
from src.models.accountingrule import AccountingRule
from src.models.accountingruledetail import AccountingRuleDetail


class AccountingRuleService(IAccountingRuleService):

    def __init__(self, repository: IAccountingRuleRepository):
        self.repository = repository


    async def get_rule(self, ruleCode: str):

        return await self.repository.get_rule(ruleCode)


    async def create_accounting_rule(self, request):

        rule = AccountingRule(
            ruleCode=request.ruleCode,
            moduleName=request.moduleName,
            description=request.description
        )

        for d in request.details:

            detail = AccountingRuleDetail(
                accountCode=d.accountCode,
                entryType=d.entryType,
                amountSource=d.amountSource
            )

            rule.details.append(detail)

        return await self.repository.create_accounting_rule(rule)