from common.generic.generic_repository import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal
from src.models.controlitem import ControlItem
from src.models.journal_model import Journal
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail
from src.models.accountingperiod import AccountingPeriod
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem
from sqlalchemy import select, func, cast, Integer
from src.models.activitycenter import ActivityCenter
from src.models.responsibilitycenter import ResponsibilityCenter
from src.schemas.journal_schema import JournalCreate
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
from common.enum.commenum import DefaultAccount
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository


class CommonJournalRepository(GenericRepository[Journal], ICommonJournalRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Journal, db)
    
    async def _get_open_period(self) -> AccountingPeriod | None:
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
            .order_by(AccountingPeriod.periodStart.desc())
        )
        return result.scalars().first()
    

    async def get_detail_item_by_account_id(self, account_id: int) -> str:
        result = await self.db.execute(
            select(DetailItem.detailItemCode)
            .where(DetailItem.accountID == account_id)
            .limit(1)
        )
        return result.scalar_one()
    
    async def get_bank_detail_item_by_account_id(self, account_id: int) -> str:
        result = await self.db.execute(
            select(DetailItem.detailItemCode)
            .where(DetailItem.accountID == account_id)
            .limit(1)
        )
        return result.scalar_one()

    async def resolve_detail_hierarchy(self, detail_item_code: str) -> dict:
        result = await self.db.execute(
            select(
                DetailItem.detailItemCode,
                ReportingItem.reportingItemCode,
                ControlItem.controlItemCode,
                ControlItem.fATypeID
            )
            .join(ReportingItem, DetailItem.reportingItemCode == ReportingItem.reportingItemCode)
            .join(ControlItem, ReportingItem.controlItemCode == ControlItem.controlItemCode)
            .where(DetailItem.detailItemCode == detail_item_code)
        )
        row = result.one()

        return {
            "detailItemCode": row.detailItemCode,
            "reportingItemCode": row.reportingItemCode,
            "controlItemCode": row.controlItemCode,
            "fAType": row.fATypeID,
        }

    async def get_default_activity_center(self, company_code: str) -> str:
        result = await self.db.execute(
            select(ActivityCenter.activityCenterCode)
            .where(ActivityCenter.companyCode == company_code)
            .order_by(ActivityCenter.activityCenterCode)
            .limit(1)
        )
        return result.scalar_one()

    async def get_default_resp_center(self, company_code: str) -> str:
        result = await self.db.execute(
            select(ResponsibilityCenter.respCenterCode)
            .order_by(ResponsibilityCenter.respCenterCode)
            .limit(1)
        )
        return result.scalar_one()

    async def get_current_fiscal_year(self, company_code: str) -> int:
        return 2025  # or fetch dynamically

    async def create_opening_balance_journal(self, data: dict):
        journal = Journal(**data)
        self.db.add(journal)
        await self.db.flush()
    
    async def create_opening_balance(self, data: dict):
        journaldetail = JournalDetail(**data)
        self.db.add(journaldetail)
        await self.db.flush()
        
    async def create_bank_deposit_journal(self, data: dict):
        journal = Journal(**data)
        self.db.add(journal)
        await self.db.flush()
        
    async def create_bank_withdraw_journal(self, data: dict):
        journal = Journal(**data)
        self.db.add(journal)
        await self.db.flush()
        
    async def get_next_control_item_code(self) -> str:
        stmt = select(
            func.max(cast(ControlItem.controlItemCode, Integer))
        )
        result = await self.db.execute(stmt)
        max_code = result.scalar()

        if max_code is None:
            next_code = 1
        else:
            next_code = max_code + 1

        return f"{next_code:02d}"
    
    async def create_general_journal_entry(self, request):

        # 1. Validate accounting period
        period = await self._get_open_period()
        if not period:
            raise ValueError("No open accounting period found")

        # 2. Create Journal Header
        header = JournalHeader(
            journalDate=request.journalDate,
            journalType=request.journalType,
            referenceNo=request.referenceNo,
            description=request.description,
            periodID=period.periodID
        )

        self.db.add(header)
        await self.db.flush()  # gets journalHeaderID

        # 3. Insert Journal Details
        for row in request.details:
            amount = Decimal(row.amount)

            self.db.add_all([
                JournalDetail(
                    journalHeaderID=header.journalHeaderID,
                    detailItemCode=row.debitItemCode,
                    debitAmount=amount,
                    creditAmount=Decimal(0)
                ),
                JournalDetail(
                    journalHeaderID=header.journalHeaderID,
                    detailItemCode=row.creditItemCode,
                    debitAmount=Decimal(0),
                    creditAmount=amount
                )
            ])

        # ✅ 4. COMMIT (THIS WAS MISSING)
        await self.db.commit()

        return header