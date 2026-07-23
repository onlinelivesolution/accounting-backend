from common.generic.generic_repository import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import re
from sqlalchemy import select, text
from sqlalchemy.dialects import mssql
from decimal import Decimal
from datetime import datetime
from src.models.controlitem import ControlItem
from src.models.vataccountmapping import VatAccountMapping
from src.models.journal_model import Journal
from src.models.vatrate_model import VATRates
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail
from src.models.accountingperiod import AccountingPeriod
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from decimal import Decimal, ROUND_HALF_UP
from src.models.detailitem import DetailItem
from sqlalchemy import select, func, cast, Integer
from src.models.activitycenter import ActivityCenter
from src.models.responsibilitycenter import ResponsibilityCenter
from src.schemas.journal_schema import JournalCreate
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
from common.enum.commenum import DefaultAccount
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
VAT_INPUT_ACCOUNT_CODE = "VAT_INPUT"
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

class CommonJournalRepository(GenericRepository[Journal], ICommonJournalRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Journal, db)

    
    async def get_vat_detail_item(
        self,
        vat_type: str,
        company_code: str
    ):
        result = await self.db.execute(
            select(VatAccountMapping.detailItemCode)
            .where(
                VatAccountMapping.vatType == vat_type,
                VatAccountMapping.companyCode == company_code,
                VatAccountMapping.isActive == True
            )
        )
        return result.scalar_one_or_none()
    
    async def _get_open_period(self):
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
        )
        return result.scalar_one_or_none()
    

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
    
    async def get_vat_rate_by_id(self, vat_rate_id: int) -> Decimal:
        result = await self.db.execute(
            select(VATRates.ratePercent)
            .where(VATRates.vATRateID == vat_rate_id)
        )

        rate_percent = result.scalar()

        if rate_percent is None:
            raise ValueError("Invalid VAT Rate ID")

        print("RAW rate_percent from DB:", repr(rate_percent), type(rate_percent))

        # ✅ REMOVE ALL NON-NUMERIC CHARACTERS (except dot)
        cleaned = re.sub(r"[^\d.]", "", str(rate_percent))

        if not cleaned:
            raise ValueError(f"Invalid VAT rate format in DB: {rate_percent}")

        return Decimal(cleaned)

    async def create_general_journal_entry(self, request):

        period = await self._get_open_period()
        if not period:
            raise ValueError("No open accounting period found")

        fiscal_year = period.fiscalYear
        company_code = period.companyCode

        header = JournalHeader(
            journalDate=request.journalDate,
            journalType=request.journalType,
            referenceNo=request.referenceNo,
            description=request.description,
            periodID=period.periodID,
            fiscalYear=fiscal_year,
            createdDate=datetime.utcnow()
        )

        self.db.add(header)
        await self.db.flush()

        vat_detail_item = await self.get_vat_detail_item("INPUT", company_code)

        for row in request.details:

            base_amount = Decimal(row.amount)
            rate_percent = Decimal("0.00")

            if row.vATRateID:
                rate_percent = await self.get_vat_rate_by_id(row.vATRateID)

            vat_amount = (base_amount * rate_percent / Decimal(100)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            total_amount = base_amount + vat_amount

            print("VAT Rate ID:", row.vATRateID)
            print("VAT %:", rate_percent)
            print("VAT Amount:", vat_amount)

            # Debit (Expense)
            self.db.add(
                JournalDetail(
                    journalHeaderID=header.journalHeaderID,
                    detailItemCode=row.debitItemCode,
                    debitAmount=base_amount,
                    creditAmount=Decimal("0.00"),
                    narration=row.narration,
                    fiscalYear=fiscal_year
                )
            )

            # VAT Debit Line
            if vat_amount > 0:
                if not vat_detail_item:
                    raise ValueError("VAT Input account is not configured")

                self.db.add(
                    JournalDetail(
                        journalHeaderID=header.journalHeaderID,
                        detailItemCode=vat_detail_item,
                        debitAmount=vat_amount,
                        creditAmount=Decimal("0.00"),
                        narration="VAT Input",
                        ratePercent=rate_percent,
                        fiscalYear=fiscal_year
                    )
                )

            # Credit
            self.db.add(
                JournalDetail(
                    journalHeaderID=header.journalHeaderID,
                    detailItemCode=row.creditItemCode,
                    debitAmount=Decimal("0.00"),
                    creditAmount=total_amount,
                    narration=row.narration,
                    fiscalYear=fiscal_year
                )
            )

        await self.db.commit()
        return header
    
    async def get_period_by_date(self, companyCode: str, txn_date):

        # Convert datetime to date
        if isinstance(txn_date, datetime):
            txn_date = txn_date.date()

        print("=" * 60)
        print("Searching Accounting Period")
        print("Company :", companyCode)
        print("Txn Date:", txn_date)
        print("Type    :", type(txn_date))

        # Current database
        db_name = await self.db.execute(text("SELECT DB_NAME()"))
        print("Database:", db_name.scalar())

        # Debug: Show all Accounting Periods
        all_periods = await self.db.execute(
            text("""
                SELECT
                    periodID,
                    companyCode,
                    periodStart,
                    periodEnd,
                    isClosed
                FROM AccountingPeriod
                ORDER BY periodStart
            """)
        )

        print("Accounting Periods:")
        for row in all_periods.fetchall():
            print(row)

        # ORM Query
        stmt = (
            select(AccountingPeriod)
            .where(
                AccountingPeriod.companyCode == companyCode,
                AccountingPeriod.periodStart <= txn_date,
                AccountingPeriod.periodEnd >= txn_date,
            )
        )

        result = await self.db.execute(stmt)
        period = result.scalar_one_or_none()

        print("Matched Period:", period)

        if period:
            print(f"Period ID   : {period.periodID}")
            print(f"Start Date  : {period.periodStart}")
            print(f"End Date    : {period.periodEnd}")
            print(f"Fiscal Year : {period.fiscalYear}")
            print(f"Is Closed   : {period.isClosed}")

        print("=" * 60)

        return period
    
    async def create_journal(self, header: JournalHeader, details: list[JournalDetail]):
        self.db.add(header)
        await self.db.flush()  # to get journalHeaderID
        for line in details:
            line.journalHeaderID = header.journalHeaderID
        self.db.add_all(details)
        # await self.db.commit()
        return header
    
    async def create_invoice_journal_entry(self, data: dict):

        # assuming you already have model
        journal = GeneralJournal(**data)

        self.db.add(journal)
        # ❗ DO NOT commit here (commit in service)

        return journal

    
