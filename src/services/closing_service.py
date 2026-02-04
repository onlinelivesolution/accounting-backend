from sqlalchemy.ext.asyncio import AsyncSession
from src.models.journaldetail_model import JournalDetail
from src.models.journalheader_model import JournalHeader
from datetime import datetime

class ClosingService:

    def __init__(self, repo, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def post_closing_journal(self, closing_date):

        balances = await self.repo.get_income_expense_balances()

        if not balances:
            return {"message": "No income or expense to close"}

        journal = JournalHeader(
            journalDate=closing_date,
            journalType="CLOSING",
            referenceNo=f"CLOSE-{closing_date.strftime('%Y%m%d')}",
            description="Period closing journal",
        )

        self.db.add(journal)
        await self.db.flush()  # get journalID

        total_income = 0
        total_expense = 0

        for row in balances:
            net = row["credit"] - row["debit"]

            if row["category"] == "INCOME" and net > 0:
                total_income += net

                self.db.add(
                    JournalDetail(
                        journalID=journal.journalID,
                        detailItemCode=row["detailCode"],
                        debitAmount=net,
                        creditAmount=0,
                    )
                )

            elif row["category"] == "EXPENSE" and -net > 0:
                total_expense += -net

                self.db.add(
                    JournalDetail(
                        journalID=journal.journalID,
                        detailItemCode=row["detailCode"],
                        debitAmount=0,
                        creditAmount=-net,
                    )
                )

        # 🔹 Equity Adjustment
        net_profit = total_income - total_expense

        equity_code = "EQT-OPEN"  # your Opening / Retained Equity account

        if net_profit > 0:
            # Profit
            self.db.add(
                JournalDetail(
                    journalID=journal.journalID,
                    detailItemCode=equity_code,
                    debitAmount=0,
                    creditAmount=net_profit,
                )
            )
        else:
            # Loss
            self.db.add(
                JournalDetail(
                    journalID=journal.journalID,
                    detailItemCode=equity_code,
                    debitAmount=abs(net_profit),
                    creditAmount=0,
                )
            )

        await self.db.commit()

        return {
            "message": "Closing journal posted",
            "netProfit": net_profit,
        }
