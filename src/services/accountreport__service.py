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