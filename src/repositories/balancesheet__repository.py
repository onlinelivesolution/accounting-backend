from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem
from src.models.journaldetail_model import JournalDetail
from src.repositories.interfaces.ibalancesheet__repository import IBalanceSheetRepository
from common.generic.generic_repository import GenericRepository


class BalanceSheetRepository(GenericRepository, IBalanceSheetRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(DetailItem, db)
        self.db = db

    async def get_balance_sheet_raw(self):

        stmt = (
            select(
                ControlItem.accountCategory.label("category"),
                ControlItem.controlItemName.label("controlName"),
                DetailItem.detailItemCode.label("detailCode"),
                DetailItem.detailItemName.label("detailName"),
                func.coalesce(func.sum(JournalDetail.debitAmount), 0).label("debit"),
                func.coalesce(func.sum(JournalDetail.creditAmount), 0).label("credit"),
            )
            .join(ReportingItem, ReportingItem.controlItemCode == ControlItem.controlItemCode)
            .join(DetailItem, DetailItem.reportingItemCode == ReportingItem.reportingItemCode)
            .outerjoin(
                JournalDetail,
                JournalDetail.detailItemCode == DetailItem.detailItemCode
            )
            .where(
                ControlItem.accountCategory.in_(["ASSET", "LIABILITY", "EQUITY"])
            )
            .group_by(
                ControlItem.accountCategory,
                ControlItem.controlItemName,
                DetailItem.detailItemCode,
                DetailItem.detailItemName
            )
            .order_by(ControlItem.accountCategory, DetailItem.detailItemCode)
        )

        result = await self.db.execute(stmt)
        return result.mappings().all()
