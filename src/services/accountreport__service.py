from typing import List, Optional
from datetime import date
from src.repositories.interfaces.iaccountreport__repository import IAccountReportRepository
from src.services.interfaces.iaccountreport__service import IAccountReportService
from src.schemas.accountreport_schema import AccountReportRead
from decimal import Decimal
from collections import defaultdict

class AccountReportService(IAccountReportService):
    def __init__(self, repository: IAccountReportRepository):
        self.repository = repository
    
    async def get_balance_sheet(self, as_of_date):
        rows = await self.repository.get_balance_sheet(as_of_date)

        result = {
            "assets": [],
            "liabilities": [],
            "equity": []
        }

        for r in rows:
            group = r["BalanceSheetGroup"]

            if group == "Assets":
                result["assets"].append(r)
            elif group == "Liabilities":
                result["liabilities"].append(r)
            elif group == "Equity":
                result["equity"].append(r)

        return result
    
    async def get_trial_balance(self, as_of_date):
        rows = await self.repository.get_trial_balance(as_of_date)

        total_debit = sum(r["DebitBalance"] for r in rows)
        total_credit = sum(r["CreditBalance"] for r in rows)

        return {
            "rows": rows,
            "totalDebit": total_debit,
            "totalCredit": total_credit,
            "isBalanced": total_debit == total_credit
        }
        
    async def get_profit_loss(self, as_of_date):
        rows = await self.repository.get_profit_loss(as_of_date)

        income = []
        expense = []
        cogs = []

        total_income = 0
        total_expense = 0
        total_cogs = 0

        for r in rows:
            control = r["ControlItemName"]
            amount = r["Amount"]

            if control == "Income":
                income.append(r)
                total_income += amount

            elif control == "Expense":
                expense.append(r)
                total_expense += amount

            elif control == "Cost of Goods Sold":
                cogs.append(r)
                total_cogs += amount

        gross_profit = total_income - total_cogs
        net_profit = gross_profit - total_expense

        return {
            "income": income,
            "cogs": cogs,
            "expense": expense,
            "totalIncome": total_income,
            "totalCOGS": total_cogs,
            "totalExpense": total_expense,
            "grossProfit": gross_profit,
            "netProfit": net_profit
        }
    
    async def get_ledger(
        self,
        detailItemCode: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[AccountReportRead]:

        rows = await self.repository.get_ledger_entries(
            detailItemCode,
            start_date,
            end_date
        )

        balance = Decimal("0")
        ledger: List[AccountReportRead] = []

        for row in rows:
            debit = row["debit"] or Decimal("0")
            credit = row["credit"] or Decimal("0")

            if row["normalBalance"] == "DEBIT":
                balance += debit - credit
            else:
                balance += credit - debit

            ledger.append(
                AccountReportRead(
                    journalID=row["journalID"],
                    journalDate=row["journalDate"],
                    journalType=row["journalType"],
                    referenceNo=row["referenceNo"],
                    description=row["description"],
                    detailItemCode=row["detailItemCode"],
                    detailItemName=row["detailItemName"],
                    normalBalance=row["normalBalance"],
                    debit=debit,
                    credit=credit,
                    balance=balance
                )
            )

        return ledger
