from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.detailitem import DetailItem
from src.models.journaldetail_model import JournalDetail
from src.repositories.interfaces.itrialbalance__repository import ITrialBalanceRepository
from common.generic.generic_repository import GenericRepository


class TrialBalanceRepository(GenericRepository, ITrialBalanceRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(DetailItem, db)
        self.db = db

    async def get_trial_balance(self):
        stmt = (
            select(
                DetailItem.detailItemCode.label("detailItemCode"),
                DetailItem.detailItemName.label("detailItemName"),
                func.coalesce(func.sum(JournalDetail.debitAmount), 0).label("totalDebit"),
                func.coalesce(func.sum(JournalDetail.creditAmount), 0).label("totalCredit"),
            )
            .join(
                JournalDetail,
                DetailItem.detailItemCode == JournalDetail.detailItemCode
            )
            .group_by(
                DetailItem.detailItemCode,
                DetailItem.detailItemName
            )
            .order_by(DetailItem.detailItemCode)
        )

        result = await self.db.execute(stmt)
        return result.mappings().all()
