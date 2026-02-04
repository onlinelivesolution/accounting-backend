from src.services.interfaces.ibalancesheet__service import IBalanceSheetService
from src.repositories.interfaces.ibalancesheet__repository import IBalanceSheetRepository


class BalanceSheetService(IBalanceSheetService):

    def __init__(self, repository: IBalanceSheetRepository):
        self.repository = repository

    async def get_balance_sheet(self):

        rows = await self.repository.get_balance_sheet_raw()

        result = {
            "assets": [],
            "liabilities": [],
            "equity": [],
            "totalAssets": 0,
            "totalLiabilities": 0,
            "totalEquity": 0,
        }

        for r in rows:
            debit = r["debit"]
            credit = r["credit"]

            if r["category"] == "ASSET":
                balance = debit - credit
                result["assets"].append({
                    "detailItemCode": r["detailCode"],
                    "detailItemName": r["detailName"],
                    "amount": balance,
                })
                result["totalAssets"] += balance

            elif r["category"] == "LIABILITY":
                balance = credit - debit
                result["liabilities"].append({
                    "detailItemCode": r["detailCode"],
                    "detailItemName": r["detailName"],
                    "amount": balance,
                })
                result["totalLiabilities"] += balance

            elif r["category"] == "EQUITY":
                balance = credit - debit
                result["equity"].append({
                    "detailItemCode": r["detailCode"],
                    "detailItemName": r["detailName"],
                    "amount": balance,
                })
                result["totalEquity"] += balance

        return result
