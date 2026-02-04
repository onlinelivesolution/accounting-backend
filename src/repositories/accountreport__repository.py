from typing import List, Optional
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.detailitem import DetailItem
from src.models.journaldetail_model import JournalDetail
from src.models.journalheader_model import JournalHeader
from src.schemas.accountreport_schema import AccountReportRead
from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.iaccountreport__repository import IAccountReportRepository

class AccountReportRepository(GenericRepository[JournalDetail], IAccountReportRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(JournalDetail, db)
        self.db = db

    async def get_ledger_entries(
        self,
        detailItemCode: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[dict]:

        query = (
            select(
                JournalHeader.journalID,
                JournalHeader.journalDate,
                JournalHeader.journalType,
                JournalHeader.referenceNo,
                JournalHeader.description,
                DetailItem.detailItemCode,
                DetailItem.detailItemName,
                DetailItem.normalBalance,
                JournalDetail.debitAmount.label("debit"),
                JournalDetail.creditAmount.label("credit"),
            )
            .join(JournalHeader, JournalHeader.journalID == JournalDetail.journalID)
            .join(DetailItem, DetailItem.detailItemCode == JournalDetail.detailItemCode)
            .where(JournalDetail.detailItemCode == detailItemCode)
        )

        if start_date:
            query = query.where(JournalHeader.journalDate >= start_date)

        if end_date:
            query = query.where(JournalHeader.journalDate <= end_date)

        query = query.order_by(
            JournalHeader.journalDate,
            JournalHeader.journalID
        )

        result = await self.db.execute(query)
        return result.mappings().all()