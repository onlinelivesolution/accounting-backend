from src.services.interfaces.itrialbalance__service import ITrialBalanceService
from src.repositories.interfaces.itrialbalance__repository import ITrialBalanceRepository


class TrialBalanceService(ITrialBalanceService):

    def __init__(self, repository: ITrialBalanceRepository):
        self.repository = repository

    async def get_trial_balance(self):
        rows = await self.repository.get_trial_balance()

        result = []

        for r in rows:
            debit = r["totalDebit"]
            credit = r["totalCredit"]

            result.append({
                "detailItemCode": r["detailItemCode"],
                "detailItemName": r["detailItemName"],
                "debit": max(debit - credit, 0),
                "credit": max(credit - debit, 0),
            })

        return result
