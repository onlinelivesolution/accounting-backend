from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.journaldetail_model import JournalDetail
from src.models.detailitem import DetailItem
from src.models.reportingitem import ReportingItem
from src.models.controlitem import ControlItem
 

class ClosingRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_income_expense_balances(self):

        stmt = (
            select(
                ControlItem.accountCategory.label("category"),
                DetailItem.detailItemCode.label("detailCode"),
                func.coalesce(func.sum(JournalDetail.debitAmount), 0).label("debit"),
                func.coalesce(func.sum(JournalDetail.creditAmount), 0).label("credit"),
            )
            .join(DetailItem, JournalDetail.detailItemCode == DetailItem.detailItemCode)
            .join(ReportingItem, DetailItem.reportingItemCode == ReportingItem.reportingItemCode)
            .join(ControlItem, ReportingItem.controlItemCode == ControlItem.controlItemCode)
            .where(ControlItem.accountCategory.in_(["INCOME", "EXPENSE"]))
            .group_by(
                ControlItem.accountCategory,
                DetailItem.detailItemCode,
            )
        )

        result = await self.db.execute(stmt)
        return result.mappings().all()
