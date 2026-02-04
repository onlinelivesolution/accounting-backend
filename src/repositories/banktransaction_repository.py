from decimal import Decimal
from sqlalchemy import select, func
from decimal import Decimal
from src.models.journaldetail_model import JournalDetail
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.interfaces.ibanktransaction_repository import IBankTransactionRepository
from src.models.bankaccount_model import BankAccount
from src.models.detailitem import DetailItem
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail
from src.models.accountingperiod import AccountingPeriod


class BankTransactionRepository(IBankTransactionRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_open_period(self) -> AccountingPeriod | None:
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
            .order_by(AccountingPeriod.periodStart.desc())
        )
        return result.scalars().first()
    
    async def get_account_balance(self, detail_item_code: str) -> Decimal:
        result = await self.db.execute(
            select(
                func.coalesce(func.sum(JournalDetail.debitAmount), 0) -
                func.coalesce(func.sum(JournalDetail.creditAmount), 0)
            ).where(JournalDetail.detailItemCode == detail_item_code)
        )
        return Decimal(result.scalar())

    async def create_transaction(self, data):
        bank_detail = await self.db.get(
            DetailItem, data.bankDetailItemCode
        )
        if not bank_detail:
            raise ValueError("Bank / Cash detail item not found")

        contra_detail = await self.db.get(
            DetailItem, data.contraDetailItemCode
        )
        if not contra_detail:
            raise ValueError("Contra detail item not found")

        # 3. Open Period
        period = await self._get_open_period()
        if not period:
            raise ValueError("No open accounting period found")

        # 4. Journal Header
        header = JournalHeader(
            journalDate=data.transactionDate,
            referenceNo=data.referenceNo,
            description=data.description,
            journalType=data.transactionType,
            periodID=period.periodID
        )

        self.db.add(header)
        await self.db.flush()

        amount = Decimal(data.amount)
        
        if data.transactionType == "DEPOSIT":
            debit_code = bank_detail.detailItemCode
            credit_code = contra_detail.detailItemCode
        else:  # WITHDRAWAL
            debit_code = contra_detail.detailItemCode
            credit_code = bank_detail.detailItemCode

        self.db.add_all([
            JournalDetail(
                journalHeaderID=header.journalHeaderID,
                detailItemCode=debit_code,
                debitAmount=amount,
                creditAmount=Decimal(0)
            ),
            JournalDetail(
                journalHeaderID=header.journalHeaderID,
                detailItemCode=credit_code,
                debitAmount=Decimal(0),
                creditAmount=amount
            )
        ])

        return header
